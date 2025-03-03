# AGV Raspberry Pi Installation Package

## Installation Instructions

1. Write this entire package to a fresh SD card
2. Insert SD card into Raspberry Pi 4
3. Connect your Raspberry Pi to power and network
4. SSH into your Raspberry Pi:
   ```bash
   ssh pi@raspberrypi.local
   ```
   Default password: raspberry

5. Run the installation script:
   ```bash
   cd /boot/agv
   bash setup.sh
   ```

6. After installation completes:
   - Web interface will be available at: http://[raspberry-pi-ip]:5000
   - Default login: admin/agv123

## Hardware Setup Required:
1. L298N Motor Driver connections:
   - ENA -> GPIO 25 (Pin 22)
   - IN1 -> GPIO 17 (Pin 11)
   - IN2 -> GPIO 18 (Pin 12)
   - ENB -> GPIO 24 (Pin 18)
   - IN3 -> GPIO 22 (Pin 15)
   - IN4 -> GPIO 23 (Pin 16)
   - GND -> GND

2. Camera:
   - If using Pi Camera: Connect to dedicated camera port
   - If using USB Camera: Connect to any USB port

3. Power Supply:
   - Raspberry Pi: 5V/3A power supply
   - Motors: 12V battery pack

## Testing
After installation, run the hardware test:
```bash
cd /home/pi/agv
python3 hardware_test.py
```

## Troubleshooting
If you encounter any issues:
1. Check all hardware connections
2. Verify power supply voltages
3. Check system logs: `sudo journalctl -u agv`
4. Test motors and camera individually using hardware_test.py
