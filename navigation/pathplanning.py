"""Path planning and navigation module"""
import numpy as np
from config import MIN_OBSTACLE_DISTANCE

class PathPlanner:
    def __init__(self):
        self.current_path = []
        self.target = None
        
    def set_target(self, target_pos):
        """Set new target position"""
        self.target = np.array(target_pos)
        self._plan_path()
        
    def _plan_path(self):
        """Simple A* path planning implementation"""
        if self.target is None:
            return
            
        # Implement simple direct path for now
        self.current_path = [self.target]
        
    def get_next_movement(self, current_pos, obstacles):
        """Get next movement vector based on current position and obstacles"""
        if not self.current_path:
            return (0, 0)
            
        target = self.current_path[0]
        direction = target - current_pos
        distance = np.linalg.norm(direction)
        
        # Check for obstacles
        if self._check_obstacles(obstacles):
            return (0, 0)  # Stop if obstacles detected
            
        # If close to target, pop it
        if distance < 5:
            self.current_path.pop(0)
            return (0, 0)
            
        # Normalize direction
        direction = direction / distance
        
        return tuple(direction * min(distance, 10))
        
    def _check_obstacles(self, obstacles):
        """Check if obstacles are too close"""
        if obstacles is None:
            return False
            
        # Simple obstacle check - if any white pixels are too close
        return np.any(obstacles > 0)
