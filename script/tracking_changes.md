The testing branch will serve as the main production branch. The master branch will preserve the original scripts that were used as a proof of concept.

# Tracking Changes

Changes made:

*   edited the master file; added functions to clean up the script

*   added a script to turn the motor clockwise (in one direction)

*   added a script to turn the motor counter clockwise&#x20;

*   created a script that will count the number of steps. this can be used to determine the number of steps for a complete rotation around the track. this will be used to compute the number of steps between txmit and receive antenna locations.

*   added a command line parser that makes it easier to pass arguments to the script

*   made the script a little more modular
    
    * executing the script on the raspberry pi can be done with a password or an ssh-key

    * the data file is now passed as a variable to each of the functions, rather than a global variable

Changes to be made:

*   ~~add a script to turn the motor counter clockwise (in the other direction)~~

*   ~~alter the master script to be able to select the direction of rotation~~

*   determine how to convert number of positions to steps or vice versa

    *   use the number of antennas provided to calculate the steps between each measurement position

    *   we will first need to determine how many steps are needed to make a full rotation around the track

    *   then a function can be used to calculate the steps and pass it on through the script


