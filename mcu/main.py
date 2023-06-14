from controller.rfidcontroller import RFiDController as rc
from controller.databasecontroller import DatabaseController as dc

from machine import Pin, PWM
from communicator.umqttsimple import MQTTClient

import time

adminMode = False

tick_counter = 0
tick_interval = 60

relay = Pin(2, Pin.OUT)
button = Pin(12, Pin.IN, Pin.PULL_UP)
buzzer = PWM(Pin(14, Pin.OUT))

red = Pin(27, Pin.OUT)
green = Pin(25, Pin.OUT)
blue = Pin(26, Pin.OUT)

internal_buzzer = PWM(Pin(32, Pin.OUT))

green.off()
blue.on()
red.on()

buzzer.duty(0)
internal_buzzer.duty(0)

dc = dc()
rc = rc()

def connect_and_subscribe():
    global client_id, mqtt_address, mqtt_port, topic_pub, topic_sub, mqtt_user, mqtt_password, ssid, mqtt_con_flag, pingresp_rcv_flag, next_ping_time
    
    client = MQTTClient(client_id, mqtt_address, mqtt_port, mqtt_user, mqtt_password)
    
    client.set_callback(sub_cb)
    client.connect(clean_session=True)
    client.subscribe(topic_sub)
    
    client.publish(topic_pub, 'Connected to MQTT address ' + mqtt_address + ' with sucess. (No retained messages)')
    
    mqtt_con_flag = True
    pingresp_rcv_flag = True
    
    next_ping_time = time.time() + tick_interval
    
    lock = False
    
    return client

def restart_and_reconnect():
    time.sleep_ms(5000)
    
    machine.reset()

def sub_cb(topic, msg):
    global topic_sub, topic_pub
    
    if topic == topic_sub and msg == b'open':
        print('test')

def ping():
    client.ping()
    
    ping_reset()

def ping_reset():
    global next_ping_time
    
    next_ping_time = time.time() + tick_interval

def ping_check():
    global next_ping_time, mqtt_con_flag, pingresp_rcv_flag
    
    if time.time() >= next_ping_time:
        
        if not pingresp_rcv_flag:
            mqtt_con_flag = False
        else:
            ping()
            
            pingresp_rcv_flag = False
            
    res = client.check_msg()
    
    if (res == b'PINGRESP'):
        pingresp_rcv_flag = True
        
        print('OK')
    
try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

def grant(delay, name, rfid):
    global topic_pub
    
    relay.value(0)
    
    buzzer.freq(3000)
    buzzer.duty(1023)
    
    green.on()
    blue.off()
    red.on()
    
    time.sleep_ms(350)
    
    blue.on()
    green.off()
    red.on()
    
    buzzer.duty(0)
    
    client.publish(topic_pub, f'ACCESS -> {name} entered in the LAB (RFID: {rfid})')
    
    time.sleep_ms(delay)

def deny(tag):
    global topic_pub
    
    relay.value(1)
    
    client.publish(topic_pub, f'ACCESS -> {tag} has no permission to enter in the LAB')
    
    red.off()
    green.off()
    blue.off()
    
    time.sleep_ms(350)
    
    blue.on()
    green.off()
    red.on()

def admin():
    global topic_pub
    
    relay.value(0)
    
    client.publish(topic_pub, f'MODE -> Door entered in the program mode, releasing the relay')

def normal():
    relay.value(1)

while True:
    
    global topic_pub, lock, mqtt_con_flag
    
    cardTag = str(rc.get())
    
    try:
        ping_check()
    except:
        lock = True
        
        mqtt_con_flag = False
        
        time.sleep_ms(1000)
        
        restart_and_reconnect()
    
    while cardTag == 'no-tag':
        
        client.check_msg()
        
        if button.value() == 0:
            
            relay.value(0)
            
            internal_buzzer.freq(2500)
            internal_buzzer.duty(1023)
            
            time.sleep_ms(3000)
            
            relay.value(1)
            
            internal_buzzer.duty(0)
        
        else:
            
            relay.value(1)
            
            internal_buzzer.duty(0)
        
        if adminMode == True:
            admin()
        else:
            normal()
        
        cardTag = str(rc.get())
        
        if (time.time() - last_msg) >= message_interval:
            client.publish(topic_pub, f'OK {tick_counter}', 1)
        
        last_msg = time.time()
        
        tick_counter += 1
        
        relay.value(1)
    
    if adminMode == True:
        
        if dc.ismastercard(cardTag):
            
            client.publish(topic_pub, 'MODE -> Door left the program mode, attaching the relay')
            
            adminMode = False
        
        else:
            
            if dc.findcard(cardTag)[0]:
                
                client.publish(topic_pub, f'UNREGISTER -> RFiD {cardTag} has been removed from the database')
                
                dc.removecard(cardTag)
                
                time.sleep_ms(3000)
                
            else:
                
                client.publish(topic_pub, f'REGISTER -> RFiD {cardTag} added to database by an administrator')
                
                dc.addcard(cardTag, input('Holder name'))
                
                time.sleep_ms(3000)
    else:
        
        if dc.ismastercard(cardTag):
            
            adminMode = True
            
            time.sleep_ms(2000)
            
            amount = dc.amount()
            
            client.publish(topic_pub, f'STATUS -> {amount} cards registered in the internal database')
            
            time.sleep_ms(1000)
            
            client.publish(topic_pub, 'REQUEST -> Door requesting a card to be added or removed')
        
        else:
            
            if dc.findcard(cardTag)[0]:
                grant(3000, 'test', cardTag)
            else:
                deny(cardTag)
