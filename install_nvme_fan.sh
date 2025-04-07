#!/bin/bash
# NVMe Fan Control installation script (without fetching the repository)

# Step 1: Install required packages
echo "Installing packages: python3, python3-gpiozero, nvme-cli..."
sudo apt-get update
sudo apt-get install -y python3 python3-gpiozero nvme-cli

# Step 2: Set the installation directory (assuming the repository is located in the current directory)
INSTALL_DIR=$(pwd)

# Step 3: Set executable permissions for the script
echo "Setting executable permissions for nvme-fan.py and nvme_fan_gui.sh ..."
sudo chmod +x "$INSTALL_DIR/nvme-fan.py"
sudo chmod +x "$INSTALL_DIR/nvme_fan_gui.sh"

# Step 4: Install the systemd service file
echo "Copying the service file to /etc/systemd/system/ ..."
sudo cp "$INSTALL_DIR/nvme-fan.service" /etc/systemd/system/nvme-fan.service

# Step 5: Reload systemd configuration, enable and start the service
echo "Reloading systemd configuration..."
sudo systemctl daemon-reload
echo "Enabling nvme-fan service to start at boot..."
sudo systemctl enable nvme-fan.service
echo "Starting nvme-fan service..."
sudo systemctl start nvme-fan.service

echo "Installation completed. Check service status with:"
echo "  sudo systemctl status nvme-fan.service"
