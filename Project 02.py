# Import library to control the General-Purpose Input/output pins (GPIO)
import RPi.GPIO as GPIO
# Import library so we can use the SLEEP command
import time

# Variable for the GPIO pin number
LED_pin = 24
# Tell the GPIO library we are using the breakout board pin numbering system
GPIO.setmode(GPIO.BCM)
# Tell the GPIO library not to issue warnings
GPIO.setwarnings(False)

# Set up the GPIO pin for output
GPIO.setup(LED_pin, GPIO.OUT)
# Creates software PWM on LED_pin running at 50Hz
pwm = GPIO.PWM(LED_pin, 50)

increment = 2
brightness = 10
pwm.start(brightness)
# Infinite loop to fade our led
while True:
    pwm.ChangeDutyCycle(brightness)
    if ((brightness >= 100) or (brightness <= 0)):
        increment = -increment
    brightness = brightness + increment
    time.sleep(0.1)