import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)
while True:
    GPIO.output(24, True)
    time.sleep(1)
    GPIO.output(24, False)
    time.sleep(1)