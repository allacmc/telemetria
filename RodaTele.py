# python 3.6
import sys
sys.path.insert(1, '/ms5837-python')

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import random
import time
import ms5837
import time
from paho.mqtt import client as mqtt_client
import logging
logging.basicConfig(filename = "telemetria.log", level = logging.DEBUG)
import led

sensor = ms5837.MS5837_30BA()
broker = '192.168.1.210'
port = 1883
topic1 = "belov/barco01/tele01/temperatura"
topic2 = "belov/barco01/tele01/profundidade"
pinled = 8
tempoEnvio = 500/1000

client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'CasaPendotiba'
password = 'Casa12345678@#'

#Prepara os pinos fisicos do Led
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinled, GPIO.OUT, initial=GPIO.LOW) 

try:
    if not sensor.init():
       print("sensor com problema")
       exit(1)
except:
    logging.warning(f"Sensor com problema")
    print("Sensor com problema, verifique a conexão")
    exit(1)
    
def led(status):
    if status == True:
       GPIO.output(pinled, GPIO.HIGH) # Turn on
    else:
       GPIO.output(pinled, GPIO.LOW) # Turn off
    
def on_disconnect(client, userdata, rc):
   print("client disconnected ok")
   client.connected_flag=False
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.connected_flag=True
    else:
        print("Failed to connect, return code %d\n", rc)
        client.connected_flag=False
def connect_mqtt():
    client.connect(broker, port)
    return client

def publish(client):
    msg_count = 0
    print("in publish")
    while True:
        #GPIO.output(pinled, GPIO.LOW) # Turn off
        led(False)
        time.sleep(tempoEnvio)
        if sensor.read():
           p = sensor.depth()
           t = sensor.temperature()
        else:
           exit(1)
        
        if client.connected_flag: 
           result = client.publish(topic1, t)
           result2 = client.publish(topic2, p)
           status = result[0]
           if status == 0:
              print(f"Enviando dados para o Broker...", t, p)
              #GPIO.output(pinled, GPIO.HIGH) # Turn on
              led(True)  
              print(f"Contador:", msg_count)
           else:
              print(f"Failed to send message to topic {topic}")
        msg_count += 1
        

def run():
    
    publish(client)


if __name__ == '__main__':
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_disconnect=on_disconnect
    client.connected_flag=False
    while True:
        try:
            client.connect(broker, port)
            client.loop_start()
            break

        except:
            print("connection failed")
        time.sleep(5)
   
    publish(client)
    print("end")
