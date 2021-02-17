## Version 0.0.3 ##

## importing needed libraries ##
# (includes RPi.GPIO to control the fan, pyrebase to access firebase and sleep functions)

import RPi.GPIO as GPIO
import pyrebase
from time import sleep
import datetime
import string
import urllib.request


## Initialising Variables and perfoming configs ##
# APIs removed for security.
config = {
  "apiKey": "AIzaSyBvm2pyA-6171fBtjubGKXfQkEDAJi2yWQ",
  "authDomain": "lockerserver-e567b.firebaseapp.com",
  "databaseURL": "https://lockerserver-e567b-default-rtdb.firebaseio.com",
  "storageBucket": "lockerserver-e567b.appspot.com"
}

firebase = pyrebase.initialize_app(config)
ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')

db = firebase.database()
fanStatus = "False"
init = True
fan = 14

GPIO.setmode(DPIO.BCM)
GPIO.setup(channel, GPIO.OUT)

print("\n\n --- STARTING WEBSERVER LISTENER ---\n\n")

## Setting up the firebase listener and fan control ##
def stream_handler(message):
    global init
    global fan
    global ip
    if init == True:
        init = False
    elif message["data"] == "False":
        print("Turning off the fan")
        GPIO.output(fan, GPIO.LOW)

        time = datetime.datetime.now().strftime('%A at %I:%M%p')
        data = {"time": str(time), "ip": str(ip), "value": "fanOFF"}
        db.child("logs").push(data)
    elif message["data"] == "True":
        print("Turning on the fan")
        GPIO.ouput(fan, GPIO.HIGH)

        time = datetime.datetime.now().strftime('%A at %I:%M%p')
        data = {"time": str(time), "ip": str(ip), "value": "fanON"}
        db.child("logs").push(data)


## Starting the listener ##
my_stream = db.stream(stream_handler, stream_id="fanStatus")
