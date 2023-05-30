from pyPS4Controller.controller import Controller  #Import controller functionality
import RPi.GPIO as GPIO ## Import GPIO Library
import time             ## Import 'time' library for a delay
import random
import os
import signal

LED_pins = [4, 17, 27, 22, 5, 6, 13, 19]  # Face button are first 4 pins in List, Bumper buttons are last 4 in List

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for pin in LED_pins: 
    GPIO.setup(pin, GPIO.OUT)  ## set output
 
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 100)   ## PWM Frequency
pwm.start(5)

startAngle = 90
startDuty = float(startAngle)/10 + 2.5  ## Angle To Duty cycle Converstion
pwm.ChangeDutyCycle(startDuty)
time.sleep(2)

L1ToggleLED = 0
R1ToggleLED = 0
LightshowToggle = 0

R2LEDPWM = GPIO.PWM(13, 50)
R2LEDPWM.start(0)

L2LEDPWM = GPIO.PWM(19, 50)
L2LEDPWM.start(0)

servoStep = 10

functionLock = 0
functionLockLightshow = 0

TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(27, GPIO.OUT)

GPIO.output(TRIG, False)


class MyController(Controller):
    
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        
    def on_square_press(self):      # LED press/hold control
        global functionLock
        global functionLockLightshow
        
        if functionLock == 0 and functionLockLightshow == 0:
            GPIO.output(4, GPIO.HIGH)
        
        
    def on_square_release(self):    # LED press/hold control
        global functionLock
        global functionLockLightshow
        
        if functionLock == 0 and functionLockLightshow == 0:
            GPIO.output(4, GPIO.LOW)
        
    def on_triangle_press(self):    # LED press/hold control
        global functionLock
        global functionLockLighshow
        
        if functionLock == 0 and functionLockLightshow == 0:
            GPIO.output(17, GPIO.HIGH)
        
    def on_triangle_release(self):  # LED press/hold control
        global functionLock
        global functionLockLightshow
        
        if functionLock == 0 and functionLockLightshow == 0:
            GPIO.output(17, GPIO.LOW)
        
    def on_circle_press(self):      # LED press/hold control
        global functionLock
        global functionLockLightshow
        
        if functionLock == 0 and functionLockLightshow == 0:
            GPIO.output(27, GPIO.HIGH)
        
    def on_circle_release(self):    # LED press/hold control
        global functionLock
        global functionLockLightshow
        
        if functionLock == 0 and functionLockLightshow == 0:
            GPIO.output(27, GPIO.LOW)
        
    def on_x_press(self):           # LED press/hold control
        global functionLock
        global functionLockLightshow
        
        if functionLock == 0 and functionLockLightshow == 0:
            GPIO.output(22, GPIO.HIGH)
        
    def on_x_release(self):         # LED press/hold control
        global functionLock
        global functionLockLightshow
        
        if functionLock == 0 and functionLockLightshow == 0:
            GPIO.output(22, GPIO.LOW)

    def on_L1_press(self):          # LED toggle on/off control
        global functionLock
        global functionLockLightshow
        global L1ToggleLED
        
        if functionLock == 0 and functionLockLightshow == 0:
        
            L1ToggleLED = not L1ToggleLED
            
            if L1ToggleLED == 1:
                GPIO.output(5, GPIO.HIGH)
            elif L1ToggleLED == 0:
                GPIO.output(5, GPIO.LOW)
        
    def on_L1_release(self):        # No operation
        pass

    def on_L2_press(self, value):   # LED variable brightness control
        global functionLock
        global functionLockLightshow
        
        if functionLock == 0 and functionLockLightshow == 0:
        
            if value <= -32431:                           # 0% brightness
                L2LEDPWM.ChangeDutyCycle(0)         
            elif value > -32431 and value <= -25911:      # 10% brightness
                L2LEDPWM.ChangeDutyCycle(10)
            elif value > -25911 and value <= -19391:      # 20% brightness
                L2LEDPWM.ChangeDutyCycle(20)
            elif value > -19391 and value <= -12871:      # 30% brightness
                L2LEDPWM.ChangeDutyCycle(30)
            elif value > -12871 and value <= -6351:       # 40% brightness
                L2LEDPWM.ChangeDutyCycle(40)
            elif value > -6351 and value <= 169:          # 50% brightness
                L2LEDPWM.ChangeDutyCycle(50)
            elif value > 169 and value <= 6689:           # 60% brightness
                L2LEDPWM.ChangeDutyCycle(60)
            elif value > 6689 and value <= 13209:         # 70% brightness
                L2LEDPWM.ChangeDutyCycle(70)
            elif value > 13209 and value <= 19729:        # 80% brightness
                L2LEDPWM.ChangeDutyCycle(80)
            elif value > 19729 and value <= 26249:        # 90% brightness
                L2LEDPWM.ChangeDutyCycle(90)
            elif value > 26249 and value <= 32767:       # 100% brightness
                L2LEDPWM.ChangeDutyCycle(100)
        
    def on_L2_release(self):        # LED variable brightness reset control
        global functionLock
        global functionLockLightshow
        
        if functionLock == 0 and functionLockLightshow == 0:
            L2LEDPWM.ChangeDutyCycle(0)

    def on_L3_press(self):          # No operation
        pass
        
    def on_L3_release(self):       # No operation
        pass

    def on_L3_up(self, value):     # Servo Motor Position Control (Increment Single Degree)
        global startAngle
        servoStep = 1
        global functionLock
        global functionLockLightshow
        global LED_pins
        
        if functionLockLightshow == 0:
        
            if value < 0  or value == -32767:
                if startAngle + servoStep <= 180:
                    if functionLock == 1:
                        for pin in LED_pins[:5]:
                            GPIO.output(pin, GPIO.LOW)
                        functionLock = 0
                    startAngle = startAngle + servoStep
                    startDuty = float(startAngle)/10 + 2.5  ## Angle To Duty cycle Converstion
                    pwm.ChangeDutyCycle(startDuty)
                    print("Servo at {} degrees at step size {}".format(startAngle, servoStep))
                else:
                    functionLock = 1
                    for pin in LED_pins[:5]:
                        GPIO.output(pin, GPIO.LOW)
                    print("CAUTION: Attempt to pass MAX rotation angle of {} degrees at step size of {} degrees".format(startAngle, servoStep))
                    GPIO.output(22, GPIO.HIGH)
        
    def on_L3_down(self, value):   # Servo Motor Position Control (Decrement Single degree)
        global startAngle
        servoStep = 1
        global functionLock
        global functionLockLightshow
        global LED_pins
        
        if functionLockLightshow == 0:
        
            if value > 0 or value == 32767:
                if startAngle - servoStep >= 0:
                    if functionLock == 1:
                        for pin in LED_pins[:5]:
                            GPIO.output(pin, GPIO.LOW)
                        functionLock = 0
                    startAngle = startAngle - servoStep
                    startDuty = float(startAngle)/10 + 2.5  ## Angle To Duty cycle Converstion
                    pwm.ChangeDutyCycle(startDuty)
                    print("Servo at {} degrees at step size {}".format(startAngle, servoStep))
                else:
                    functionLock = 1
                    for pin in LED_pins[:5]:
                        GPIO.output(pin, GPIO.LOW)
                    print("CAUTION: Attempt to pass MIN rotation angle of {} degrees at step size of {} degrees".format(startAngle, servoStep))
                    GPIO.output(17, GPIO.HIGH)
        
    def on_L3_left(self, value):   # No operation
        pass
        
    def on_L3_right(self, value):  # No operation
        pass

    def on_L3_x_at_rest(self):     # No operation
        pass
        
    def on_L3_y_at_rest(self):     # No operation
        pass

    def on_R1_press(self):          # LED toggle on/off control
        global R1ToggleLED
        global functionLock
        global functionLockLightshow
        
        if functionLock == 0 and functionLockLightshow == 0:
        
            R1ToggleLED = not R1ToggleLED
            
            if R1ToggleLED == 1:
                GPIO.output(6, GPIO.HIGH)
            elif R1ToggleLED == 0:
                GPIO.output(6, GPIO.LOW)
        
    def on_R1_release(self):       # No operation
        pass

    def on_R2_press(self, value):  # LED variable brightness control
        global functionLock
        global functionLockLightshow
        
        if functionLock == 0 and functionLockLightshow == 0:
        
            if value <= -32431:                           # 0% brightness
                R2LEDPWM.ChangeDutyCycle(0)         
            elif value > -32431 and value <= -25911:      # 10% brightness
                R2LEDPWM.ChangeDutyCycle(10)
            elif value > -25911 and value <= -19391:      # 20% brightness
                R2LEDPWM.ChangeDutyCycle(20)
            elif value > -19391 and value <= -12871:      # 30% brightness
                R2LEDPWM.ChangeDutyCycle(30)
            elif value > -12871 and value <= -6351:       # 40% brightness
                R2LEDPWM.ChangeDutyCycle(40)
            elif value > -6351 and value <= 169:          # 50% brightness
                R2LEDPWM.ChangeDutyCycle(50)
            elif value > 169 and value <= 6689:           # 60% brightness
                R2LEDPWM.ChangeDutyCycle(60)
            elif value > 6689 and value <= 13209:         # 70% brightness
                R2LEDPWM.ChangeDutyCycle(70)
            elif value > 13209 and value <= 19729:        # 80% brightness
                R2LEDPWM.ChangeDutyCycle(80)
            elif value > 19729 and value <= 26249:        # 90% brightness
                R2LEDPWM.ChangeDutyCycle(90)
            elif value > 26249 and value <= 32767:       # 100% brightness
                R2LEDPWM.ChangeDutyCycle(100)
        
    def on_R2_release(self):       # LED variable brightness reset control
        global functionLock
        global functionLockLightshow
        
        if functionLock == 0 and functionLockLightshow == 0:
            R2LEDPWM.ChangeDutyCycle(0)

    def on_R3_press(self):         # No operation
        pass
        
    def on_R3_release(self):       # No operation
        pass

    def on_R3_up(self, value):      # Servo motor position step size control (increment)
        global servoStep
        global functionLock
        global functionLockLightshow
        
        if functionLock == 0 and functionLockLightshow == 0:
        
            if value == -32767 and servoStep + 5 <= 180:
                servoStep = servoStep + 5
                print("Current step size is {}".format(servoStep))
        
    def on_R3_down(self, value):    # Servo motor position step size control (decrement)
        global servoStep
        global functionLock
        global functionLockLightshow
        
        if functionLock == 0 and functionLockLightshow == 0:
        
            if value == 32767 and servoStep - 5 >= 0:   
                servoStep = servoStep - 5
                print("Current step size is {}".format(servoStep))

    def on_R3_left(self, value):    # No operation
        pass
        
    def on_R3_right(self, value):   # No operation
        pass

    def on_R3_x_at_rest(self):      # No operation
        pass 
        
    def on_R3_y_at_rest(self):      # No operation
        pass
    
    def on_up_arrow_press(self):   # Servo motor position control (increment)
        global startAngle
        global servoStep
        global functionLock
        global functionLockLightshow
        global LED_pins
        
        if functionLockLightshow == 0:
        
            if startAngle + servoStep <= 180:
                if functionLock == 1:
                    for pin in LED_pins[:5]:
                        GPIO.output(pin, GPIO.LOW)
                    functionLock = 0
                startAngle = startAngle + servoStep
                startDuty = float(startAngle)/10 + 2.5  ## Angle To Duty cycle Converstion
                pwm.ChangeDutyCycle(startDuty)
                print("Servo at {} degrees at step size {}".format(startAngle, servoStep))
            else:
                functionLock = 1
                for pin in LED_pins[:5]:
                    GPIO.output(pin, GPIO.LOW)
                print("CAUTION: Attempt to pass MAX rotation angle of {} degrees at step size of {} degrees".format(startAngle, servoStep))
                GPIO.output(22, GPIO.HIGH)
            
    def on_up_down_arrow_release(self):  # No operation
        pass

    def on_down_arrow_press(self): # Servo motor position control (decrement)
        global startAngle
        global servoStep
        global functionLock
        global functionLockLightshow
        global LED_pins
        
        if functionLockLightshow == 0:
        
            if startAngle - servoStep >= 0:
                if functionLock == 1:
                    for pin in LED_pins[:5]:
                        GPIO.output(pin, GPIO.LOW)
                    functionLock = 0
                startAngle = startAngle - servoStep
                startDuty = float(startAngle)/10 + 2.5  ## Angle To Duty cycle Converstion
                pwm.ChangeDutyCycle(startDuty)
                print("Servo at {} degrees at step size {}".format(startAngle, servoStep))
            else:
                functionLock = 1
                for pin in LED_pins[:5]:
                    GPIO.output(pin, GPIO.LOW)
                print("CAUTION: Attempt to pass MIN rotation angle of {} degrees at step size of {} degrees".format(startAngle, servoStep))
                GPIO.output(17, GPIO.HIGH)
        
    def on_left_arrow_press(self): # Enable/perform LED "lightshow"
        global LED_pins
        global L1ToggleLED
        global R1ToggleLED
        global LightshowToggle
        global child
        global functionLock
        global functionLockLightshow
        
        if functionLock == 0:
        
            LightshowToggle = not LightshowToggle
            
            if R2LEDPWM != 0:
                R2LEDPWM.ChangeDutyCycle(0)

            if L2LEDPWM != 0:
                L2LEDPWM.ChangeDutyCycle(0)
                
            if L1ToggleLED != 0:
                L1ToggleLED = 0
                
            if R1ToggleLED != 0:
                R1ToggleLED = 0
            
            i = 0
            LED_time = [1, 0.5, 0.25]
            
            for pins in LED_pins:
                GPIO.output(pins, GPIO.LOW)
            
            if LightshowToggle == 1:
                
                functionLockLightshow = 1
                
                child = os.fork()
                
                if child is 0:
                
                    while LightshowToggle == 1:
                        
                        randomTime = random.choice(LED_time)
                        randomPin = random.choice(LED_pins)
                        if randomPin == 13:
                            R2LEDPWM.ChangeDutyCycle(100)
                        elif randomPin == 19:
                            L2LEDPWM.ChangeDutyCycle(100)
                        else:
                            GPIO.output(randomPin, GPIO.HIGH)
                        time.sleep(randomTime)
                        if randomPin == 13:
                            R2LEDPWM.ChangeDutyCycle(0)
                        elif randomPin == 19:
                            L2LEDPWM.ChangeDutyCycle(0)
                        else:
                            GPIO.output(randomPin, GPIO.LOW)
                        #time.sleep(randomTime)
                    
            elif LightshowToggle == 0:
                
                functionLockLightshow = 0
                os.kill(child, signal.SIGSTOP)
        
    def on_left_right_arrow_release(self):   # No operation
        pass
    
    def on_right_arrow_press(self):          # Ultrasonic Sensor Activation Control
        global functionLock
        global functionLockLightshow
        global R2LEDPWM
        global L2LEDPWM
        global L1ToggleLED
        global R1ToggleLED
        global LED_pins
        
        if functionLock == 0 and functionLockLightshow == 0:
            
            if R2LEDPWM != 0:
                R2LEDPWM.ChangeDutyCycle(0)

            if L2LEDPWM != 0:
                L2LEDPWM.ChangeDutyCycle(0)
                
            if L1ToggleLED != 0:
                L1ToggleLED = 0
                
            if R1ToggleLED != 0:
                R1ToggleLED = 0
            
            for pin in LED_pins:
                GPIO.output(pin, GPIO.LOW)
        
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
                time.sleep(2)
                
            if distance > 20:
                print("No object detected within range")
                time.sleep(2)
                
            if distance < 5:
                print("Object too close...")
                GPIO.output(27, True)
                time.sleep(2)
                GPIO.output(27, False)
        
    def on_options_press(self):              # No operation
        pass
        
    def on_options_release(self):            # No operation
        pass
        
    def on_share_press(self):                # No operation
        pass
        
    def on_share_release(self):              # No operation
        pass
        
    def on_playstation_button_press(self):   # Displays controller button functionality
        print("\nController Button Functionality\n")
        print("Press/Hold LED Controls:")
        print("  - Square    =>  LED 1")
        print("  - Triangle  =>  LED 2")
        print("  - Circle    =>  LED 3")
        print("  - Cross     =>  LED 4")
        print("\nToggle LED Controls:")
        print("  - L1  =>  LED 5")
        print("  - R1  =>  LED 6")
        print("\nVariable LED Brightness Controls:")
        print("  - R2  =>  LED 7")
        print("  - L2  =>  LED 8")
        print("\nServo Motor Position Controls:")
        print("  - Up Arrow D-Pad          =>  Increment Servo Position By Specified Step Amount")
        print("  - Down Arrow D-Pad        =>  Decrement Servo Position By Specified Step Amount")
        print("  - Up On Left Joystick     =>  Increment Servo Position By 1 Degree (Continuous)")
        print("  - Down On Left Joystick   =>  Decrement Servo Position By 1 Degree (Continuous)")
        print("  - Up on Right Joystick    =>  Increment Servo Step Size by 5 Degrees")
        print("  - Down on Right Joystick  =>  Decrement Servo Step Size by 5 Degrees")
        print("\nToggle On/Off LED Lightshow:")
        print("  - Left Arrow D-Pad  =>  Perform Lightshow")
        print("\nActivate Ultrasonic Sensor:")
        print("  - Right Arrow D-Pad  =>  Read Object Distance Through Ultrasonic\n")
        
    def on_playstation_button_release(self):   # No operation
        pass
        
controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen(timeout=60)