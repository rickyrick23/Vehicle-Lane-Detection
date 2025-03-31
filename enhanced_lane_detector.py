import cv2
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

class LaneDetector:
    def __init__(self, speed_limit=60):
        self.speed_processor = SpeedProcessor(speed_limit)
        
    def process_frame(self, frame, current_speed):
        """Process single frame with speed adaptation"""
        speed_data = self.speed_processor.add_speed_reading(current_speed)
        settings = get_speed_settings(speed_data['factor'])
        
        # Convert to grayscale and blur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        
        # Edge detection with speed-adaptive thresholds
        edges = cv2.Canny(blur, settings['canny_min'], settings['canny_max'])
        
        # Speed-adaptive ROI
        height, width = edges.shape
        roi_start = int(height * settings['roi_start'])
        roi = edges[roi_start:height, :]
        
        # Detect lines with adaptive parameters
        lines = cv2.HoughLinesP(roi, 1, np.pi/180, 
                              threshold=settings['hough_thresh'],
                              minLineLength=30,
                              maxLineGap=50)
        
        # Draw results
        if lines is not None:
            for line in lines:
                x1,y1,x2,y2 = line[0]
                cv2.line(frame, (x1,y1+roi_start), (x2,y2+roi_start), (0,255,0), 2)
        
        # Add status overlay with all required parameters
        height, width = frame.shape[:2]
        self._add_overlay(frame, speed_data, lines, width)
        
        return frame
    
    def _add_overlay(self, frame, speed_data, lines, width):
        """Determine if vehicle is in right lane"""
        in_right_lane = False
        color = (0,0,255)  # Red by default (not in right lane)
        
        if lines is not None:
            # Calculate average line position
            line_positions = [(line[0][0] + line[0][2])/2 for line in lines]
            avg_x = np.mean(line_positions)
            
            # Check if majority of lines are in right lane
            right_lane_lines = sum(1 for x in line_positions if x > width * 0.6)
            in_right_lane = right_lane_lines / len(lines) > 0.7
            
            if in_right_lane:
                color = (0,255,0)  # Green
            
        lane_status = "IN RIGHT LANE" if in_right_lane else "NOT IN RIGHT LANE"
        speed_status = f"SPEED: {speed_data['current']}km/h"
        
        # Display lane status (top)
        cv2.putText(frame, lane_status, (20, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        # Display speed (below lane status)
        speed_color = (0,255,0)  # Green
        if speed_data['status'] == "WARNING":
            speed_color = (0,255,255)  # Yellow
        elif speed_data['status'] == "DANGER":
            speed_color = (0,0,255)  # Red
            
        cv2.putText(frame, speed_status, (20, 100), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, speed_color, 2)

def process_video(input_path, output_path, speed_data):
    """Process video with simulated speed data"""
    print(f"Attempting to open video: {input_path}")
    detector = LaneDetector()
    cap = cv2.VideoCapture(input_path)
    
    if not cap.isOpened():
        print("Error: Could not open video file")
        return
    else:
        print("Successfully opened video file")
        print(f"Frame width: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}")
        print(f"Frame height: {int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
        print(f"Total frames: {int(cap.get(cv2.CAP_PROP_FRAME_COUNT))}")
    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Create output writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Get simulated speed (cycling through speed_data)
        speed = speed_data[frame_count % len(speed_data)]
        processed = detector.process_frame(frame, speed)
        out.write(processed)
        frame_count += 1
    
    cap.release()
    out.release()

if __name__ == "__main__":
    # Simulated speed data (km/h)
    test_speeds = [40, 50, 60, 70, 80, 90, 100]
    process_video("solidWhiteRight.mp4", "lane_detection_output.mp4", test_speeds)
    print("Processing complete. Output saved to lane_detection_output.mp4 in current directory")