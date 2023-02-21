import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

pin_led = 16

GPIO.setup(pin_led, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)


while True: # Run forever
 GPIO.output(pin_led, GPIO.HIGH) # Turn on
 sleep(1) # Sleep for 1 second
 GPIO.output(pin_led, GPIO.LOW) # Turn off
 sleep(1) # Sleep for 1 second
