"""Motor control module for the AGV"""
import sys
import platform

# Try to import RPi.GPIO, fall back to mock if not on Raspberry Pi
try:
    import RPi.GPIO as GPIO
except (RuntimeError, ImportError):
    from hardware.gpio_mock import GPIOMock
    GPIO = GPIOMock()

from config import (
    MOTOR_LEFT_FORWARD, MOTOR_LEFT_BACKWARD,
    MOTOR_RIGHT_FORWARD, MOTOR_RIGHT_BACKWARD,
    MOTOR_ENABLE_LEFT, MOTOR_ENABLE_RIGHT,
    MAX_SPEED
)

class Motors:
    def __init__(self):
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Setup motor pins
        self.pins = [
            MOTOR_LEFT_FORWARD, MOTOR_LEFT_BACKWARD,
            MOTOR_RIGHT_FORWARD, MOTOR_RIGHT_BACKWARD,
            MOTOR_ENABLE_LEFT, MOTOR_ENABLE_RIGHT
        ]

        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)

        # Setup PWM
        self.pwm_left = GPIO.PWM(MOTOR_ENABLE_LEFT, 100)
        self.pwm_right = GPIO.PWM(MOTOR_ENABLE_RIGHT, 100)
        self.pwm_left.start(0)
        self.pwm_right.start(0)

    def set_speeds(self, left_speed, right_speed):
        """Set the speed of both motors"""
        # Ensure speeds are within bounds
        left_speed = max(-MAX_SPEED, min(MAX_SPEED, left_speed))
        right_speed = max(-MAX_SPEED, min(MAX_SPEED, right_speed))

        # Set left motor
        if left_speed >= 0:
            GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
            GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
            self.pwm_left.ChangeDutyCycle(left_speed)
        else:
            GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.HIGH)
            self.pwm_left.ChangeDutyCycle(-left_speed)

        # Set right motor
        if right_speed >= 0:
            GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
            GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
            self.pwm_right.ChangeDutyCycle(right_speed)
        else:
            GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
            self.pwm_right.ChangeDutyCycle(-right_speed)

    def stop(self):
        """Stop both motors"""
        GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        self.pwm_left.ChangeDutyCycle(0)
        self.pwm_right.ChangeDutyCycle(0)

    def cleanup(self):
        """Cleanup GPIO"""
        self.stop()
        self.pwm_left.stop()
        self.pwm_right.stop()
        GPIO.cleanup()