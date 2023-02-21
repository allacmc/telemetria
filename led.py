import RPi.GPIO as GPIO
import json

config = json.load(open('/telemetria/config.json', 'r'))
pinLed = config['pinLed']

#pinled = 16 #pino que está plugado o led

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinLed, GPIO.OUT, initial=GPIO.LOW) 

def status(status):


    if status == True:
       GPIO.output(pinLed, GPIO.HIGH) # Turn on
       #print("HIGH")
    else:
       GPIO.output(pinLed, GPIO.LOW) # Turn off
       #print("low")
