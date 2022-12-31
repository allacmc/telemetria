# python 3.6
import sys
sys.path.insert(1, '/ms5837-python')


import random
import time
import ms5837
import time
from paho.mqtt import client as mqtt_client
import paho.mqtt.publish as publish
from datetime import datetime


sensor = ms5837.MS5837_30BA()
broker = '192.168.1.201'
port = 1883
topic1 = "belov/barco01/tele01/temperatura"
topic2 = "belov/barco01/tele01/profundidade"
topic3 = "belov/barco01/tele01/pressao"

client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'Casa'
password = '12345678'


if not sensor.init():
        print("Sensor could not be initialized")
        exit(1)


def run():
    client = connect_mqtt()
    #----------------------------------------
    #client.loop_start()
    #print("Conectando no broker....")

    #while not client.connected_flag and not client.bad_connection_flag:
    #    print("Aguardando rede...")
    #    time.sleep(1)
    #if client.bad_connection_flag:
    #    print("Problema na conexão")
    #    client.loop_stop()
    #    sys.exit()
#    #---------------------------------------

    publish(client)


def connect_mqtt():
    mqtt_client.Client.connected_flag = False
    mqtt_client.Client.bad_connection_flag = False
    client = mqtt_client.Client(client_id) #Cria o objeto "client"
    client.username_pw_set(username, password)
    client.on_connect = on_connect        #Associa o evento On-Connect
    client.on_disconnect = on_disconnect  #Associa o evento On-Disconnect

    #client.connect(broker, port) #Connecta de fato.
    client.connect(broker, port)
    client.loop_start()

    return client

def on_connect(client, userdata, flags, rc):
    if rc == 0:
       client.connected_flag=True #set flag
       print("Conectado ao Broker Code=", rc)
    else:
       print("Failed to connect, return code %d\n", rc)
       client.bad_connection_flag=True

def on_disconnect(client, userdata, rc):
    logging.info("Desconectado motivo =  "  +str(rc))
    client.connected_flag=False
    client.disconnect_flag=True


def publish(client):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    msg_count = 0
    while True:
        time.sleep(1)

        if sensor.read():
            p = sensor.depth()
            t = sensor.temperature()
            y = sensor.pressure()
            y = y / 1000
        else:
            exit(1)

        result = client.publish(topic1, t)
        result2 = client.publish(topic2, p)
        result3 = client.publish(topic3, y)

        status = result[0]
        if status == 0:
            print("Publicação:", msg_count)
            print(f"Resultado", result[0])
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1



if __name__ == '__main__':
    run()
