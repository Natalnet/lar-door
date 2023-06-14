import gc, ujson, json, esp, ubinascii, machine, network, esp32

from communicator.umqttsimple import MQTTClient

esp.osdebug(None)

gc.collect()

config = open('config.json')

load_config = json.load(config)

config.close()

ssid_name = load_config["ssid"]
ssid_password = load_config["ssid_password"]

mqtt_address = load_config["mqtt_address"]
mqtt_port = load_config["mqtt_port"]
mqtt_user = load_config["mqtt_user"]
mqtt_password = load_config["mqtt_password"]

client_id = ubinascii.hexlify(machine.unique_id())

topic_sub = bytes(load_config['topic_sub'], 'utf-8')
topic_pub = bytes(load_config['topic_pub'], 'utf-8')

last_msg = 0
message_interval = 1

mqtt_con_flag = False
pingresp_rcv_flag = True
lock = True
next_ping_time = 0

try:
    print('Loading RFID database')
    
    db = open('ID.json').read()
    
    print('RFID database was loaded')
    
except:
    
    print('Error trying to load the RFID database')
    print('Attempting to load RFID database')
    
    db = open('ID.json', 'w')
    
    print('RFID database was loaded')
    
    db.close()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():
    
    print('Connecting to WiFi...')
    
    wlan.connect(ssid_name, ssid_password)
    
    while not wlan.isconnected():
        pass
    
    print('Connected to network: ', wlan.ifconfig())

print('Door system started successfully')



    
    

