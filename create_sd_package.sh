#!/bin/bash

# Script to create AGV installation package for SD card

# Create package directory
PACKAGE_DIR="agv_sd_package"
mkdir -p "$PACKAGE_DIR/agv"

# Copy source files
echo "Copying source files..."
cp main.py config.py hardware_test.py "$PACKAGE_DIR/agv/"
cp -r hardware navigation web "$PACKAGE_DIR/agv/"

# Copy installation files
echo "Copying installation files..."
cp install/setup.sh "$PACKAGE_DIR/agv/"
cp install/requirements.txt "$PACKAGE_DIR/agv/"
cp install/agv.service "$PACKAGE_DIR/agv/"
cp install/README.md "$PACKAGE_DIR/agv/"

# Create installation instructions
echo "Creating instructions..."
cat > "$PACKAGE_DIR/README.txt" << EOF
AGV Installation Package
=======================

To install the AGV system:

1. Copy the entire 'agv' folder to /boot/agv on your Raspberry Pi SD card
2. Insert SD card into Raspberry Pi and power on
3. SSH into your Pi (username: pi, password: raspberry)
4. Run the installation script:
   cd /boot/agv
   bash setup.sh

The web interface will be available at:
http://[raspberry-pi-ip]:5000
Username: admin
Password: agv123
EOF

echo "Package created in $PACKAGE_DIR"
echo "Copy the 'agv' folder to /boot/agv on your SD card"
