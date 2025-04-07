#!/usr/bin/env python3
import curses
import subprocess
import re
import os

# Define file paths (adjust if necessary)
CONFIG_FILE = "nvme-fan.py"
INSTALL_SCRIPT = "./install_nvme_fan.sh"
UNINSTALL_SCRIPT = "./uninstall_nvme_fan.sh"

def get_current_value(pattern):
    """
    Reads the CONFIG_FILE and returns the first captured value from a matching line.
    """
    try:
        with open(CONFIG_FILE, 'r') as f:
            for line in f:
                match = re.match(pattern, line)
                if match:
                    return match.group(1)
    except Exception as e:
        return None
    return None

def update_config(new_values):
    """
    Updates the CONFIG_FILE replacing values for FAN_PIN, TEMP_ON, TEMP_OFF, SENSOR_NUMBER.
    """
    try:
        with open(CONFIG_FILE, 'r') as f:
            content = f.read()
        content = re.sub(r'^(FAN_PIN\s*=\s*)\d+', r'\1' + str(new_values['FAN_PIN']), content, flags=re.MULTILINE)
        content = re.sub(r'^(TEMP_ON\s*=\s*)\d+', r'\1' + str(new_values['TEMP_ON']), content, flags=re.MULTILINE)
        content = re.sub(r'^(TEMP_OFF\s*=\s*)\d+', r'\1' + str(new_values['TEMP_OFF']), content, flags=re.MULTILINE)
        content = re.sub(r'^(SENSOR_NUMBER\s*=\s*)\d+', r'\1' + str(new_values['SENSOR_NUMBER']), content, flags=re.MULTILINE)
        with open(CONFIG_FILE, 'w') as f:
            f.write(content)
        return True
    except Exception as e:
        return False

def modify_parameters(stdscr):
    curses.echo()
    stdscr.clear()
    stdscr.addstr("Modify Parameters\n\n")

    # Get current values (or default if not found)
    current_fan_pin = get_current_value(r'^FAN_PIN\s*=\s*(\d+)') or "14"
    current_temp_on = get_current_value(r'^TEMP_ON\s*=\s*(\d+)') or "50"
    current_temp_off = get_current_value(r'^TEMP_OFF\s*=\s*(\d+)') or "45"
    current_sensor_number = get_current_value(r'^SENSOR_NUMBER\s*=\s*(\d+)') or "1"

    stdscr.addstr(f"Current FAN_PIN ({current_fan_pin}): ")
    fan_pin = stdscr.getstr().decode('utf-8').strip()
    if fan_pin == "":
        fan_pin = current_fan_pin

    stdscr.addstr(f"Current TEMP_ON ({current_temp_on}): ")
    temp_on = stdscr.getstr().decode('utf-8').strip()
    if temp_on == "":
        temp_on = current_temp_on

    stdscr.addstr(f"Current TEMP_OFF ({current_temp_off}): ")
    temp_off = stdscr.getstr().decode('utf-8').strip()
    if temp_off == "":
        temp_off = current_temp_off

    stdscr.addstr(f"Current SENSOR_NUMBER ({current_sensor_number}): ")
    sensor_number = stdscr.getstr().decode('utf-8').strip()
    if sensor_number == "":
        sensor_number = current_sensor_number

    new_values = {
        'FAN_PIN': int(fan_pin),
        'TEMP_ON': int(temp_on),
        'TEMP_OFF': int(temp_off),
        'SENSOR_NUMBER': int(sensor_number)
    }

    if update_config(new_values):
        stdscr.addstr("\nParameters updated successfully!\n")
    else:
        stdscr.addstr("\nError updating parameters!\n")
    stdscr.addstr("Press any key to return to menu...")
    stdscr.getch()
    curses.noecho()

def run_command(stdscr, command, message="Executing..."):
    stdscr.clear()
    stdscr.addstr(message + "\n")
    stdscr.refresh()
    try:
        subprocess.run(command, shell=True, check=True)
        stdscr.addstr("\nDone.\n")
    except subprocess.CalledProcessError as e:
        stdscr.addstr("\nError executing command.\n")
    stdscr.addstr("Press any key to return to menu...")
    stdscr.getch()

def main_menu(stdscr):
    curses.curs_set(0)
    menu = [
        "Modify Parameters", 
        "Reset/Restart Service", 
        "Enable/Start Service", 
        "Install Service", 
        "Uninstall Service", 
        "Quit"
    ]
    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr("NVMe Fan Control GUI\n", curses.A_BOLD | curses.A_UNDERLINE)
        stdscr.addstr("Use arrow keys to navigate and press Enter to select.\n\n")

        for idx, item in enumerate(menu):
            if idx == current_row:
                stdscr.addstr(f"> {item}\n", curses.A_REVERSE)
            else:
                stdscr.addstr(f"  {item}\n")

        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key in [10, 13]:
            if menu[current_row] == "Modify Parameters":
                modify_parameters(stdscr)
            elif menu[current_row] == "Reset/Restart Service":
                run_command(stdscr, "sudo systemctl restart nvme-fan.service", "Restarting service...")
            elif menu[current_row] == "Enable/Start Service":
                run_command(stdscr, "sudo systemctl enable nvme-fan.service && sudo systemctl start nvme-fan.service", "Enabling and starting service...")
            elif menu[current_row] == "Install Service":
                run_command(stdscr, f"sudo {INSTALL_SCRIPT}", "Running install script...")
            elif menu[current_row] == "Uninstall Service":
                run_command(stdscr, f"sudo {UNINSTALL_SCRIPT}", "Running uninstall script...")
            elif menu[current_row] == "Quit":
                break

    stdscr.clear()
    stdscr.addstr("Goodbye!\n")
    stdscr.refresh()
    curses.napms(1000)

def main():
    curses.wrapper(main_menu)

if __name__ == "__main__":
    main()
