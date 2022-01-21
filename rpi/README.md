# Setting up the Raspberry Pi

This was done using a Raspberry Pi 4 Model B running the latest Raspberry Pi OS.&#x20;

We start by placing the Raspberry Pi into gadget mode. Gadget mode allows us to connect the Raspberry Pi to a PC as a USB device using only the USB-C power adapter. Doing so, we can both power the Raspberry Pi and send and receive data. Note that this method enables a low power mode on the Raspberry Pi. As such, we use a headless setup to minimize power consumption. This guide will not include installing the operating system. There are many guides available online, including from the Raspberry Pi Foundation's website.

***

## Gadget Mode

First, we need to make some changes to the configuration files on the Raspberry Pi OS. This is best done by plugging the micro-SD drive into your PC and editing the files in the root directory.&#x20;

Start by navigating to and opening `/boot/config.txt` and at the very end add the following: `dtoverlay=dwc2`.

Then, edit `/boot/cmdline.txt` and add: `modules-load=dwc2,g_ether` after "rootwait." This file is particular about formatting and spacing, so take caution when editing this file.

Next, ensure that there is an empty file called `ssh` in the the `/boot/` directory. We have finished making the necessary changes to the OS. We can now replace the micro-SD into the Raspberry Pi and boot it up.&#x20;

If you are connecting from a Windows PC, then the [Bonjour Print Services](https://support.apple.com/kb/DL999?locale=en_US) from Apple are needed to connect the Raspberry Pi via ssh.

Finally, we can connect to the Raspberry Pi through ssh from the PC using:\\

```bash
ssh pi@raspberrypi.local
```

***

## SSH Keys

Ssh keys are useful in allowing a user to login to a remote device without having to enter a password. Ssh keys can be configured to request an additional passphrase, but since we are not concerned with security, we will not be using this feature. Ssh keys consist of a private and public key (a pair of files) which are used to authenticate users. The private key is stored on the *remote user's* machine (and not to be shared), whereas the public key is deployed to *servers*. In this case, the *PC* is the remote user and the *Raspberry Pi* would be considered the server.

Since we are automating the process of data collection, we want to take advantage of this ability to run the script on the Raspberry Pi without user intervention/ authentication.

To generate a pair of ssh keys, on the remote user's machine run the `ssh-keygen` command. Go through the prompts that follow. I would recommend renaming the file to be something descriptive. Leave the passphrase prompt blank. Once complete, the ssh public and private keys will have been created and stored in the supplied directory. On Windows, ssh keys are typically stored in `C:\Users\<username>\.ssh`.&#x20;

To make use of the ssh-key, we need to transfer the ***public key*** to the *server*, in this case the *Raspberry Pi*. On Linux, ssh keys are stored in `/home/user/.ssh`. Transfering the file can simply be done by copying the file over using a USB drive. If the Raspberry Pi is connected to a Windows PC using *gadget mode*, this can also be done using the following command:

```bash
scp C:\Users\<username>\.ssh\ssh-public-key.pub pi@raspberrypi.local:/home/pi/.ssh

# more generally
scp C:\path\to\ssh-public-key.pub user@hostname.local:/home/user/.ssh
```

You will be prompted for the user's password. Of course, modify the command with the appropriate file names, usernames, and hostname of the Raspberry Pi, if it has been changed. This will store the public key in `/home/pi/.ssh` on the Raspberry Pi.

On the server, or the Raspberry Pi, create a file called `authorized_keys` in `/home/user/.ssh`. We simply need to copy the contents of the public key file into the authorized keys file. This can be done using (modifying the file name as needed):

```bash
cat /home/user/.ssh/ssh-public-key.pub >> /home/user/.ssh/authorized_keys
```
