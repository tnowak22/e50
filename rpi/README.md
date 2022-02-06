# Setting up the Raspberry Pi

This was done using a Raspberry Pi 4 Model B running the latest Raspberry Pi OS.&#x20;

We start by placing the Raspberry Pi into gadget mode. Gadget mode allows us to connect the Raspberry Pi to a PC as a USB device using only the USB-C power adapter. Doing so, we can both power the Raspberry Pi and send and receive data. Note that this method enables a low power mode on the Raspberry Pi. As such, we use a headless setup to minimize power consumption. This guide will not include installing the operating system. There are many guides available online, including from the Raspberry Pi Foundation's website.

***

## Gadget Mode

First, we need to make some changes to the configuration files on the Raspberry Pi OS. This is best done by plugging the micro-SD drive into your PC and editing the files in the root directory.&#x20;

Start by navigating to and opening `/boot/config.txt` and at the very end add the following: `dtoverlay=dwc2`.

Then, edit `/boot/cmdline.txt` and add: `modules-load=dwc2,g_ether` after "rootwait." This file is particular about formatting and spacing, so take caution when editing this file. The contents of the file should all be on a single line with a single space between each option listed.

Next, ensure that there is an empty file called `ssh` in the the `/boot/` directory. We have finished making the necessary changes to the OS. We can now replace the micro-SD into the Raspberry Pi and boot it up.&#x20;

If you are connecting from a Windows PC, then the [Bonjour Print Services](https://support.apple.com/kb/DL999?locale=en_US) from Apple are needed to connect to the Raspberry Pi via ssh.

Finally, we can connect to the Raspberry Pi through ssh from the PC using:

```bash
ssh pi@raspberrypi.local
```

***

## SSH Keys

Ssh keys are useful in allowing a user to login to a remote device without having to enter a password. Ssh keys can be configured to request an additional passphrase, but since we are not concerned with security, we will not be using this feature. Ssh keys consist of a private and public key (a pair of files) which are used to authenticate users. The private key is stored on the *remote user's* machine (and not to be shared), whereas the public key is deployed to *servers*. In this case, the *PC* is the remote user and the *Raspberry Pi* would be considered the server.

Since we are automating the process of data collection, we want to take advantage of this ability to run the script on the Raspberry Pi without user intervention/ authentication.

To generate a pair of ssh keys, on the remote user's machine run the `ssh-keygen` command. On Windows, this can be done through the command line or powershell. Go through the prompts that follow. I would recommend renaming the file to be something descriptive. Leave the passphrase prompt blank. Once complete, the ssh public and private keys will have been created and stored in the supplied directory. On Windows, ssh keys are typically stored in `C:\Users\<username>\.ssh`.&#x20;

To make use of the ssh-key, we need to transfer the ***public key*** to the *server*, in this case the Raspberry Pi. On Linux, ssh keys are stored in `/home/user/.ssh`. Transfering the file can simply be done by copying the file over using a USB drive. If the Raspberry Pi is connected to a Windows PC using *gadget mode*, this can also be done using the following command:

```bash
scp C:\Users\<username>\.ssh\ssh-public-key.pub pi@raspberrypi.local:/home/pi/.ssh

# more generally
scp C:\path\to\ssh-public-key.pub user@hostname.local:/home/user/.ssh
```

You will be prompted for the user's password. Of course, modify the command with the appropriate file names, usernames, and hostname of the Raspberry Pi, if it has been changed. This will store the public key in `/home/user/.ssh` on the Raspberry Pi.

On the server, or the Raspberry Pi, create a file called `authorized_keys` in `/home/user/.ssh`. We simply need to copy the contents of the public key file into the authorized keys file. This can be done using (modifying the file name as needed):

```bash
cat /home/user/.ssh/ssh-public-key.pub >> /home/user/.ssh/authorized_keys
```

Finally, to ssh in to the Raspberry Pi (in gadget mode) from a Windows PC, we need to specify the private key file using the `-i` option:

    ssh -i C:\Users\<username>\.ssh\ssh-private-key user@hostname.local

If it logs in without a password prompt, then the ssh keys are all set.&#x20;

***

## Python - Raspi

All of the coding done for this project used python. Before we begin running scripts on the Raspberry Pi, we need to make sure the environment is set and all the necessary python libraries are installed. This project was completed using python version 3.7.

Most Raspberry Pis come with python installed. Ensure that python3 is installed on the Raspi. In the terminal, run the command `python3 --version`. If it returns with "Python 3.X.X", then python3 is already installed. If not, run:

    sudo apt update
    sudo apt install python3

Next, check if pip3 is installed. In the same manner, in the terminal run `pip3 --version`. If it returns with a version number, then it is installed. If not, run:

    sudo apt install python3-pip

Next, we'll install the python libraries that are needed.

    pip3 install RPi.GPIO

The `RPi.GPIO` library will allow us to control the motor using the Raspberry Pi's general purpose input output pins. This will be used to interface with the motor driver.

***

*this could possibly be in its own section/ folder dedicated for setting up the Windows PC*

## Python - Windows PC

In addition, we need to install python on the Windows PC that will be running the VNA software and connecting to the Raspberry Pi. This can be done by navigating to the python organization's [website](https://www.python.org/downloads/windows/) and downloading the desired version. Installing python on Windows should automatically install the pip package manager.

Finally, on the Windows PC, we need to install the `paramiko` python library. This library allows us to initialize a ssh client in any script. This will allow us to automatically log in to the Raspberry Pi and then execute the script that will move the motor after we have collected data.&#x20;

To install the paramiko library, in the command line, run:

    pip3 install paramiko

***
