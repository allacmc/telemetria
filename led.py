import RPi.GPIO as GPIO

pinled = 8

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinled, GPIO.OUT, initial=GPIO.LOW) 
