from machine import Pin
import motor
from time import sleep, ticks_ms
import servo

last_motor_ticks = 0
motor_state = 0
def motor_loop():
    global last_motor_ticks, motor_state
    if (ticks_ms() - last_motor_ticks) >= 500:
        if motor_state == 0:
            motor.move(motor.FORWARD, 50)
        elif motor_state == 1:
            motor.move(motor.FORWARD, 100)
        elif motor_state == 2:
            motor.move(motor.BACKWARD, 50)
        elif motor_state == 3:
            motor.move(motor.BACKWARD, 100)
        elif motor_state == 4:
            motor.move(motor.TURN_LEFT, 100)
        elif motor_state == 5:
            motor.move(motor.TURN_RIGHT, 100)
        elif motor_state == 6:
            motor.stop()
        motor_state = motor_state + 1
        if motor_state > 6:
            motor_state = 0
        last_motor_ticks = ticks_ms()

last_led_ticks = 0
led_state = 0
leds = [ 10, 11, 12, 26, 27 ]
def led_loop():
    global last_led_ticks, led_state
    if (ticks_ms() - last_led_ticks) >= 100:
        Pin(leds[4 if led_state == 0 else led_state - 1], Pin.OUT).value(0)
        Pin(leds[led_state], Pin.OUT).value(1)
        led_state = led_state + 1
        if led_state > 4:
            led_state = 0
        last_led_ticks = ticks_ms()


last_servo_ticks = 0
servo_state = 0
def servo_loop():
    global last_servo_ticks, servo_state
    if (ticks_ms() - last_servo_ticks) >= 1000:
        if servo_state == 0:
            servo.angle(servo.SV1, 0)
            servo.angle(servo.SV2, 180)
            servo.angle(servo.SV3, 180)
        elif servo_state == 1:
            servo.angle(servo.SV1, 90)
            servo.angle(servo.SV2, 90)
            servo.angle(servo.SV3, 0)
        elif servo_state == 2:
            servo.angle(servo.SV1, 180)
            servo.angle(servo.SV2, 0)
            servo.angle(servo.SV3, 90)
        servo_state = servo_state + 1
        if servo_state > 2:
            servo_state = 0
        last_servo_ticks = ticks_ms()

while True:
    motor_loop()
    led_loop()
    servo_loop()
    sleep(0.1)
