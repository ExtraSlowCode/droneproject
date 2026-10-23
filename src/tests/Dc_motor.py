from machine import Pin
from time import sleep

# Motor pins
motor1 = Pin(13, Pin.OUT)
motor2 = Pin(14, Pin.OUT)

try:
    print("--Started--")
    while True:
        motor1.value(1)
        motor2.value(0)
        print("Turning right")
        sleep(4)
        
        motor1.value(0)
        motor2.value(1)
        print("Turning left")
        sleep(4)
except Exception as e:
    print(e)