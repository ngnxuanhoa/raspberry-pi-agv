"""Mock GPIO module for development and testing"""
class GPIOMock:
    BCM = 11
    OUT = 0
    IN = 1
    HIGH = 1
    LOW = 0
    
    def __init__(self):
        self.pins = {}
        self.pwm_pins = {}
        
    def setmode(self, mode):
        pass
        
    def setwarnings(self, flag):
        pass
        
    def setup(self, pin, mode):
        self.pins[pin] = 0
        
    def output(self, pin, value):
        self.pins[pin] = value
        
    def cleanup(self):
        self.pins.clear()
        self.pwm_pins.clear()
        
    def PWM(self, pin, freq):
        return PWMMock(pin, freq)
        
class PWMMock:
    def __init__(self, pin, freq):
        self.pin = pin
        self.freq = freq
        self.duty_cycle = 0
        
    def start(self, dc):
        self.duty_cycle = dc
        
    def ChangeDutyCycle(self, dc):
        self.duty_cycle = dc
        
    def stop(self):
        self.duty_cycle = 0
