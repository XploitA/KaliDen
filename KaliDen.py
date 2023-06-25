import os
import subprocess
import argparse

# Banner
BANNER = """

██╗  ██╗ █████╗ ██╗     ██╗██████╗ ███████╗███╗   ██╗
██║ ██╔╝██╔══██╗██║     ██║██╔══██╗██╔════╝████╗  ██║
█████╔╝ ███████║██║     ██║██║  ██║█████╗  ██╔██╗ ██║
██╔═██╗ ██╔══██║██║     ██║██║  ██║██╔══╝  ██║╚██╗██║
██║  ██╗██║  ██║███████╗██║██████╔╝███████╗██║ ╚████║
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═══╝
                                        version(1.0)                    
"""

# Colors for terminal outputs
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RESET = "\033[0m"
DARK_GREEN = "\033[0;32m"
BLUE_BOLD = "\033[1;34m"

# Symbols
COG = "\u2699"
CHECK = "\u2713"
CROSS = "\u2717"
ARROW = "\u27a4"
STAR = "\u269d"
coffee_cup = '\u2615'

# Utility function to print colored outputs
def print_color(color, msg):
    print(f"{color}{msg}{RESET}")

# Checks if debootstrap is installed
def is_debootstrap_installed():
    try:
        output = subprocess.run(["debootstrap", "--help"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return True
    except FileNotFoundError:
        return False

# Creates the chroot environment and installs Kali Linux in it
def create_environment(directory):
    print_color(YELLOW, f"{COG}  Creating kali environment at {directory}\n")
    os.makedirs(directory, exist_ok=True)
    
    print_color(GREEN, f"{CHECK}  Directories created at {directory}\n")

    command = "debootstrap"
    args = ["kali-rolling", directory , "http://http.kali.org/kali"]
    print_color(YELLOW, f"{CYAN}{STAR}  This might take a while, lean back and have some coffee {coffee_cup}.{RESET}\n ")
    process = subprocess.Popen([command] + args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    for line in process.stdout:
        print_color(DARK_GREEN,f"{COG}  " + line.strip())
        if "Failed" in line or "Error" in line:
            print_color(RED, f"\n{CROSS}  Error or failure detected in debootstrap output. Exiting.\n")
            exit()

    os.makedirs(f"{directory}/root/shared", exist_ok=True)

# Creates backup of the current fstab configuration and configures automounts
def configure_environment(directory, shared_dir=None):
    source_file = '/etc/fstab'
    backup_file = '/etc/fstab.bak_prekd'
    print_color(YELLOW, f"\n{COG}  Creating backup of fstab file at /etc/fstab.bak_prekd .\n")

    result = subprocess.run(['sudo', 'cp', source_file, backup_file], capture_output=True)

    if result.returncode != 0:
        print_color(RED, f"{CROSS}  Failed to create backup. Exiting.\n")
        print(result.stderr.decode())
        exit()

    print_color(GREEN, f"{CHECK}  Backup created successfully.\n")

    mounts = [f"/dev    {directory}/dev    none    bind    0    0",
              f"/proc   {directory}/proc    none    bind    0    0",
              f"/sys    {directory}/sys    none    bind    0    0",
              f"newinstance  {directory}/dev/pts    devpts    defaults,newinstance    0   0"] 
    if shared_dir:
        mounts.append(f"{shared_dir}    {directory}/root/shared    none    bind    0    0")

    config = ["", "# Kali Chroot setup", *mounts]

    try:
        with open(source_file, 'a') as file:
            file.write('\n'.join(config) + '\n')
    except IOError as e:
        print_color(RED, f"{CROSS}  Failed to write to fstab: {e}. Exiting.\n")
        exit()

    if shared_dir:
        print_color(GREEN, f"{CHECK}  Auto-mounts and shared directory configured successfully.\n")
    else:
        print_color(GREEN, f"{CHECK}  Auto-mounts configured successfully.\n")

# Creates /usr/local/bin/kshell chroot loader
def create_executable(directory):
    path="/usr/local/bin/kshell"

    try:
        with open(path, "w") as f:
            f.write(f"""#!/bin/bash
            CHROOT_PATH="{directory}"
            xhost +local:
            clear
            chroot $CHROOT_PATH
            """)
        os.system("chmod +x /usr/local/bin/kshell")
    except Exception as e:
        print_color(RED, f"{CROSS}  Failed to create kshell: {e}. Exiting.\n")
        exit()

# Installer function that drives the whole installation process
def post_install(directory):
    pidirectory = directory 
    postinstall = subprocess.run(['sudo', 'chroot', pidirectory, "/./postinstall.sh"], capture_output=True)
        


def install_environemnt():
    if not is_debootstrap_installed():
        print_color(RED, f"{CROSS}  debootstrap is not installed exiting.\n")
        exit()
    directory = input(f"{CYAN}{STAR}  Enter a path where you wish to install the kali chroot environment [Default /chroot/kali].{RESET}\n{ARROW} ")
    directory = directory or "/chroot/kali"
    directory = os.path.normpath(directory)
    
    while True:
        mount_confirmation = input(f"\n{CYAN}{STAR}  Important! Do you want to mount dev, proc and sys to the chroot environment? This will modify the current fstab configuration to auto-mount /dev /proc and /sys as soon as the system boots.[y/n]{RESET}\n{ARROW} ").lower()
        if not mount_confirmation:
            pass
        else:
            break
    shared_dir = None
    if mount_confirmation == "y":
        while True:
            share_confirmation = input(f"\n{CYAN}{STAR}  Do you want to create a shared directory between the kali chroot environment and the host?{RESET}\n{ARROW} ").lower()
            if share_confirmation == "y":
                shared_dir = input(f"\n{CYAN}{STAR}  Enter path to the directory which you want to share.{RESET}\n{ARROW} ")
                shared_dir = os.path.normpath(shared_dir)
                if shared_dir == "":
                    print_color(RED, f"\n{CROSS}  Shared directory path cannot be empty. Retry.\n")
                    pass
                elif os.path.isdir(shared_dir):
                    print_color(YELLOW, f"\n{COG}  Initiating installation at {directory}\n")
                    create_environment(directory)
                    configure_environment(directory, shared_dir)
                    print_color(GREEN, f"{CHECK}  Kali chroot environment created at {directory}\n")
                    break
                else:
                    print_color(RED, f"\n{CROSS}  Shared directory path does not exist. Retry.\n")
                    pass
            else:
                shared_dir = ""
                print_color(YELLOW, f"\n{COG}  Initiating installation at {directory}\n")
                create_environment(directory)
                configure_environment(directory, shared_dir)
                break
    else:
        print_color(YELLOW, f"\n{COG}  Initiating installation at {directory}\n")
        create_environment(directory)
        print_color(CYAN, f"{STAR}  Kali chroot environment created at " + directory + " Without mounting dev, proc, and sys. Some functions might not work properly.\n" )     

    print_color(YELLOW, f"{COG}  Creating executable named kshell at /usr/local/bin\n")
    create_executable(directory)
    print_color(GREEN, f"{CHECK}  Executable named kshell was created.\n")
    print_color(CYAN, f"{STAR}  Reboot the system and then you can enter the command \"sudo kshell\" to start a kali shell.\n")

# Revert function
def revert_environment():
    # Revert fstab
    source_file = '/etc/fstab'
    backup_file = '/etc/fstab.bak_prekd'
    print_color(YELLOW, f"{COG}  Restoring fstab file from /etc/fstab.bak_prekd.\n")
    result = subprocess.run(['sudo', 'mv', backup_file, source_file], capture_output=True)
    if result.returncode != 0:
        print_color(RED, f"{CROSS}  Failed to restore fstab. Check if the backup file exists.\n")
        print(result.stderr.decode())
    else:
        print_color(GREEN, f"{CHECK}  fstab file restored successfully.\n")

    # Remove kshell
    path="/usr/local/bin/kshell"
    if os.path.isfile(path):
        print_color(YELLOW, f"{COG}  Removing kshell.\n")
        os.remove(path)
        print_color(GREEN, f"{CHECK}  kshell removed successfully.\n")
    else:
        print_color(RED, f"{CROSS}  kshell not found.\n")

    print(f"{CYAN}{STAR}  To remove the environment completely reboot the system and delete the chroot environment manually by using \"{RESET}{GREEN}sudo rm -rf <path to chroot>{RESET}{CYAN}\"{RESET}\n")

def main():
    print_color(BLUE_BOLD, BANNER)
    username=subprocess.check_output(['whoami']).decode('utf-8')
    parser = argparse.ArgumentParser(description=f"{CYAN}{STAR}  Run the script without any arguments to install the Kali Linux inside a chroot environment.{RESET}\n")
    parser.add_argument("-R", "--revert", action="store_true", help="Revert the Kali chroot environment")
    args = parser.parse_args()
    if "root" not in username:
        print_color(RED, f"{CROSS}  Run this script with sudo.\n")
        exit()
    else:
        pass
    if args.revert:
        revert_environment()
    else:
        install_environemnt()

if __name__ == "__main__":
    main()
