# HandTrackingAutomation
# Hand Gesture Control

A Python-based **Hand Gesture Recognition System** using **OpenCV, MediaPipe, and PyAutoGUI** to control system actions like opening Chrome, adjusting volume, taking screenshots, and more—just by drawing gestures in the air!

## Features
✅ **Hand Tracking** using OpenCV & MediaPipe  
✅ **Gesture Recognition** for predefined shapes  
✅ **Automated Actions** (Open apps, control volume, take screenshots, etc.)  
✅ **Customizable Gestures** via `gestures.json`  
✅ **Real-time Mouse Control** with index finger movement  
✅ **Click Detection** using thumb & index finger distance  

## Installation
### Prerequisites
Ensure you have **Python 3.7+** installed. Then install dependencies:

```sh
pip install opencv-python mediapipe pyautogui numpy
```

## Usage
1. **Run the script**:
   ```sh
   python gesture_control.py
   ```
2. **Perform gestures** in front of the webcam to trigger actions.
3. **Press 'Q'** to quit the application.

## Predefined Gestures & Actions
| Gesture | Action |
|---------|--------|
| C | Open Chrome |
| > | Volume Up |
| < | Volume Down |
| O | Show Desktop |
| L | Delete |
| 2 | Rename |
| S | Screenshot |
| T | Open Notepad |
| X | Lock Screen |
| U | Undo |

You can modify gestures in `gestures.json` to customize actions.

## How It Works
- **Hand tracking** detects the position of fingers.
- **Gesture path** is recorded and analyzed.
- **Recognized gestures** trigger system actions using PyAutoGUI.

## Contributing
Pull requests are welcome! Feel free to improve gesture recognition or add new features.

## License
This project is licensed under the **MIT License**.

---
🔗 **GitHub Repository:** [Your Repo Link]

