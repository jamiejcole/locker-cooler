
## Version 0.0.1 ##

## importing needed libraries ##
# (includes RPi.GPIO to control the fan, pyrebase to access firebase and sleep functions)

import RPi.GPIO as GPIO
import pyrebase4
from time import sleep


## Initialising Variables and perfoming configs ##
config = {
  "apiKey": "AIzaSyBvm2pyA-6171fBtjubGKXfQkEDAJi2yWQ",
  "authDomain": "lockerserver-e567b.firebaseapp.com",
  "databaseURL": "https://lockerserver-e567b-default-rtdb.firebaseio.com",
  "storageBucket": "lockerserver-e567b.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()
fanStatus = "False"
init = True
fan = 5

## Setting up the firebase listener and fan control ##
def stream_handler(message):
    global init
    global fan
    if init == True:
        init = False
    elif message["data"] == "False":
        print("Turning off the fan")
        GPIO.output(fan, GPIO.LOW)
    elif message["data"] == "True":
        print("Turning on the fan")
        GPIO.ouput(fan, GPIO.HIGH)


## Starting the listener ##
my_stream = db.stream(stream_handler, stream_id="fanStatus")
