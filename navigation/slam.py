"""Simple SLAM implementation for AGV mapping"""
import numpy as np
import cv2
from config import SLAM_MAP_RESOLUTION, MAP_SIZE, CAMERA_RESOLUTION

class SLAM:
    def __init__(self):
        self.map = np.zeros(MAP_SIZE, dtype=np.uint8)
        self.position = np.array([MAP_SIZE[0]//2, MAP_SIZE[1]//2])  # Start at center
        self.orientation = 0  # radians
        self._draw_grid()

    def _draw_grid(self):
        """Draw reference grid on the map"""
        # Draw vertical lines
        for x in range(0, MAP_SIZE[0], 50):
            cv2.line(self.map, (x, 0), (x, MAP_SIZE[1]), 25, 1)

        # Draw horizontal lines
        for y in range(0, MAP_SIZE[1], 50):
            cv2.line(self.map, (0, y), (MAP_SIZE[0], y), 25, 1)

    def update(self, frame, motion):
        """Update SLAM with new camera frame and motion data"""
        if frame is None:
            return

        # Update position based on motion
        dx, dy = motion
        self.position[0] += dx * SLAM_MAP_RESOLUTION
        self.position[1] += dy * SLAM_MAP_RESOLUTION

        # Ensure position stays within bounds
        self.position = np.clip(self.position, 0, MAP_SIZE[0]-1)

        # Process frame to detect features
        edges = cv2.Canny(frame, 50, 150)

        # Update map with detected features
        map_region = self._get_map_region()
        self.map[map_region] = cv2.addWeighted(
            self.map[map_region],
            0.7,
            edges,
            0.3,
            0
        )

    def _get_map_region(self):
        """Get the current region of the map based on position"""
        x, y = self.position.astype(int)
        half_width = CAMERA_RESOLUTION[0] // 2
        half_height = CAMERA_RESOLUTION[1] // 2

        x1 = max(0, x - half_width)
        x2 = min(MAP_SIZE[0], x + half_width)
        y1 = max(0, y - half_height)
        y2 = min(MAP_SIZE[1], y + half_height)

        return slice(y1, y2), slice(x1, x2)

    def get_map(self):
        """Get the current map with robot position marked"""
        # Create a colored map for better visualization
        map_rgb = cv2.cvtColor(self.map, cv2.COLOR_GRAY2BGR)

        # Draw robot position
        pos = self.position.astype(int)
        cv2.circle(map_rgb, tuple(pos), 10, (0, 0, 255), -1)  # Red circle for robot
        cv2.circle(map_rgb, tuple(pos), 12, (0, 0, 255), 2)   # Red outline

        # Draw robot's field of view
        fov_pts = np.array([
            pos,
            pos + [CAMERA_RESOLUTION[0]//2, CAMERA_RESOLUTION[1]//2],
            pos + [-CAMERA_RESOLUTION[0]//2, CAMERA_RESOLUTION[1]//2]
        ], dtype=np.int32)
        cv2.polylines(map_rgb, [fov_pts], True, (0, 255, 0), 2)

        return map_rgb

    def get_position(self):
        """Get current position"""
        return self.position.copy()