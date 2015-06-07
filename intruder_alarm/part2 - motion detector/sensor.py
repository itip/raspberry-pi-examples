# sensor.py

import RPi.GPIO as GPIO
import time

sensor = 4

# Set the way pin numbers are read. We want to use the name (Broadcom SOC channel)
# rather than the logical position, e.g. 1st, 2nd, 3rd. See http://raspberrypi.stackexchange.com/a/12967
GPIO.setmode(GPIO.BCM)

# Specify which pin we're going to use. Also add a 10K pull up resistor.
# see http://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_UP)

# Create an infinite loop which repeatedly checks the input sensor/
while True:
   time.sleep(0.1)
   value = GPIO.input(sensor)
   print("GPIO pin %s is %s" % (sensor, value))
