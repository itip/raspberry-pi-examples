# sensor_event.py

import RPi.GPIO as GPIO
from time import sleep

sensor = 4

# Set the way pin numbers are read. We want to use the name (Broadcom SOC channel)
# rather than the logical position, e.g. 1st, 2nd, 3rd. See http://raspberrypi.stackexchange.com/a/12967
GPIO.setmode(GPIO.BCM)

# Specify which pin we're going to use. Also add a 10K pull down resistor.
# see http://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

# This function will be called when movement is detected
def motion_detected(channel):
   print("Motion detected")

# Detect rise
GPIO.add_event_detect(sensor, GPIO.RISING, callback=motion_detected)

# Code will keep running until you press the enter key on your keyboard
close = raw_input("Press ENTER to exit\n")
print "Closing..."
