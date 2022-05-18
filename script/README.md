# README

This folder contains all of the python script files that were used for this project. The following is a short description of each of the files. 

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
    
The most important script files will be the _main\_control.py_ and _motor\_ccw.py_ and _motor\_cw.py_. The _main\_control.py_ script will need to be executed from the user's PC running the Shockline software. The _motor\_ccw.py_ and _motor\_cw.py_ files are present on the raspberry pi and should not need to be modified. 
