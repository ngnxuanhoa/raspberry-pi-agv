"""Main control script for the AGV system"""
import time
import signal
import sys
from hardware.camera import Camera
from hardware.motors import Motors
from navigation.slam import SLAM
from navigation.pathplanning import PathPlanner
from web.server import start_server, app
from config import TIMEOUT_DURATION
import threading

class AGV:
    def __init__(self):
        self.camera = Camera()
        self.motors = Motors()
        self.slam = SLAM()
        self.path_planner = PathPlanner()
        self.running = False

        # Set global references for web server
        import web.server as server
        server.camera = self.camera
        server.slam = self.slam
        server.path_planner = self.path_planner

    def start(self):
        """Start all AGV systems"""
        self.running = True

        # Start camera
        try:
            self.camera.start()
        except RuntimeError as e:
            print(f"Failed to start camera: {e}")
            self.cleanup()
            sys.exit(1)

        # Start web server in separate thread
        self.web_thread = threading.Thread(target=start_server)
        self.web_thread.daemon = True
        self.web_thread.start()

        # Main control loop
        self.control_loop()

    def control_loop(self):
        """Main control loop"""
        last_update = time.time()

        while self.running:
            current_time = time.time()
            dt = current_time - last_update

            # Get camera frame and process
            frame = self.camera.get_processed_frame()

            if frame is not None:
                # Update SLAM
                motion = self.get_motion_estimate()
                self.slam.update(frame, motion)

                # Get current position and obstacles
                current_pos = self.slam.get_position()
                obstacles = self.detect_obstacles(frame)

                # Get next movement
                movement = self.path_planner.get_next_movement(
                    current_pos,
                    obstacles
                )

                # Control motors
                self.control_motors(movement)

            # Safety timeout
            if current_time - last_update > TIMEOUT_DURATION:
                self.motors.stop()

            last_update = current_time
            time.sleep(0.01)  # Small sleep to prevent CPU overload

    def get_motion_estimate(self):
        """Estimate motion from sensors (simplified)"""
        # In a real implementation, this would use encoders or IMU
        return (0, 0)  # No motion for now

    def detect_obstacles(self, frame):
        """Detect obstacles in the processed frame"""
        # Simple threshold-based detection
        return frame > 200

    def control_motors(self, movement):
        """Control motors based on desired movement"""
        dx, dy = movement

        # Simple differential drive control
        left_speed = (dy + dx) * 50  # Scale to motor speed
        right_speed = (dy - dx) * 50

        self.motors.set_speeds(left_speed, right_speed)

    def cleanup(self):
        """Cleanup and stop all systems"""
        self.running = False
        self.camera.stop()
        self.motors.cleanup()

def signal_handler(sig, frame):
    """Handle shutdown signals"""
    print("Shutting down AGV...")
    if '_agv_instance' in globals():
        globals()['_agv_instance'].cleanup()
    sys.exit(0)

if __name__ == "__main__":
    # Setup signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start AGV
    print("Starting AGV...")
    _agv_instance = AGV()
    _agv_instance.start()