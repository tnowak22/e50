# Setting up the Raspberry Pi

This was done using a Raspberry Pi 4 Model B running the latest Raspberry Pi OS.&#x20;

We start by placing the Raspberry Pi into gadget mode. Gadget mode allows us to connect the Raspberry Pi to a PC as a USB device using only the USB-C power adapter. Doing so, we can both power the Raspberry Pi and send and receive data. Note that this method enables a low power mode on the Raspberry Pi. As such, we use a headless setup to minimize power consumption. This guide will not include installing the operating system. There are many guides available online, including from the Raspberry Pi Foundation's website.

***

First, we need to make some changes to the configuration files on the Raspberry Pi OS. This is best done by plugging the micro-SD drive into your PC and editing the files in the root directory.&#x20;

Start by navigating to and opening `/boot/config.txt` and at the very end add the following: `dtoverlay=dwc2`.

Then, edit `/boot/cmdline.txt` and add: `modules-load=dwc2,g_ether` after "rootwait." This file is particular about formatting and spacing, so take caution when editing this file.

Next, ensure that there is an empty file called `ssh` in the the `/boot/` directory. We have finished making the necessary changes to the OS. We can now replace the micro-SD into the Raspberry Pi and boot it up.&#x20;

If you are connecting from a Windows PC, then the [Bonjour Print Services](https://support.apple.com/kb/DL999?locale=en_US) from Apple are needed to connect the Raspberry Pi via ssh.

Finally, we can connect to the Raspberry Pi through ssh from the PC using:\


```bash
ssh pi@raspberrypi.local
```

***

