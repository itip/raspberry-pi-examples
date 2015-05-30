# photo.py 

import picamera

# Put the data and time in the name of the photo.
# This make sure each photo has a unique name and none get overwitten.
name = "photo %s.jpg" % time.strftime("%H:%M:%S")

# Create the camera, set the brightness
camera = picamera.PiCamera()
camera.brightness = 60
camera.capture(name)
print "Photo Taken!!"
