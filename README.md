# GestureCalculator
A real-time **gesture-controlled calculator** built using **Python**, **OpenCV**, and **MediaPipe**, allowing users to perform basic arithmetic operations using only their hand gestures — no buttons or keyboard required!

# How It Works
- Uses hand tracking to detect **fingers as digit and operation**
- **Gesture combinations** are mapped to:
   -- One Hand : 0 - 5 fingers --> 0-5 dgits
   -- Two Hand: 5 + 1 fingers--> "+"
                5 + 2 fingers--> "-"
                5 + 3 fingers--> "*"
                5 + 4 fingers--> "/"
                2 + 2 fingers--> "delete"
                5 + 5 fingers-->" clear"
                0 + 0 fingers--> "="
---
  ##  Features

-  Real-time gesture detection
-  Hands-free calculator input
-  Basic arithmetic operations: `+`, `-`, `×`, `÷`
-  Supports multi-digit numbers
-  Clean UI rendered over video

---
##  Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/shivangi-6382/GestureCalculator.git
cd GestureCalculator
 ```
### 2. Install Requirements
```bash
pip install opencv-python mediapipe numpy
 ```
### 3.Run Application
```bash
python GestureCalculator.py
 ```
## License
This project is licensed under the MIT License

  


  
  
