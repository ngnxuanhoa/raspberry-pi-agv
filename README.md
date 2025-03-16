# Raspberry Pi AGV (Autonomous Guided Vehicle)

A Raspberry Pi-based autonomous guided vehicle with computer vision capabilities, SLAM-based navigation, and web interface control.

## Features
- Real-time camera feed and navigation map
- Web-based control interface accessible over LAN
- SLAM (Simultaneous Localization and Mapping)
- Autonomous navigation with obstacle avoidance
- Secure authentication for remote access

## Hardware Requirements
- Raspberry Pi 4
- Camera Module (Pi Camera or USB Webcam)
- L298N Motor Driver Module
- 2x DC Motors (12V recommended)
- Chassis with wheels
- Power supply:
  - 5V/3A for Raspberry Pi
  - 12V for motors (battery pack)
- Jumper wires
Cập nhật Raspberry Pi OS
sudo apt update
sudo apt upgrade -y
sudo reboot

## Quick Installation
1. Clone this repository:
```bash
git clone https://github.com/ngnxuanhoa/raspberry-pi-agv
cd raspberry-pi-agv
```

2. Install dependencies:
```bash
sudo apt update
sudo apt install -y python3-pip python3-opencv
pip3 install -r requirements.txt
```

3. Configure settings in `config.py`:
```python
CAMERA_ENABLED = True  # Enable for real hardware
WEB_USERNAME = 'admin'  # Change default credentials
WEB_PASSWORD = 'your_secure_password'
```

4. Start the AGV system:
```bash
python3 main.py
```

## Development Setup
1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

2. Run in development mode:
```bash
python3 main.py
```

The web interface will be available at: http://localhost:5000

## Production Deployment
1. Copy files to Raspberry Pi
2. Install as system service:
```bash
sudo cp install/agv.service /etc/systemd/system/
sudo systemctl enable agv
sudo systemctl start agv
```

## Hardware Setup
Connect the L298N motor driver to Raspberry Pi:
- ENA -> GPIO 25 (Pin 22)
- IN1 -> GPIO 17 (Pin 11)
- IN2 -> GPIO 18 (Pin 12)
- ENB -> GPIO 24 (Pin 18)
- IN3 -> GPIO 22 (Pin 15)
- IN4 -> GPIO 23 (Pin 16)
- GND -> GND

## Testing
Run the hardware test script:
```bash
python3 hardware_test.py
```

## Web Interface
Access the control interface at: http://[raspberry-pi-ip]:5000
- Default username: admin
- Default password: agv123

## Project Structure
```
.
├── hardware/           # Hardware control modules
├── navigation/         # SLAM and path planning
├── web/               # Web interface
├── install/           # Installation scripts
├── config.py          # Configuration settings
├── main.py            # Main application
└── hardware_test.py   # Hardware testing script
```

## License
MIT License

## Contributing
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Security Notes
- Change default credentials before deployment
- Keep emergency stop button accessible
- Monitor battery levels
- Secure all connections before operation
