"""Configuration settings for the AGV system"""

# GPIO Pin Configuration
MOTOR_LEFT_FORWARD = 17
MOTOR_LEFT_BACKWARD = 18
MOTOR_RIGHT_FORWARD = 22
MOTOR_RIGHT_BACKWARD = 23
MOTOR_ENABLE_LEFT = 25
MOTOR_ENABLE_RIGHT = 24

# Camera Configuration
CAMERA_RESOLUTION = (640, 480)
CAMERA_FRAMERATE = 30

# Web Server Configuration
WEB_HOST = '0.0.0.0'  # Allow access from LAN
WEB_PORT = 5000
WEB_USERNAME = 'admin'  # Basic authentication credentials
WEB_PASSWORD = 'agv123'

# Navigation Configuration
MAX_SPEED = 100  # Maximum motor speed (0-100)
MIN_OBSTACLE_DISTANCE = 30  # cm
SLAM_MAP_RESOLUTION = 50  # pixels per meter
MAP_SIZE = (1000, 1000)  # pixels

# Safety Configuration
TIMEOUT_DURATION = 10  # seconds
CAMERA_ENABLED = False  # Set to True when using real hardware