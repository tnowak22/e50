# E50 - Scattered Field Measurement System

Fall '21 - Spring '22 Senior Design Group; Scattered Field Measurement System

The following repository documents work done for a senior design project at Marquette University. The group was tasked with creating an apparatus that would collect scattered field information from a known object. This repository documents the hardware and software that was used and any initial setup that was required.&#x20;

Refer to the wiki for additional information and guides.

***

The files that are present in this repository are as follows:

*   main\_control.py

    &#x20;   This is the main python file that is executed on the PC running the shockline software. It is responsible for initializing the VNA, data collection, processing the data, storing the data in a file, and executing a python script on the raspberry pi to advance the motor.

*   count\_numsteps.py

    &#x20;   This script was used to calibrate the rack and pinion track. It simply counts the number of steps while the motor is operating. We were able to obtain a ballpark estimate for the number of steps required for a full rotation of the motor around the track. Once this was known, we were able to fine tune the number of steps needed for 360 degree rotation.&#x20;

*   motor\_ccw\.py

    &#x20;   This script moves the motor counter clockwise. This script lives on the rapsberry pi.

*   motor\_cw\.py

    &#x20;   This script moves the motor clockwise. This script also lives on the rapsberry pi.&#x20;

*   motor\_original.py

    &#x20;   This was the original motor control python script from which motor\_cw.py and motor\_ccw.py originated. This was kept as a backup.&#x20;

***

## Cloning the Repository

If you are unfamiliar with git and git clone, the repository can be downloaded by navigating to the `Code` button above and hitting the _Download ZIP_ option. This downloads an archive of the repository and has the same effect as running a `git clone`.

![](https://github.com/tnowak22/e50/blob/main/wiki/images/clone_repo.png)

<p align="center">
  <img src="https://github.com/tnowak22/e50/blob/main/wiki/images/clone_repo2.png">
</p>

To use git to download the repository, run

```
git clone https://github.com/tnowak22/e50
```

To clone the wiki pages, run

```
git clone https://github.com/tnowak22/e50.wiki.git
```
This will download all of the wiki pages as _.md_ files, which can then be accessed using your preferred document viewer.
