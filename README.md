# Controle de acesso do LAR (Laboratório de Automação e Robótica)

![1](https://github.com/Natalnet/lar-door/blob/master/images/door-circuit.jpg)

Este projeto consiste em fazer um controle de acesso simples, utilizando uma placa feita com componentes básicos para gerenciar entradas e saídas do laboratório.

## Configuração dentro do MCU

```bash
{
    "ssid": "<ssid>",
    "ssid_password": "<password>",
    "mqtt_address": "127.0.0.1",
    "mqtt_port": 1883,
    "mqtt_user": "mqtt",
    "mqtt_password": "<password>",
    "topic_sub": "door/input",
    "topic_pub": "door/output"
}
```

## Pinagem (GPIO, SCK, SCL, SDA, MFCR)

GPIO '2': **Relé / SPI**
GPIO '12': **Botão de saída**

GPIO '27': **Cor vermelha do RGB**
GPIO '25': **Cor verde do RGB**
GPIO '26': **Cor azul do RGB**

GPIO '32': **Buzzer interno**
GPIO '14': **Buzzer externo**

GPIO RST '4': **Recebimento do MFRC522**
GPIO CS '5': **Envio do MFRC522**
