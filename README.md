
# NVMe Fan Control Installation Guide

This repository contains everything you need to control your NVMe fan on a Raspberry Pi using GPIO. It includes:

- **nvme-fan.py** – The Python script that monitors the NVMe temperature and controls the fan.
- **nvme-fan.service** – A systemd service file to run the script at startup.
- **install_nvme_fan.sh** – An installation script to automate the setup process.

---

## Prerequisites

- A Raspberry Pi configured with your NVMe fan hardware.
- Basic knowledge of using the terminal.
- **Required packages:** `python3`, and `git` (if you need to clone the repository).

---

## Installation Steps

1. **Clone the Repository (if not already present):**

   Open a terminal and run:
   ```bash
   git clone https://github.com/woojak/nvme-fan.git
   cd nvme-fan
   ```
   > *If you already have the repository on your device, you can skip this step.*

2. **Run the Installation Script:**

   The repository already includes an `install_nvme_fan.sh` script. To run it, execute:
   ```bash
   sudo chmod +x install_nvme_fan.sh
   sudo ./install_nvme_fan.sh
   ```
   This script will:
   - Update your package lists and install the required packages.
   - Set executable permissions for `nvme-fan.py`.
   - Copy `nvme-fan.service` to `/etc/systemd/system/`.
   - Reload the systemd configuration, enable the service to start on boot, and start the service immediately.

3. **Verify the Service:**

   To check if the service is running properly, execute:
   ```bash
   sudo systemctl status nvme-fan.service
   ```
   You should see that the service is active and running. If not, check the logs using:
   ```bash
   sudo journalctl -u nvme-fan.service
   ```

---

## Visual Overview

```
       ┌─────────────────────────┐
       │ NVMe Fan Control Repo   │
       └─────────────────────────┘
                  │
                  ▼
     ┌─────────────────────────┐
     │   nvme-fan.py           │   <-- Python script that reads temperature and controls the fan 🌡️💨
     └─────────────────────────┘
                  │
                  ▼
     ┌─────────────────────────┐
     │  nvme-fan.service       │   <-- systemd service file to run the script at boot 🔧
     └─────────────────────────┘
                  │
                  ▼
     ┌─────────────────────────┐
     │ install_nvme_fan.sh     │   <-- Installation script (this file!) 🚀
     └─────────────────────────┘
```

---

## Troubleshooting Tips

- **GPIO Busy Issues:**  
  If you run into errors about GPIO pins being busy, verify that no other processes are using the pins. You can use:
  ```bash
  sudo apt-get install gpiod
  gpioinfo
  ```
  This will list all currently used GPIO pins.

- **Service Logs:**  
  Use the following command to view the logs and troubleshoot any issues:
  ```bash
  sudo journalctl -u nvme-fan.service
  ```

---

Enjoy your project and happy cooling! 😎👍

----------------------------------------------------------------------------------------


## Operation and Temperature Customization

The **NVMe Fan Control** script is designed to continuously monitor the temperature of your NVMe drive and automatically control a cooling fan based on configurable thresholds. 
Here's how it works and how you can adjust the settings:

### How It Works

1. **Temperature Reading:**  
   The script uses the `nvme smart-log` command to fetch temperature data from the NVMe drive. It parses the output to extract the temperature value from "Temperature Sensor 1".  

2. **Fan Control Logic:**  
   - **Fan Activation:** When the temperature reaches or exceeds the **activation threshold** (by default, `TEMP_ON = 50°C`), the script turns the fan on.
   - **Fan Deactivation:** When the temperature drops to or below the **deactivation threshold** (by default, `TEMP_OFF = 45°C`), the script turns the fan off.

3. **Continuous Monitoring:**  
   The script operates in an infinite loop, checking the temperature every 10 seconds. It is designed to run as a systemd service so that it automatically starts at boot and keeps your system cool.

### Customizing Temperature Thresholds

You can easily modify the temperature thresholds to suit your specific requirements:

- **Locate the Constants:**  
  Open the `nvme-fan.py` file in your preferred text editor. At the top of the file, you'll find the following lines:

  ```python
  TEMP_ON = 50   # Temperature at which the fan turns on
  TEMP_OFF = 45  # Temperature at which the fan turns off
  ```

- **Adjust the Values:**  
  Change `50` and `45` to your desired values. For example, if you want the fan to turn on at 55°C and turn off at 50°C, update the constants as follows:

  ```python
  TEMP_ON = 55
  TEMP_OFF = 50
  ```

- **Save and Restart:**  
  After modifying the file, save your changes and restart the NVMe Fan Control service to apply the new thresholds:

  ```bash
  sudo systemctl restart nvme-fan.service
  ```

### Additional Customization Options

- **Polling Interval:**  
  The script checks the temperature every 10 seconds (using `time.sleep(10)`). If you wish to change this interval, locate the following line in the script and adjust the number of seconds:

  ```python
  time.sleep(10)
  ```

- **Log Output:**  
  The script prints temperature readings and status messages to the console. You can redirect or expand this logging functionality if needed for your monitoring or troubleshooting purposes.

### Visual Overview

```
       ┌─────────────────────────────────────┐
       │     NVMe Fan Control Script         │
       ├─────────────────────────────────────┤
       │ Read NVMe temperature sensor data   │
       │    ↓                                │
       │ Parse temperature from output       │
       │    ↓                                │
       │ If temperature ≥ TEMP_ON → Turn on fan│
       │ If temperature ≤ TEMP_OFF → Turn off fan│
       └─────────────────────────────────────┘
```

By adjusting these parameters, you can tailor the script’s behavior to best suit your cooling needs and NVMe drive specifications. Enjoy the enhanced cooling management and feel free to further customize the script for your specific application! 😎❄️

---
