import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
#Prepara os pinos fisicos do Led
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinled, GPIO.OUT, initial=GPIO.LOW) 

