# Import library to control the General Purpose Input/Output pins (GPIO)
import RPi.GPIO as GPIO
# Import library so we can use the SLEEP command
import time

# List of GPIO pin numbers to use
LED_pins = [23,24,25]
# Tell the GPIO library we are using the breakout board pin numbering system
GPIO.setmode(GPIO.BCM)
# Tell the GPIO library not to issue warnings
GPIO.setwarnings(False)
# Set up the GPIO pins for output
for LED_pin in LED_pins:
    GPIO.setup(LED_pin, GPIO.OUT)

# Infinite loop to blink our LEDs
while True:
    for LED_pin in LED_pins:
        GPIO.output(LED_pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(LED_pin, GPIO.LOW)
        time.sleep(1)