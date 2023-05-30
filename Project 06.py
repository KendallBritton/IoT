import RPi.GPIO as GPIO ## Import GPIO Library
import time             ## Import 'time' library for a delay

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)  ## set output

pwm = GPIO.PWM(18, 100)   ## PWM Frequency
pwm.start(5)

angle1 = 10
duty1 = float(angle1)/10 + 2.5  ## Angle To Duty cycle Converstion

angle2 = 90
duty2 = float(angle2)/10 + 2.5

angle3 = 180
duty3 = float(angle3)/10 + 2.5

angleSolution = 0
dutySolution = float(angleSolution)/10 + 2.5

ck = 0
step = 20
increments = 180/int(step)
while ck <= increments :
    #pwm.ChangeDutyCycle(duty1)
    pwm.ChangeDutyCycle(dutySolution)
    angleSolution = angleSolution + step
    dutySolution = float(angleSolution)/10 + 2.5
    time.sleep(2)
    #pwm.ChangeDutyCycle(duty2)
    #time.sleep(2)
    #pwm.ChangeDutyCycle(duty3)
    #time.sleep(2)
    ck = ck + 1
    
done = False
    
while done == False:
    
    angleSolution = 0
    dutySolution = float(angleSolution)/10 + 2.5
    pwm.ChangeDutyCycle(dutySolution)
    time.sleep(2)
    
    print("Input the amount of degrees to step by (0-180)")
    step = input()
    
    if int(step) == 0:
        done = True
    
    ck = 0
    increments = 180/int(step)
    
    while ck <= increments:
        angleSolution = angleSolution + int(step)
        dutySolution = float(angleSolution)/10 + 2.5
        pwm.ChangeDutyCycle(dutySolution)
        time.sleep(2)
        ck = ck + 1
        
print("Program Ended")
       

time.sleep(1)
GPIO.cleanup()