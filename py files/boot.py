# This file is executed on every boot (including wake-boot from deepsleep)

import uos, machine
import gc
import webrepl
webrepl.start()
gc.collect()
import network


ssid = 'eSSID'
password = 'eSSID_PASSWORD'


def do_connect():

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
do_connect()







