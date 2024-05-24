import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
#this will be the number of whatever pin we end up plugging the button into
buttonPin = 37
#setup button as input
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    #state is true or false (1 or 0) depending on if the button is pressed
    state = GPIO.input(buttonPin)
    #prints 1 when the button is not pressed, and 0 when it is
    print(state)

    time.sleep(.5)  
