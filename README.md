# KaliDen
KaliDen eliminates the dilemma of potentially destabilizing system packages while integrating Kali tools into a daily-use Linux distribution.

Historically, adding Kali tools to an everyday-use Linux distro has posed significant challenges. These tools typically need to be installed by building from source, fetching them from GitHub, or by incorporating Kali repositories into your sources.lst file – the latter is only possible if you're utilizing a Debian-based distribution.

Moreover, dual-booting or running Kali on bare metal presents its own set of problems, given Kali is not intended to be a daily-driver distribution.

KaliDen comes into play here. This Python script enables you to install Kali Linux within a chroot environment on any Linux distribution. By doing this, KaliDen circumvents the need for a baremetal Kali Linux installation or the modification of repository files in your distro for tool installation. This ensures the integrity and stability of your primary Linux environment while granting the power of Kali tools.

