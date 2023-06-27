## This file is uploaded to the microcontroller as code.py
import neopixel
import board
import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from time import time,sleep
import json
from analogio import AnalogOut

pixel = neopixel.NeoPixel(board.NEOPIXEL,1)
pixel.fill([0, 0, 255])
a_out = AnalogOut(board.A0)


try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    pixel.fill([255, 0, 0])
    raise

print("Connecting to %s" % secrets["SSID"])
wifi.radio.connect(secrets["SSID"], secrets["WPA"])
print("Connected to %s!" % secrets["SSID"])

ka_topic = f"pressure_node/{secrets['name']}/keep_alive"
destination = f"pressure_node/{secrets['name']}/pressure_cmd"
err_topic = f"pressure_node/{secrets['name']}/error"

def message(client, topic, message):
    try: 
        
        print(message)
        data = json.loads(message) #expects {"bit": int ,"rgb": [R,G,B]}
        pixel.fill([0, 0, 0])
        sleep(0.1)
        bit = int(data['bit']) * 64 # bit received is a 10 bit integer
        a_out.value = bit
        pixel.fill(data['rgb'])

    except Exception as E:
        pixel.fill([255, 0, 0])
        client.publish(err_topic,str(E))

pool = socketpool.SocketPool(wifi.radio)
mqtt_client = MQTT.MQTT(broker=secrets["MQTT"],port=1883,socket_pool=pool)
mqtt_client.on_message = message

mqtt_client.connect()
mqtt_client.subscribe(destination)

ticks = 0
tocks = 200

while True:
    ticks+=1
    if (ticks > tocks):
        ticks = 0
        mqtt_client.publish(ka_topic,"Status: Available")
    mqtt_client.loop()
    sleep(.01)
