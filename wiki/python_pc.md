## Python - Windows PC

In addition, we need to install python on the Windows PC that will be running the VNA software and connecting to the Raspberry Pi. This can be done by navigating to the python organization's [website](https://www.python.org/downloads/windows/) and downloading the desired version. Installing python on Windows should automatically install the pip package manager. For this project, **python version 3.10.2** was used. *Note, with python version 3.7, there were issues with importing the paramiko package.*

Finally, on the Windows PC, we need to install the `paramiko` python library. This library allows us to initialize a ssh client in any script. This will allow us to automatically log in to the Raspberry Pi when executing the script so that we can move the motor after we have collected data.&#x20;

To install the paramiko library, in the Windows command line, run:

    pip3 install paramiko

***
