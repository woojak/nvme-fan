from gpiozero import OutputDevice, Device
import subprocess
import time
import re

# GPIO pin configuration for fan (we use GPIO 14)
FAN_PIN = 14
fan = OutputDevice(FAN_PIN)

# Temperature thresholds in Celsius
TEMP_ON = 50   # Temperature at which fan turns on
TEMP_OFF = 45  # Temperature at which fan turns off

def get_nvme_temperature():
    try:
        # Execute nvme-cli command and read temperature from sensor 1
        result = subprocess.run(['nvme', 'smart-log', '/dev/nvme0'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'Temperature Sensor 1' in line:
                # Extract temperature value (e.g. "32°C")
                temp_match = re.search(r'(\d+)\s?°C', line)
                if temp_match:
                    return int(temp_match.group(1))
    except Exception as e:
        print(f"Error reading temperature: {e}")
    return None

try:
    fan_on = False
    while True:
        temperature = get_nvme_temperature()
        if temperature is not None:
            print(f"Current NVMe temperature: {temperature}°C")
            if temperature >= TEMP_ON and not fan_on:
                fan.on()
                fan_on = True
                print("Fan ON ")
            elif temperature <= TEMP_OFF and fan_on:
                fan.off()
                fan_on = False
                print("Fan OFF")
        else:
            print("Could not read temperature.")
        time.sleep(10)  # Wait 10 seconds before reading again
except KeyboardInterrupt:
    print("Stopped by user")
finally:
    # Make sure the fan is off and GPIO resources are freed
    fan.off()
    fan.close()
    Device.pin_factory.reset()
