import time
import machine
from umqttsimple import MQTTClient
from machine import ADC
from machine import Pin
from machine import WDT

wdt = WDT()  # enable it with a timeout of 2s
analog = ADC(0)     # create ADC object on ADC pin
GPIO5_D1 = Pin(5, Pin.OUT)
GPIO5_D1.on()

mqtt_server = 'mqtt.by'
mqtt_port = 1883
mqtt_user = 'MQTT_LOGIN'
mqtt_password = 'MQTT_PASS'
client_id = 'wifiRelay'
topic_prefix = b'/user/valik/'
topic_sub = topic_prefix + b'krd/zal/clickRelay'
topic_pub = topic_prefix + b'krd/zal/status'

# Complete project details at https://RandomNerdTutorials.com

def sub_cb(topic, msg):
    print((topic, msg))
    if topic == topic_sub:
        if msg == b'0':
            if status != 1024:
                print('forced turn off')
                GPIO5_D1.off()
                time.sleep(3.5)
                GPIO5_D1.on()
            else:
                print('PC is turned off')

        elif msg == b'1':
            print('turn on')
            GPIO5_D1.off()
            GPIO5_D1.on()

def connect_and_subscribe():
    client = MQTTClient(client_id=client_id, server=mqtt_server, port=mqtt_port, user=mqtt_user, password=mqtt_password)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
    return client


def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()


try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

while True:
    try:
        client.check_msg()

        status = analog.read()
        msg = b'OFF' if status== 1024 else b'ON'
        client.publish(topic_pub, msg)
        time.sleep(1) #sec
        wdt.feed() # wathdog
        print(msg)

    except OSError as e:
        restart_and_reconnect()