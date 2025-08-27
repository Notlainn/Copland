import os
import inquirer
from colorama import Fore, Style, init, Back
from utils import *

log_file="/home/kali/Desktop/HTB/.last_machine_info"

banner()

if os.path.exists(log_file):
    reuse = str(input(Style.BRIGHT + input_color + "╚?╗" + Style.RESET_ALL + Style.BRIGHT + " Reuse last machine info? (s/n): " + input_color +""))
    if ( reuse == "s"):
        with open(log_file, "r") as file:
            line = file.readlines()
            machine_name = line[0].strip()
            machine_ip = line[1].strip()
            machine_OS = line[2].strip()
            machine_dns = line[3].strip()
            choose_func(machine_name, machine_ip, machine_dns)
    else:
        os.remove(log_file)

if not os.path.exists(log_file):

    "========MACHINE-INFO========"
    machine_name = str(input(Style.BRIGHT + input_color + "╚⊙╗" + Style.RESET_ALL + Style.BRIGHT + " Machine Name: " + input_color +""))
    machine_ip = str(input(Style.BRIGHT + input_color + "╔⊙╝" + Style.RESET_ALL + Style.BRIGHT +" Machine IP: " + input_color +""))
    machine_OS = str(input(Style.BRIGHT + input_color + "╚⊙╗" + Style.RESET_ALL + Style.BRIGHT +" Machine OS: " + input_color +""))

    "========CREATE-DIRECTORY========"
    create_dir(machine_name)

    "========GET-ICON========"
    get_icon(machine_name)

    "========GET-DNS========"
    machine_dns = get_dns(machine_name, machine_ip)

    "========SAVE-MACHINE-INFO========"
    with open(log_file, "w") as file:
        file.write(machine_name + "\n")
        file.write(machine_ip + "\n")
        file.write(machine_OS + "\n")
        file.write(machine_dns + "\n")
    
    "========CONFIGURE-DNS========"
    configure_dns(machine_dns, machine_ip)

    "========CONFIGURE-DNS========"
    choose_func(machine_name, machine_ip, machine_dns)
