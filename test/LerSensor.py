# importing the sys module
import sys

# inserting the mod.py directory at
# position 1 in sys.path
sys.path.insert(1, '/ms5837-python')



import ms5837
import time

sensor = ms5837.MS5837_30BA() # Default I2C bus is 1 (Raspberry Pi 3)

# We must initialize the sensor before reading it
if not sensor.init():
        print("Sensor could not be initialized")
        exit(1)

# Print readings
while True:
        if sensor.read():
                print(
		     ("Pressão:%0.3f Temperatura: %0.2f, Profundidade:%0.2f ") % (
                sensor.pressure(ms5837.UNITS_psi), 
                sensor.temperature(),
		sensor.depth())
		     )
        else:
                print("Sensor read failed!")
                exit(1)
