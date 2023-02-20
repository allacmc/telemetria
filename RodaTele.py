# python 3.6
import sys
sys.path.insert(1, '/ms5837-python')

import random
import time
import ms5837
import time
from paho.mqtt import client as mqtt_client
import logging
logging.basicConfig(filename = "telemetria.log", level = logging.DEBUG)
import led
import json

#Pegas as informações sobre conexão no arquivo json config.json e coloca dentro das variaveis.
config = json.load(open('/telemetria/config.json', 'r'))
print ("Dados do Arquivo de Configuração - config.json")
print (config['broker'])
print (config['port'])
print (config['topic1'])
print (config['topic2'])
print (config['username'])
print (config['password'])
print (config['tempoEnvio'])
print (config['DensidadeFluido'])

broker = config['broker']
port = config['port']
topic1 = config['topic1']
topic2 = config['topic2']
username = config['username']
password = config['password']
tempoEnvio = config['tempoEnvio']
dFluido = config['DensidadeFluido']

client_id = f'python-mqtt-{random.randint(0, 1000)}'
sensor = ms5837.MS5837_30BA()
sensor.setFluidDensity(dFluido)

try:
    if not sensor.init():
       print("sensor com problema")
       exit(1)
except:
    logging.warning(f"Sensor com problema")

    print("Sensor com problema, verifique a conexão")
    exit(1)

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
def on_publish(client, userdata, rc):
   print("Mensagem chegou no MQTT:", userdata)

def publish(client):
    msg_count = 0
    print("in publish")
    while True:
        led.status(False)
        time.sleep(tempoEnvio)
        try:
            if sensor.read():
               p = sensor.depth()
               t = sensor.temperature()
            else:
               exit(1)
        except:
            print("Erro de leitura no sensor")

        if client.connected_flag:
           result = client.publish(topic1, t)
           result2 = client.publish(topic2, p)
           print(f"Contador:", msg_count, t, p)
           led.status(True)
        msg_count += 1

if __name__ == '__main__':
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_disconnect=on_disconnect
    client.on_publish =on_publish
    client.connected_flag=False
    while True:
        try:
            client.connect(broker, port)
            #client.loop_start()
            client.loop()
            break
        except:
            print("Falha na conexão")
    publish(client)
