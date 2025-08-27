import requests
import os
import ast
import subprocess
import inquirer
import re
import time
import pyfiglet
from yaspin import yaspin
from yaspin.spinners import Spinners
from colorama import Fore, Style, init, Back
from inquirer.themes import Default
from blessed import Terminal
from urllib.parse import urlparse
from bs4 import BeautifulSoup

term = Terminal()

input_color = Fore.MAGENTA
error_color = Fore.RED
success_color = Fore.GREEN

class CustomTheme(Default):
    def __init__(self):
        super().__init__()
        # muda o símbolo do prompt
        self.Question.mark_color = term.magenta
        self.Question.brackets_color = term.magenta + term.bold
        self.Checkbox.selection_color = term.magenta + term.bold
        self.Checkbox.selected_icon = "[x]"
        self.Checkbox.selected_color = term.magenta + term.bold 
        self.List.selection_color = term.magenta + term.bold
        self.List.selection_cursor = ">"
        self.List.unselected_color = term.white + term.bold

def banner():
    f = pyfiglet.figlet_format("Copland", font="ansi_shadow")
    print(Style.BRIGHT + Fore.MAGENTA + "╔══════════════════════════════════════════════════════════╗\n\r\n")
    print(Style.BRIGHT + Fore.MAGENTA + f)
    text = Style.BRIGHT + Fore.MAGENTA + "╔══════════════════════════════════════════════════════════╝"

    with yaspin(Spinners.lainbar,text=Style.BRIGHT + input_color) as sp:
        time.sleep(2)
        sp.ok(text)

def execute_command(cmd, msg):

    with yaspin(Spinners.lovelain, text=msg, color="magenta") as sp:
        try:
            # bufsize=1 para line-buffered; text=True para strings
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                shell=True,
            )

            # Lê a saída em tempo real e imprime ACIMA do spinner
            for line in proc.stdout:
                sp.write(line.rstrip("\n"))

            proc.wait()

            if proc.returncode == 0:
                sp.write(Style.BRIGHT + success_color + "[⊙]" + Style.RESET_ALL + Style.BRIGHT +" Portscan Finished!")
            else:
                sp.fail("[⌀] ")

        except KeyboardInterrupt:
            proc.terminate()
            sp.write(error_color + "[⌀] Stopped!")
        except Exception as e:
            proc.terminate()
            sp.fail("[⌀] ")
            sp.write(f"Erro: {e}")

def create_dir(name):

    dir = '/home/kali/Desktop/HTB/{}'.format(name)

    try:
        os.mkdir(dir)
        print(Style.BRIGHT + success_color + "╔⊙╝" + Style.RESET_ALL + Style.BRIGHT + " Directory created at {}".format(dir))
    except FileExistsError:
        print(Style.BRIGHT + error_color + "╔⌀╝" + Style.RESET_ALL + Style.BRIGHT +" Directory already exist! :(")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_icon(name):

    try:
        cmd = 'curl -s https://www.hackthebox.com/machines/{} | grep "https://htb-mp-prod-public-storage.s3.eu-central-1.amazonaws.com/avatars" | cut -d "=" -f3 | sed "s/alt//" | head -n 1 | tr -d \\"'.format(name)
        output = subprocess.check_output(cmd,shell=True)
        print(Style.BRIGHT + success_color + "╚⊙╗" + Style.RESET_ALL + Style.BRIGHT + " Icon: " + input_color + "{}".format(output.decode().strip()))
    except:
        None

def get_dns(name, ip):

    machine_dns1 = None
    machine_dns2 = None

    try:

        r = requests.get("http://{}".format(ip), timeout=2, allow_redirects=False)

        try:
            #First way to get DNS
            url = r.headers[('Location')]
            parsed_url = urlparse(url)
            machine_dns1 = parsed_url.netloc
        except KeyError as e:
            None

        try:
            # Second way to get DNS
            pattern = r"\b[a-zA-Z0-9.-]+\.htb\b"
            matches = re.findall(pattern, r.text)[0]
            machine_dns2 = matches
        except IndexError as e:
            None

    except requests.exceptions.ConnectTimeout as e:
        None
     
    if (machine_dns1 != None):
        name = machine_dns1
    elif (machine_dns2 != None):
        name = machine_dns2
    else:
        name = name + '.htb' 
    
    return name

def configure_dns(name, ip):
 
    try:
        cmd = 'echo "{} {}" | sudo tee -a /etc/hosts > /dev/null'.format(ip, name)
        verify = subprocess.check_output('grep -w "{} {}" /etc/hosts'.format(ip, name),shell=True)
    except subprocess.CalledProcessError as e:
        output = subprocess.check_output(cmd,shell=True)
        print(Style.BRIGHT + success_color + "╔⊙╝" + Style.RESET_ALL + Style.BRIGHT + "{} {} added to /etc/hosts".format(ip, name))

def choose_func(name, ip, dns):
    questions = [
    inquirer.Checkbox("modes",message=Style.BRIGHT + "Choose functions to use (backspace)",
                              choices=['portscan', 'fuzzDns', 'fuzzDir'],
                     ),
            ]
    global mode
    mode = inquirer.prompt(questions, theme=CustomTheme())

    global machine_name
    global machine_ip
    global machine_dns

    machine_name = name
    machine_ip = ip
    machine_dns = dns

    for func in mode["modes"]:
        globals()[func]()
 
def portscan():

    msg = Style.BRIGHT + input_color + Style.BRIGHT +"Running portscan..."
    cmd = "rustscan -r 1-65535 --ulimit 5000 -t 2000 -a {} -- -v -sV -Pn -oN /home/kali/Desktop/HTB/{}/scan.txt 2> /dev/null".format(machine_ip, machine_name)
    execute_command(cmd, msg)

def fuzzDns():

    port = str(input(Style.BRIGHT + input_color + "[⊙]" + Style.RESET_ALL + Style.BRIGHT + " Insert port: " + input_color +""))
    print(Style.BRIGHT + success_color + "[⊙]" + Style.RESET_ALL + Style.BRIGHT + " Subdomains found: " + input_color +"")
    msg = Style.BRIGHT + input_color + "Running DNS fuzzing... "
    cmd = 'ffuf -s -c -u http://{}:{} -H "Host: FUZZ.{}" -w /usr/share/seclists/Discovery/DNS/n0kovo_subdomains.txt -t 100 -ac'.format(machine_dns, port, machine_dns)
    execute_command(cmd, msg)

def fuzzDir():

    port = str(input(Style.BRIGHT + input_color + "[⊙]" + Style.RESET_ALL + Style.BRIGHT + " Insert port: " + input_color +""))
    wordlist = [
        inquirer.List(
            "files",
            message=Style.BRIGHT + "Select wordlist",
            choices=["quickhits.txt", "fuzz-Bo0oM-friendly.txt", "raft-large-directories.txt"],
        ),
    ]
    answer = inquirer.prompt(wordlist, theme=CustomTheme())

    print(Style.BRIGHT + success_color + "[⊙]" + Style.RESET_ALL + Style.BRIGHT + " Directory/Files found: " + input_color +"")
    msg = Style.BRIGHT + input_color + "Running directory fuzzing..."
    cmd = 'ffuf -s -c -u http://{}:{}/FUZZ -w wordlists/{} -mc 200,301,403'.format(machine_dns, port, answer["files"])
    execute_command(cmd, msg)