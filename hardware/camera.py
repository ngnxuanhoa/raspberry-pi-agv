"""Camera management module for video capture and processing"""
import cv2
import numpy as np
import threading
from config import CAMERA_RESOLUTION, CAMERA_FRAMERATE, CAMERA_ENABLED

class MockCamera:
    """Mock camera for development without hardware"""
    def __init__(self):
        self.resolution = CAMERA_RESOLUTION
        self.frame = np.zeros((CAMERA_RESOLUTION[1], CAMERA_RESOLUTION[0], 3), dtype=np.uint8)

    def read(self):
        # Generate a simple test pattern
        self.frame = np.zeros((CAMERA_RESOLUTION[1], CAMERA_RESOLUTION[0], 3), dtype=np.uint8)
        cv2.putText(self.frame, "Mock Camera", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        return True, self.frame.copy()

    def release(self):
        pass

    def set(self, prop, value):
        return True

    def isOpened(self):
        return True

class Camera:
    def __init__(self):
        self.camera = None
        self.frame = None
        self.running = False
        self._lock = threading.Lock()

    def start(self):
        """Initialize and start the camera capture"""
        if self.running:
            return

        if CAMERA_ENABLED:
            self.camera = cv2.VideoCapture(0)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_RESOLUTION[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_RESOLUTION[1])
            self.camera.set(cv2.CAP_PROP_FPS, CAMERA_FRAMERATE)
        else:
            self.camera = MockCamera()

        if not self.camera.isOpened():
            raise RuntimeError("Could not start camera")

        self.running = True
        threading.Thread(target=self._capture_loop, daemon=True).start()

    def _capture_loop(self):
        """Continuous capture loop"""
        while self.running:
            ret, frame = self.camera.read()
            if ret:
                with self._lock:
                    self.frame = frame

    def get_frame(self):
        """Get the latest frame from the camera"""
        with self._lock:
            if self.frame is None:
                return None
            return self.frame.copy()

    def stop(self):
        """Stop the camera capture"""
        self.running = False
        if self.camera:
            self.camera.release()

    def get_processed_frame(self):
        """Get processed frame for obstacle detection"""
        frame = self.get_frame()
        if frame is None:
            return None

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply edge detection
        edges = cv2.Canny(blurred, 50, 150)

        return edges