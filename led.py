import RPi.GPIO as GPIO

pinled = 8

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinled, GPIO.OUT, initial=GPIO.LOW) 

def status(status):
    if status == True:
       GPIO.output(pinled, GPIO.HIGH) # Turn on
       #print("HIGH")
    else:
       GPIO.output(pinled, GPIO.LOW) # Turn off
       #print("low")
