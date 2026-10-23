import machine
import MPU6050 
from drv8833 import DRV8833 # ../lib/drv8833.py
from time import sleep

i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15)) #Accelerometer interface
mpu = MPU6050.MPU6050(i2c)


# motor pins
frequency = 40_000
MAX_THROTTLE = 1.0 

# Make sure to set the correct pins!
frontrightin1 = PWM(Pin(15, Pin.OUT))
frontrightin2 = PWM(Pin(14, Pin.OUT))
backrightin1 = PWM(Pin(13, Pin.OUT))
backrightin2 = PWM(Pin(12, Pin.OUT))

# Make sure to set the correct pins!
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

drv_1 = DRV8833(frontrightin1, frontrightin2, backrightin1, backrightin2)
drv_2 = DRV8833(frontleftin1, frontleftin2, backleftin1, backleftin2)

targetangle = 0
maxleanangle = 15

def turn():
    if ( "right") 
        drv_1.throttle_b(MAX_THROTTLE)
        drv_2.throttle_b(MAX_THROTTLE)
        
        drv_1.throttle_a(MAX_THROTTLE  * 0.8)
        drv_2.throttle_a(MAX_THROTTLE *0.8)
    else if ("left")
     drv_1.throttle_b(MAX_THROTTLE)
     drv_2.throttle_b(MAX_THROTTLE)
     drv_1.throttle_a(MAX_THROTTLE  * 0.8)
     drv_2.throttle_a(MAX_THROTTLE *0.8)
     
       

def forward():
    drv_1.throttle_b(MAX_THROTTLE)
    drv_2.throttle_b(MAX_THROTTLE)
    
    drv_1.throttle_a(MAX_THROTTLE  * 0.8)
     drv_2.throttle_a(MAX_THROTTLE *0.8)
     

def check_balance();

    gyro = mpu.read_gyro_data()
    accel = mpu.read_accel_data()
    while (currentangle >maxleangle) {
        #increase mot power on some side
        # read angle agian
        
}
    
while True:
    var = 0

    # lift
    while var < MAX_THROTTLE:
        var += 0.1
        drv_1.throttle_a(var)
        drv_1.throttle_b(var)
        drv_2.throttle_a(var)
        drv_2.throttle_b(var)
        time.sleep(0.2)
    #hover
    time.sleep(4)

    # land
    while var > 0:
        var -= 0.1

        drv_1.throttle_a(var)
        drv_1.throttle_b(var)
        drv_2.throttle_a(var)
        drv_2.throttle_b(var)
        
        time.sleep(0.2)