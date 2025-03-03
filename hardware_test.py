"""
Hardware test script for AGV components
Run this script to test motors and camera individually
"""
import time
import sys
try:
    import RPi.GPIO as GPIO
except (RuntimeError, ImportError):
    print("Error: This script must be run on a Raspberry Pi")
    sys.exit(1)

from config import (
    MOTOR_LEFT_FORWARD, MOTOR_LEFT_BACKWARD,
    MOTOR_RIGHT_FORWARD, MOTOR_RIGHT_BACKWARD,
    MOTOR_ENABLE_LEFT, MOTOR_ENABLE_RIGHT
)

def test_motors():
    """Test motor connections"""
    print("\nTesting motors...")
    
    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Setup motor pins
    pins = [
        MOTOR_LEFT_FORWARD, MOTOR_LEFT_BACKWARD,
        MOTOR_RIGHT_FORWARD, MOTOR_RIGHT_BACKWARD,
        MOTOR_ENABLE_LEFT, MOTOR_ENABLE_RIGHT
    ]
    
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        
    # Setup PWM
    pwm_left = GPIO.PWM(MOTOR_ENABLE_LEFT, 100)
    pwm_right = GPIO.PWM(MOTOR_ENABLE_RIGHT, 100)
    pwm_left.start(0)
    pwm_right.start(0)
    
    try:
        # Test left motor
        print("Testing left motor forward...")
        GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
        GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        pwm_left.ChangeDutyCycle(50)
        time.sleep(2)
        
        print("Testing left motor backward...")
        GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.HIGH)
        time.sleep(2)
        
        pwm_left.ChangeDutyCycle(0)
        
        # Test right motor
        print("Testing right motor forward...")
        GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
        GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        pwm_right.ChangeDutyCycle(50)
        time.sleep(2)
        
        print("Testing right motor backward...")
        GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
        time.sleep(2)
        
    finally:
        pwm_left.stop()
        pwm_right.stop()
        GPIO.cleanup()
        
def test_camera():
    """Test camera capture"""
    print("\nTesting camera...")
    import cv2
    
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera")
            return
            
        print("Camera opened successfully")
        print("Capturing test frame...")
        
        ret, frame = cap.read()
        if ret:
            print("Successfully captured frame")
            cv2.imwrite('camera_test.jpg', frame)
            print("Test image saved as 'camera_test.jpg'")
        else:
            print("Error: Could not capture frame")
            
    finally:
        if 'cap' in locals():
            cap.release()

if __name__ == "__main__":
    print("AGV Hardware Test Script")
    print("=======================")
    
    while True:
        print("\nSelect test:")
        print("1. Test Motors")
        print("2. Test Camera")
        print("3. Exit")
        
        choice = input("Enter choice (1-3): ")
        
        if choice == '1':
            test_motors()
        elif choice == '2':
            test_camera()
        elif choice == '3':
            break
        else:
            print("Invalid choice")
            
    print("\nTest complete")
