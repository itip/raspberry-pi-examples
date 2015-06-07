# sensor_event_photo.py

import picamera
import RPi.GPIO as GPIO
from time import sleep
import time

sensor = 4

# Set the way pin numbers are read. We want to use the name (Broadcom SOC channel)
# rather than the logical position, e.g. 1st, 2nd, 3rd. See http://raspberrypi.stackexchange.com/a/12967
GPIO.setmode(GPIO.BCM)

# Specify which pin we're going to use. Also add a 10K pull up resistor.
# see http://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

# Set up the camera
camera = picamera.PiCamera()
camera.vflip = True
camera.brightness = 60

# This function will be called when movement is detected
def motion_detected(channel):
   # Take a photo and store it in the current directory
   name = "photo %s.jpg" % time.strftime("%H:%M:%S")
   camera.capture(name)
   print "Photo '%s' Taken!!" % name

# Bouncetime ignores events close together which stops multiple photos being taken.
GPIO.add_event_detect(sensor, GPIO.RISING, callback=motion_detected, bouncetime=200)

# Code will keep running until you press the enter key on your keyboard
close = raw_input("Press ENTER to exit\n")
print "Closing..."
