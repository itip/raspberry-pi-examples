import json,httplib
import os
import picamera
import RPi.GPIO as GPIO
import time

from os import listdir
from os.path import isfile, join
from time import sleep

parse_application_key = "<APPLICATION_KEY>"
rest_api_key = "<REST_API_KEY>"


# Utility function which checks whether the given file is a photo
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    filename = filename.lower()
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# Upload photos to Parse
def upload_photos():
    # Search 'photos' directory for photos which haven't been uploaded
    for file_name in listdir("photos"):
        if isfile(join("photos",file_name)):
            if allowed_file(file_name):
                print("Uploading %s" % file_name)

                file_path = join("photos",file_name)

                connection = httplib.HTTPSConnection('api.parse.com', 443)
                connection.connect()

                # Upload file to Parse

                parse_url_path = "/1/files/%s" % file_name

                connection.request('POST', parse_url_path, open(file_path, 'rb').read(), {
                       "X-Parse-Application-Id": parse_application_key,
                       "X-Parse-REST-API-Key": rest_api_key,
                       "Content-Type": "image/png"
                     })
                result = json.loads(connection.getresponse().read())


                # Check file uploaded
                if 'name' not in result:
                    print ("An error ocurred when uploading the file. Will try again later.")
                    continue


                # Create a new "Alert" object in Parse
                parse_file_name = result['name']

                connection.request('POST', '/1/classes/Alert', json.dumps({
                   "name": file_name,
                   "picture": {
                     "name": parse_file_name,
                     "__type": "File"
                   }
                 }), {
                   "X-Parse-Application-Id": parse_application_key,
                   "X-Parse-REST-API-Key": rest_api_key,
                   "Content-Type": "application/json"
                 })
                result = json.loads(connection.getresponse().read())

                if 'objectId' not in result:
                    print ("An error ocurred when creating Alert object. Will try again later.")
                    continue

                # Success. Everything uploaded. Move file to 'uploaded' folder so we don't upload again.
                if not os.path.exists("uploaded"):
                    os.makedirs("uploaded")

                uploaded_path = join("uploaded", file_name)
                os.rename(file_path, uploaded_path)

                print("Finished uploading %s\n" % file_name)


# This function will be called when movement is detected
def motion_detected(channel):
   # Take a photo and store it in the current directory
   name = "photos/photo_%s.jpg" % time.strftime("%H-%M-%S")
   camera.capture(name)
   print "Photo '%s' Taken!!" % name
   upload_photos()



# Set up camera and sensor. See previous examples for explanations
sensor = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

camera = picamera.PiCamera()
camera.vflip = True
camera.brightness = 60

GPIO.add_event_detect(sensor, GPIO.RISING, callback=motion_detected, bouncetime=200)

# Code will keep running until you press the enter key on your keyboard
close = raw_input("Press ENTER to exit\n")
print "Closing.."
