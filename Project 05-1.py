import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24
LED = 12
i = 0

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

GPIO.output(TRIG, False)
print("Calbirating.....")
time.sleep(2)
print("Place the object.....")

try:
    while True:
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
            
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()
            
        pulse_duration = pulse_end - pulse_start
        
        distance = pulse_duration * 17150
        
        distance = round(distance + 1.15, 2)
        
        if distance <= 20 and distance >= 5:
            print("distance:", distance, "cm")
            GPIO.output(LED,False)
            i = 1
            
        if distance > 20 and i == 1:
            print("place the object....")
            i = 0
            
        if distance < 5:
            print("Object too close...")
            GPIO.output(LED, True)
        time.sleep(2)
        
except KeyboardInterrupt:
    GPIO.cleanup()
        
        