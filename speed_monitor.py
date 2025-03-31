import numpy as np

class SpeedProcessor:
    def __init__(self, speed_limit=60):
        self.speed_limit = speed_limit
        self.speed_history = []
        
    def add_speed_reading(self, speed):
        """Add new speed reading and return analysis"""
        if not isinstance(speed, (int, float)):
            speed = self.speed_limit  # Default if invalid
            
        self.speed_history.append(speed)
        if len(self.speed_history) > 5:
            self.speed_history.pop(0)
            
        return self._analyze()
        
    def _analyze(self):
        """Calculate speed metrics and status"""
        current = self.speed_history[-1]
        avg = np.mean(self.speed_history)
        
        status = "NORMAL"
        if current > self.speed_limit * 1.3:
            status = "DANGER"
        elif current > self.speed_limit:
            status = "WARNING"
            
        factor = min(1.0, max(0.0, (current - self.speed_limit)/20))
        
        return {
            "current": current,
            "average": avg,
            "status": status,
            "factor": factor
        }

def get_speed_settings(speed_factor):
    """Return detection parameters adjusted for speed"""
    return {
        "canny_min": 50 + int(30 * speed_factor),
        "canny_max": 150 + int(50 * speed_factor),
        "hough_thresh": max(20, 50 - int(25 * speed_factor)),
        "roi_start": 0.5 - (0.15 * speed_factor)
    }