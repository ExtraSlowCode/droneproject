from machine import PWM, Pin, I2C
import MPU6050 
from drv8833 import DRV8833 # ../lib/drv8833.py
from PID import PID
import time
import math


# https://simple.wikipedia.org/wiki/Pitch,_yaw,_and_roll
# https://github.com/gastmaier/micropython-simple-pid

#-----initalizitation parameters------
i2c = I2C(1, sda=Pin(14), scl=Pin(15)) #Accelerometer interface  PINS ARE PLACEHOLDERS
mpu = MPU6050.MPU6050(i2c)

roll_pid = PID(1, 0.1, 0.05, setpoint=15, scale='ms')
pitch_pid = PID(1, 0.1, 0.05, setpoint=15, scale='ms')
roll_pid.output_limits = (-20, 20)
pitch_pid.output_limits = (-20, 20)

baseline_throttle = 0
roll = 0
pitch = 0
yaw = 0
roll =0
dtTimer = 0


#------   motor pins    -------------
frequency = 40_000
MAX_THROTTLE = 1.0 

#PINS ARE PLACEHOLDERS!
frontrightin1 = PWM(Pin(15, Pin.OUT))
frontrightin2 = PWM(Pin(14, Pin.OUT))
backrightin1 = PWM(Pin(13, Pin.OUT))
backrightin2 = PWM(Pin(12, Pin.OUT))

#PINS ARE PLACEHOLDERS!
frontleftin1 = PWM(Pin(15, Pin.OUT))
frontleftin2 = PWM(Pin(14, Pin.OUT))
backleftin1 = PWM(Pin(13, Pin.OUT))
backleftin2 = PWM(Pin(12, Pin.OUT))

frontrightin1.freq(frequency)
frontrightin2.freq(frequency)
backrightin1.freq(frequency)
backrightin2.freq(frequency)

frontleftin1.freq(frequency)
frontleftin2.freq(frequency)
backleftin1.freq(frequency)
backleftin2.freq(frequency)

# Clockwise turning engines: Front left, Back right
# Counter-clockwise turning engines; Front Right, Back left

drv_1 = DRV8833(frontrightin1, frontrightin2, backrightin1, backrightin2)
drv_2 = DRV8833(frontleftin1, frontleftin2, backleftin1, backleftin2)

#---------------------------------------
def stop_all():
    drv_1.throttle_a(0)
    drv_1.throttle_b(0)
    drv_2.throttle_a(0)
    drv_2.throttle_b(0)

#source:
# https://www.youtube.com/watch?v=AN3yxIBAxTA
# https://youtu.be/IfL3HJowdms?si=nn2BttNZ0HaCdJus
# src\tests\drone_physics\PIDBalancing.png

def increaseThrottle(baseline_throttle):
    baseline_throttle += 0.1
    drv_1.throttle_a(baseline_throttle)
    drv_1.throttle_b(baseline_throttle)
    drv_2.throttle_a(baseline_throttle)
    drv_2.throttle_b(baseline_throttle)
    stabilize()

def decreaseThrottle(baseline_throttle):
    baseline_throttle -= 0.1
    drv_1.throttle_a(baseline_throttle)
    drv_1.throttle_b(baseline_throttle)
    drv_2.throttle_a(baseline_throttle)
    drv_2.throttle_b(baseline_throttle)
    stabilize()

# src\tests\drone_physics\pitch.png
# change pitch axis 
def pitchForward(baseline_throttle):
    stabilize() # set drone to 0.0.0
    pitch_error = 10
    pitch_pid.setpoint = 15
    while abs(pitch_error) > 2: # Small allowed error margin
        roll,pitch = readSensorsComplementary()
        pitch_error = roll_pid.setpoint - roll
        pitchCorrection = pitch_pid(pitch)
        front = baseline_throttle - pitchCorrection
        back = baseline_throttle + pitchCorrection

        drv_1.throttle_a(front)  # Front Right
        drv_2.throttle_a(front)  # Front Left
        drv_1.throttle_b(back)  # Back Right
        drv_2.throttle_b(back)  # Back Left


def pitchBackward(baseline_throttle):
    stabilize() # set drone to 0.0.0
    roll_error, pitch_error = 10
    pitch_pid.setpoint = 15
    while abs(pitch_error) > 2: # Small allowed error margin
        roll,pitch = readSensorsComplementary()
        pitch_error = roll_pid.setpoint - roll
        pitchCorrection = pitch_pid(pitch)
        front = baseline_throttle +  pitchCorrection
        back = baseline_throttle - pitchCorrection

        drv_1.throttle_a(front)  # Front Right
        drv_2.throttle_a(front)  # Front Left
        drv_1.throttle_b(back)  # Back Right
        drv_2.throttle_b(back)  # Back Left


def rollRight(baseline_throttle):
    stabilize() # set drone to 0.0.0
    roll_error = 10
    roll_pid.setpoint = 15
    pitch_pid.setpoint = 0
    while abs(roll_error) > 2: # Small allowed error margin
        roll,pitch = readSensorsComplementary()
        roll_error = roll_pid.setpoint - roll
        rollCorrection = roll_pid(roll)

        left = baseline_throttle + rollCorrection
        right = baseline_throttle - rollCorrection

        drv_1.throttle_a(right)  # Front Right
        drv_1.throttle_b(right)  # Back Right
        drv_2.throttle_a(left)  # Front Left
        drv_2.throttle_b(left)  # Back Left

def rollLeft(baseline_throttle):
    stabilize() # set drone to 0.0.0
    roll_error = 10
    roll_pid.setpoint = 15
    pitch_pid.setpoint = 0
    while abs(roll_error) > 2: # Small allowed error margin
        roll,pitch = readSensorsComplementary()
        roll_error = roll_pid.setpoint - roll
        rollval = roll_pid(roll)

        left = baseline_throttle - rollval
        right = baseline_throttle + rollval

        drv_1.throttle_a(right)  # Front Right
        drv_1.throttle_b(right)  # Back Right
        drv_2.throttle_a(left)  # Front Left
        drv_2.throttle_b(left)  # Back Left

def stabilize(baseline_throttle):
    roll_error, pitch_error = 10
    roll_pid.setpoint = 15
    pitch_pid.setpoint = 0
    while abs(roll_error) > 2 and abs(pitch_error) > 2: # Small allowed error margin
        roll,pitch = readSensorsComplementary()
        roll_error = roll_pid.setpoint - roll
        pitch_error = pitch_pid.setpoint - pitch
        rollCorrection = roll_pid(roll)
        pitchCorrection = pitch_pid(pitch)

        # >0 angle roll = leans clockwise < angle leans counterclockwise
        # >0 angle pitch = leans counterclockwsise < angle leans clockwise
        if roll > 0 and pitch > 0:
            back_right += abs(rollCorrection) + abs(pitchCorrection)
        elif roll < 0 and pitch > 0:
            back_left += abs(rollCorrection) + abs(pitchCorrection)
        elif roll > 0 and pitch < 0:
            front_right += abs(rollCorrection) + abs(pitchCorrection)
        elif roll < 0 and pitch < 0:
            front_left += abs(rollCorrection) + abs(pitchCorrection)

        drv_1.throttle_a(baseline_throttle + front_right)  # Front Right
        drv_1.throttle_b(baseline_throttle + back_right)  # Back Right
        drv_2.throttle_a(baseline_throttle + front_left)  # Front Left
        drv_2.throttle_b(baseline_throttle + back_left)  # Back Left

   
#-stabilisaztion_
  #source:
 # https://github.com/MarkSherstan/MPU-6050-9250-I2C-CompFilter/blob/master/RPi/main.py
def readSensorsComplementary():  
    tau = 0.98
    #measured angular rate
   
    gx, gy, gz = mpu.read_gyro_data() 
    ax, ay, az = mpu.read_accel_data()

    dt = time.time() - dtTimer
    dtTimer = time.time()
    
    accPitch = math.degrees(math.atan2(ay, az))
    accRoll = math.degrees(math.atan2(ax, az))

    # Gyro integration angle
    gyroRoll -= gy * dt
    gyroPitch += gx * dt
    gyroYaw += gz * dt
    yaw = gyroYaw

     # Comp filter
    roll = (tau)*(roll - gy*dt) + (1-tau)*(accRoll)
    pitch = (tau)*(pitch + gx*dt) + (1-tau)*(accPitch)
    return roll,pitch
#--------------------------------------------------

while True:
    key = read_input()

    if key = "l":
        stop_all()
    if key == "w":
        increaseThrottle()
    elif key == "s":
        decreaseThrottle()
    elif key == "a":
        rollLeft()
    elif key == "d":
        rollRight()
    elif key == "up":
        pitchForward()
    elif key == "down":
        stabilize()
         
    sleep(1) #long delay during testing phase


