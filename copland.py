import os
import inquirer
from colorama import Fore, Style, init, Back
from utils import *

log_file="/home/kali/Desktop/HTB/.last_machine_info"

#banner()

if os.path.exists(log_file):
    reuse = str(input(Style.BRIGHT + input_color + "╚?╗" + Style.RESET_ALL + Style.BRIGHT + " Reuse last machine info? (y/n): " + input_color +""))
    if ( reuse == "y"):
        with open(log_file, "r") as file:
            line = file.readlines()
            machine_name = line[0].strip()
            machine_ip = line[1].strip()
            machine_OS = line[2].strip()
            machine_dns = line[3].strip()
            machine_user = line[4].strip()
            machine_pass = line[5].strip()
            assumed_breach = line[6].strip()
            print(machine_user)
            print(machine_pass)
            verifyOS(machine_name, machine_ip, machine_dns, machine_OS, machine_user, machine_pass, assumed_breach)
    else:
        os.remove(log_file)

if not os.path.exists(log_file):

    "========MACHINE-INFO========"
    machine_name = str(input(Style.BRIGHT + input_color + "╚⊙╗" + Style.RESET_ALL + Style.BRIGHT + " Machine Name: " + input_color +""))
    machine_ip = str(input(Style.BRIGHT + input_color + "╔⊙╝" + Style.RESET_ALL + Style.BRIGHT +" Machine IP: " + input_color +""))
    #machine_OS = str(input(Style.BRIGHT + input_color + "╚⊙╗" + Style.RESET_ALL + Style.BRIGHT +" Machine OS: " + input_color +""))
    question = [
        inquirer.List(
        "files",
        message=Style.BRIGHT + input_color +" Machine OS " + Style.RESET_ALL,
        choices=["windows", "linux"]
        ),
    ]
    machine_OS = inquirer.prompt(question, theme=CustomTheme())

    "========GET-CREDS========"
    assumed_breach = str(input(Style.BRIGHT + input_color + "╔?╝" + Style.RESET_ALL + Style.BRIGHT +" Assumed Breach (y/n): " + input_color +""))
    if ( assumed_breach == "y"):

        machine_user = str(input(Style.BRIGHT + input_color + "╚⊙╗" + Style.RESET_ALL + Style.BRIGHT +" Machine user: " + input_color +""))
        machine_pass = str(input(Style.BRIGHT + input_color + "╔⊙╝" + Style.RESET_ALL + Style.BRIGHT +" Machine pass: " + input_color +""))
    else:
        machine_user = ""
        machine_pass = ""

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
        file.write(machine_OS["files"] + "\n")
        file.write(machine_dns + "\n")
        file.write(machine_user + "\n")
        file.write(machine_pass + "\n")
        file.write(assumed_breach + "\n")

    "========CONFIGURE-DNS========"
    configure_dns(machine_dns, machine_ip)

    "========IDENTIFY-OS========"
    verifyOS(machine_name, machine_ip, machine_dns, machine_OS["files"], machine_user, machine_pass, assumed_breach)

