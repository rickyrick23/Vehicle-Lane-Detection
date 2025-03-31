# Lane Detection System with Speed Monitoring

A computer vision system that detects lane position and displays current speed with safety indicators.

## Features

- Real-time lane position detection (In Right Lane/Not In Right Lane)
- Speed display with color-coded safety indicators:
  - Green: Normal speed
  - Yellow: Warning speed
  - Red: Dangerous speed
- Adaptive detection parameters based on speed
- Video processing with OpenCV

## Requirements

- Python 3.6+
- OpenCV (`pip install opencv-python`)
- NumPy (`pip install numpy`)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rickyrick23/Vehicle-Lane-Detection.git
cd lane-detection
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Processing
Process the sample video:
```bash
python enhanced_lane_detector.py
```

### Custom Video Processing
To process your own video:
```bash
python enhanced_lane_detector.py -i your_video.mp4 -o output.mp4
```

### Command Line Options
| Option | Description | Default |
|--------|-------------|---------|
| `-i` | Input video path | `solidWhiteRight.mp4` |
| `-o` | Output video path | `lane_detection_output.mp4` |
| `-s` | Simulated speeds (comma-separated) | `40,50,60,70,80,90,100` |

## Sample Output
<!-- Add screenshot manually after deployment:
1. Run the detector: `python complete_lane_detector.py`
2. Open output video in any player
3. Take screenshot during playback
4. Save as 'sample_frame.png' in project root
5. Update this README with the actual image
-->

## File Structure
```
.
├── enhanced_lane_detector.py    # Main detection script
├── speed_monitor.py             # Speed processing module
├── README.md                   # This file
└── solidWhiteRight.mp4         # Sample input video
```

## License
MIT License - see [LICENSE](LICENSE) file for details
