#!/bin/bash

# AGV Installation Script
# Run this script after first boot of Raspberry Pi

# Update system
sudo apt update
sudo apt upgrade -y

# Install required packages
sudo apt install -y \
    python3-pip \
    python3-opencv \
    git \
    python3-rpi.gpio

# Create AGV directory
mkdir -p /home/pi/agv
cd /home/pi/agv

# Copy files from installation media
cp -r /boot/agv/* .

# Install Python dependencies
pip3 install -r requirements.txt

# Set up system service
sudo cp agv.service /etc/systemd/system/
sudo systemctl enable agv
sudo systemctl start agv

# Enable camera if using Pi Camera
sudo raspi-config nonint do_camera 0

echo "AGV Installation Complete!"
echo "Access the web interface at http://$(hostname -I | cut -d' ' -f1):5000"
echo "Username: admin"
echo "Password: agv123"
