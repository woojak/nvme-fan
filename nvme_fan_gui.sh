#!/bin/bash
# NVMe Fan Control Extended Menu Script
# This script provides a graphical menu (using dialog) to:
#   1. Edit configuration parameters individually (with current values displayed)
#   2. Display service status (displayed until user closes the box)
#   3. Install the service
#   4. Uninstall the service
#   5. Restart the service
#   6. Start the service
#   7. Stop the service
#   8. Reset configuration to default settings
#   9. Exit

# Check if dialog is installed
if ! command -v dialog &> /dev/null; then
    echo "The 'dialog' command is not installed. Please install it using:"
    echo "sudo apt-get install dialog"
    exit 1
fi

# Define the path to the configuration file (nvme-fan.py)
CONFIG_FILE="nvme-fan.py"

# Function: Get the current value of a variable from the configuration file.
# This function extracts the first token (number or string) after the '=' sign.
get_current_value() {
    local var_name=$1
    grep -m1 "^$var_name *=" "$CONFIG_FILE" | sed -E "s/^[^=]*=[[:space:]]*([^#[:space:]]+).*/\1/"
}

# Function: Update a configuration variable in nvme-fan.py using sed.
update_config() {
    local var_name=$1
    local new_value=$2
    sed -i "s/^$var_name *= *.*/$var_name = $new_value/" "$CONFIG_FILE"
}

# Function: Edit an individual configuration variable.
edit_variable() {
    local var_name=$1
    local current_value
    current_value=$(get_current_value "$var_name")
    new_value=$(dialog --stdout --inputbox "Enter new value for $var_name (Current: $current_value):" 8 60)
    if [ -n "$new_value" ]; then
        update_config "$var_name" "$new_value"
        dialog --msgbox "$var_name updated to $new_value." 6 40
    fi
}

# Function: Edit configuration sub-menu.
edit_configuration() {
    while true; do
        current_fan_pin=$(get_current_value "FAN_PIN")
        current_temp_on=$(get_current_value "TEMP_ON")
        current_temp_off=$(get_current_value "TEMP_OFF")
        current_sensor=$(get_current_value "SENSOR_NUMBER")

        CHOICE=$(dialog --clear --backtitle "NVMe Fan Control" \
            --title "Edit Configuration" \
            --menu "Select a parameter to edit:" 18 70 6 \
            1 "FAN_PIN (Current: $current_fan_pin)" \
            2 "TEMP_ON (Current: $current_temp_on)" \
            3 "TEMP_OFF (Current: $current_temp_off)" \
            4 "SENSOR_NUMBER (Current: $current_sensor)" \
            5 "Back to Main Menu" \
            3>&1 1>&2 2>&3)

        case $CHOICE in
            1)
                edit_variable "FAN_PIN"
                ;;
            2)
                edit_variable "TEMP_ON"
                ;;
            3)
                edit_variable "TEMP_OFF"
                ;;
            4)
                edit_variable "SENSOR_NUMBER"
                ;;
            5)
                break
                ;;
        esac
    done
}

# Function: Show service status in a textbox until closed by the user.
show_service_status() {
    status=$(sudo systemctl status nvme-fan.service --no-pager)
    tmpfile=$(mktemp)
    echo "$status" > "$tmpfile"
    dialog --title "Service Status" --textbox "$tmpfile" 20 80
    rm "$tmpfile"
}

# Function: Reset configuration to default values.
reset_configuration() {
    update_config "FAN_PIN" "14"
    update_config "TEMP_ON" "50"
    update_config "TEMP_OFF" "45"
    update_config "SENSOR_NUMBER" "1"
    dialog --msgbox "Configuration reset to default values." 6 40
}

# Main menu loop.
while true; do
    CHOICE=$(dialog --clear --backtitle "NVMe Fan Control" \
        --title "Main Menu" \
        --menu "Choose an option:" 22 70 9 \
        1 "Edit Configuration" \
        2 "Service Status" \
        3 "Install Service" \
        4 "Uninstall Service" \
        5 "Restart Service" \
        6 "Start Service" \
        7 "Stop Service" \
        8 "Reset to Default Settings" \
        9 "Exit" \
        3>&1 1>&2 2>&3)

    case $CHOICE in
        1)
            edit_configuration
            ;;
        2)
            show_service_status
            ;;
        3)
            sudo ./install_nvme_fan.sh
            dialog --msgbox "Service installed." 6 40
            ;;
        4)
            sudo ./uninstall_nvme_fan.sh
            dialog --msgbox "Service uninstalled." 6 40
            ;;
        5)
            sudo systemctl restart nvme-fan.service
            dialog --msgbox "Service restarted." 6 40
            ;;
        6)
            sudo systemctl start nvme-fan.service
            dialog --msgbox "Service started." 6 40
            ;;
        7)
            sudo systemctl stop nvme-fan.service
            dialog --msgbox "Service stopped." 6 40
            ;;
        8)
            reset_configuration
            ;;
        9)
            break
            ;;
    esac
done

clear
echo "Exiting NVMe Fan Control Menu. Goodbye! 😊"
