import tkinter as tk
from tkinter import messagebox
import re
import subprocess

CONFIG_FILE = "nvme-fan.py"  # Assumes nvme-fan.py is in the same directory

def update_config():
    try:
        # Read current file content
        with open(CONFIG_FILE, "r") as f:
            content = f.read()
        
        # Get new values from GUI entries
        new_fan_pin = fan_pin_entry.get().strip()
        new_temp_on = temp_on_entry.get().strip()
        new_temp_off = temp_off_entry.get().strip()
        new_sensor_number = sensor_number_entry.get().strip()
        
        # Replace values using regex (lines beginning with variable name)
        content_new = re.sub(r"^(FAN_PIN\s*=\s*)(\d+)", r"\1" + new_fan_pin, content, flags=re.MULTILINE)
        content_new = re.sub(r"^(TEMP_ON\s*=\s*)(\d+)", r"\1" + new_temp_on, content_new, flags=re.MULTILINE)
        content_new = re.sub(r"^(TEMP_OFF\s*=\s*)(\d+)", r"\1" + new_temp_off, content_new, flags=re.MULTILINE)
        content_new = re.sub(r"^(SENSOR_NUMBER\s*=\s*)(\d+)", r"\1" + new_sensor_number, content_new, flags=re.MULTILINE)
        
        with open(CONFIG_FILE, "w") as f:
            f.write(content_new)
        
        messagebox.showinfo("Success", "Configuration updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update configuration: {e}")

def restart_service():
    try:
        subprocess.run(["sudo", "systemctl", "restart", "nvme-fan.service"], check=True)
        messagebox.showinfo("Success", "Service restarted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to restart service: {e}")

def start_service():
    try:
        subprocess.run(["sudo", "systemctl", "start", "nvme-fan.service"], check=True)
        messagebox.showinfo("Success", "Service started successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start service: {e}")

def install_service():
    try:
        subprocess.run(["sudo", "./install_nvme_fan.sh"], check=True)
        messagebox.showinfo("Success", "Service installed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to install service: {e}")

def uninstall_service():
    try:
        subprocess.run(["sudo", "./uninstall_nvme_fan.sh"], check=True)
        messagebox.showinfo("Success", "Service uninstalled successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to uninstall service: {e}")

# Create main window
root = tk.Tk()
root.title("NVMe Fan Control Configuration")

# Create labels and entries for parameters
tk.Label(root, text="FAN_PIN:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
fan_pin_entry = tk.Entry(root)
fan_pin_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="TEMP_ON:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
temp_on_entry = tk.Entry(root)
temp_on_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="TEMP_OFF:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
temp_off_entry = tk.Entry(root)
temp_off_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="SENSOR_NUMBER:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
sensor_number_entry = tk.Entry(root)
sensor_number_entry.grid(row=3, column=1, padx=5, pady=5)

# Buttons for configuration and service control
update_button = tk.Button(root, text="Update Configuration", command=update_config)
update_button.grid(row=4, column=0, columnspan=2, pady=10)

restart_button = tk.Button(root, text="Restart Service", command=restart_service)
restart_button.grid(row=5, column=0, columnspan=2, pady=5)

start_button = tk.Button(root, text="Start Service", command=start_service)
start_button.grid(row=6, column=0, columnspan=2, pady=5)

install_button = tk.Button(root, text="Install Service", command=install_service)
install_button.grid(row=7, column=0, columnspan=2, pady=5)

uninstall_button = tk.Button(root, text="Uninstall Service", command=uninstall_service)
uninstall_button.grid(row=8, column=0, columnspan=2, pady=5)

# Pre-fill the entry fields with current values from nvme-fan.py
try:
    with open(CONFIG_FILE, "r") as f:
        content = f.read()
        fan_pin_match = re.search(r"^FAN_PIN\s*=\s*(\d+)", content, re.MULTILINE)
        temp_on_match = re.search(r"^TEMP_ON\s*=\s*(\d+)", content, re.MULTILINE)
        temp_off_match = re.search(r"^TEMP_OFF\s*=\s*(\d+)", content, re.MULTILINE)
        sensor_number_match = re.search(r"^SENSOR_NUMBER\s*=\s*(\d+)", content, re.MULTILINE)
        if fan_pin_match:
            fan_pin_entry.insert(0, fan_pin_match.group(1))
        if temp_on_match:
            temp_on_entry.insert(0, temp_on_match.group(1))
        if temp_off_match:
            temp_off_entry.insert(0, temp_off_match.group(1))
        if sensor_number_match:
            sensor_number_entry.insert(0, sensor_number_match.group(1))
except Exception as e:
    messagebox.showerror("Error", f"Error reading configuration from file: {e}")

root.mainloop()
