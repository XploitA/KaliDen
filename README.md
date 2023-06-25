# KaliDen

KaliDen eliminates the dilemma of potentially destabilizing system packages while integrating Kali tools into a daily-use Linux distribution.

Historically, adding Kali tools to an everyday-use Linux distro has posed significant challenges. These tools typically need to be installed by building from source, fetching them from GitHub, or by incorporating Kali repositories into your sources.lst file – the latter is only possible if you're utilizing a Debian-based distribution.

Moreover, dual-booting or running Kali on bare metal presents its own set of problems, given Kali is not intended to be a daily-driver distribution.

KaliDen comes into play here. This Python script enables you to install Kali Linux within a chroot environment on any Linux distribution. By doing this, KaliDen circumvents the need for a baremetal Kali Linux installation or the modification of repository files in your distro for tool installation. This ensures the integrity and stability of your primary Linux environment while granting the power of Kali tools.

## Features

- Kali chroot environment has full access to device's hardware, which means tools like aircrack-ng suite, hashcat, will run out of the box, no configuration required.
- GUI support for tools installed inside Kali chroot (Wayland systems require the package xwayland)
- Supports creation of shared directories between the Kali chroot environment and host
- Faster performance than a virtual machine
- Supports updates and tool installation 

## Features under development

- Integration of Kali tools with the host system which will eleminate the need of starting kshell before running any Kali tool.
- A Seperate executable that will aid in installation of kali tools without starting the Kali chroot environment

## Installation

### Requirements
- Any Linux Distro 
- python3
- debootstrap

## Usage

- `sudo python3 kaliden.py -h` to see Usage
- `sudo python3 kaliden.py` to start the interactive installer
- `sudo python3 kaliden.py -R` OR `sudo python3 kaliden.py --R` to remove the chroot configuration.

## Known Issues

- Although the script creates installation directory if not present, if you choose to install the environment to a non-empty directory, the script does not check for a non-empty directory and installs the environment, which might messup any pre-existing files in that directory.   
