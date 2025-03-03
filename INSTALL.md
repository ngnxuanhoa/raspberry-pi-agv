# AGV Installation Guide for Raspberry Pi 4

## Hardware Setup

### Components Required
- Raspberry Pi 4
- Raspberry Pi Camera Module or USB Webcam
- L298N Motor Driver Module
- 2x DC Motors (12V recommended)
- Chassis with wheels
- Power supply:
  - 5V/3A for Raspberry Pi
  - 12V for motors (battery pack)
- Jumper wires

### GPIO Connections
1. Motor Driver (L298N) to Raspberry Pi:
   - ENA -> GPIO 25 (Pin 22)
   - IN1 -> GPIO 17 (Pin 11)
   - IN2 -> GPIO 18 (Pin 12)
   - ENB -> GPIO 24 (Pin 18)
   - IN3 -> GPIO 22 (Pin 15)
   - IN4 -> GPIO 23 (Pin 16)
   - GND -> GND
   
2. Camera:
   - If using Pi Camera: Connect to the dedicated camera port
   - If using USB Camera: Connect to any USB port

## Software Installation

1. Update Raspberry Pi:
```bash
sudo apt update
sudo apt upgrade -y
```

2. Install required packages:
```bash
sudo apt install -y python3-pip python3-opencv git
```

3. Clone the AGV repository:
```bash
git clone https://github.com/ngnxuanhoa/raspberry-pi-agv
cd agv-project
```

4. Install Python dependencies:
```bash
pip3 install flask numpy opencv-python RPi.GPIO
```

5. Configure the system:
   - Edit config.py:
     - Set CAMERA_ENABLED = True
     - Adjust CAMERA_RESOLUTION if needed
     - Set WEB_USERNAME and WEB_PASSWORD
     - Verify GPIO pin numbers match your connections

6. Start the AGV system:
```bash
python3 main.py
```

## Testing the Installation

1. The system will start and display the web interface URL
2. Access the web interface from any device on your LAN:
   - URL: http://[raspberry-pi-ip]:5000
   - Login with configured credentials (default: admin/agv123)

3. Verify:
   - Camera feed is visible
   - Navigation map shows
   - Motors respond to commands
   - Emergency stop works

## Troubleshooting

1. Camera Issues:
   - Check if camera is enabled in raspi-config
   - Verify camera connections
   - Check CAMERA_ENABLED in config.py

2. Motor Issues:
   - Verify GPIO connections
   - Check motor power supply
   - Test motors individually using test scripts

3. Web Interface Issues:
   - Verify Pi is connected to network
   - Check firewall settings
   - Verify correct IP address and port

## Safety Notes

1. Always test motors before mounting on chassis
2. Keep emergency stop button accessible
3. Monitor battery levels
4. Secure all connections before operation
