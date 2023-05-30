# Import library to control the General Purpose Input/Output pins (GPIO)
import RPi.GPIO as GPIO
# Import library so we can use the SLEEP command
import time

# List of GPIO pin numbers
LED_pins = [23,24,25,12,16,21]
# Tell the GPIO library we are using the breakout board pin numbering system
GPIO.setmode(GPIO.BCM)
# Tell the GPIO library not to issue warnings
GPIO.setwarnings(False)
# Create empty list to store PWM objects
pwm_list = []
# Set up the GPIO pins for output, create PWM objects and place them in pwm_list
for LED_pin in LED_pins:
    GPIO.setup(LED_pin, GPIO.OUT)
    pwm_list.append( GPIO.PWM(LED_pin, 50) )


# Infinite loop to fade our led in sequence
while True:
    for pwm in pwm_list: # for each PWM object in our pwm_list
        pwm.start(0) # start with 0 brightness
        for i in range(0,100): # loop from 0 --> 100% brightness
            pwm.ChangeDutyCycle(i)
            time.sleep(0.05)
        for i in range(100,0,-1): # loop from 100 --> 0% brightness
            pwm.ChangeDutyCycle(i)
            time.sleep(0.05)
        