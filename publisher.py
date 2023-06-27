import json
import paho.mqtt.client as mqtt
from threading import Event, Thread
from time import sleep
import secrets

def mqtt_publish(host, port, destination, payload):
    client = mqtt.Client()
    client.connect(
            host=host,
            port=port,
            keepalive=3600
        )
    client.loop_start()  
    print(destination)   
    mqtt_message = client.publish(
        topic=destination,
        payload=json.dumps(payload)
    )
    print(mqtt_message)


def main():
    HOST = secrets["SSID"]
    PORT = secrets["PORT"]

    ## ONLY Change these ##
    destination = "pressure_node/my_led_node/pressure_cmd"
    payload = {"bit": 950,  # 0<=bit<=1023
               "rgb": [0,255,0]}
    ####-----------------##
    for i in range(5):
        mqtt_publish(HOST, PORT, destination, payload)
        sleep(0.4)
    

if __name__ == '__main__':
    main()