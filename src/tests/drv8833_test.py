from machine import Pin, PWM
from drv8833 import DRV8833 # ../lib/drv8833.py
from time import sleep

Pin("LED").on()
sleep(1)
Pin("LED").off()

# NOTE: feel free to play with the frequency value! The frequency (how many PWM cycles per second
# sent to the DRV pins) changes the behavior of the connected motors, especially at low throttle
# values. (based on very brief testing) We recommend values no lower than 1,000 and no higher than
# 200,000. 40,000 is a good default.
frequency = 40_000

# Make sure to set the correct pins!
r_a_in1 = PWM(Pin(10, Pin.OUT))
r_a_in2 = PWM(Pin(11, Pin.OUT))
r_a_in1.freq(frequency)
r_a_in2.freq(frequency)			

r_b_in1 = PWM(Pin(14, Pin.OUT))
r_b_in2 = PWM(Pin(15, Pin.OUT))
r_b_in1.freq(frequency)
r_b_in2.freq(frequency)

l_a_in1 = PWM(Pin(21, Pin.OUT))
l_a_in2 = PWM(Pin(20, Pin.OUT))
l_a_in1.freq(frequency)
l_a_in2.freq(frequency)

l_b_in1 = PWM(Pin(17, Pin.OUT))
l_b_in2 = PWM(Pin(16, Pin.OUT))
l_b_in1.freq(frequency)
l_b_in2.freq(frequency)

drv_left = DRV8833(l_a_in1, l_a_in2, l_b_in1, l_b_in2) 
drv_right = DRV8833(r_a_in1, r_a_in2, r_b_in1, r_b_in2)

MAX_THROTTLE = 0.9#0.99  # maximum throttle
sleep_hold = 8.0
STEP_SIZE = 0.05
STEPS = int(MAX_THROTTLE/STEP_SIZE)

try:
    while True:
        for i in range(STEPS + 1):
            throttle = i / STEPS * MAX_THROTTLE
            drv_left.throttle_a(throttle)
            drv_left.throttle_b(throttle)
            drv_right.throttle_a(throttle)
            drv_right.throttle_b(throttle)
            
            sleep(0.05)  # small delay to avoid busy looping
            print("Speed:", throttle)
        
        sleep(sleep_hold)
        
        for i in range(STEPS, -1, -1):
            throttle = i / STEPS * MAX_THROTTLE
            drv_left.throttle_a(throttle)
            drv_left.throttle_b(throttle)
            drv_right.throttle_a(throttle)
            drv_right.throttle_b(throttle)
            sleep(0.05)
            print("Speed:", throttle)

        sleep(sleep_hold)

except KeyboardInterrupt:
    drv_right.stop_a()
    drv_right.stop_b()
    drv_left.stop_a()
    drv_left.stop_b()
    
    drv_right.deinit()
    drv_left.deinit()
