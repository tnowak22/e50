# System Overview

This page describes the basic working principles of the system. This project aimed to automate the process of data collection, however, complete automation was not achievable. The team decided to automate the process for each experiment. Subsequent experiments require repositioning the antenna and running the script afterwards.&#x20;

## Objective

The goal of this project is to measure the scattered field from a known object using microwaves. RF signals can be measured and generated using a vector network analyzer (VNA). The VNA allows us to measure the incident and reflected waves. We quantify these using scattering parameters, or s-parameters, which include the reflection and transmission coefficient. In this case, we are interested in the transmission coefficient s21, which is the ratio of the power incident at port 1 (trasmit antenna) to the power transmitted to port 2 (receive antenna). By probing the VNA, we can collect this data and store it.&#x20;

The idea is to have two antennas, one being the transmit and the other the receive antenna, to rotate around a known object and collect the scattered field information. For each experiment, the transmit antenna will be stationary and the receive antenna will rotate around the object, collecting data at predefined locations.&#x20;

## Motor & Track

To do this, we create a circular track where a rack and pinion gear are used to rotate an arm on which the receive antenna will be attached. A motor will attach to the pinion and be fixed to the arm. To automate data collection, we need to be able to control the motor precisely. The team chose a suitable stepper motor and motor driver, which can interface with an arduino or a raspberry pi. For this project, we decided to use python and, therefore, used a raspberry pi.&#x20;

## Antennas

For this project, we designed a monopole antenna with a ground plane. For an operating frequency of 3GHz, a quarter wavelength monopole has a length of 2.5cm. We tested the antennas using the VNA to confirm the center frequency.&#x20;

## VNA

The VNA can be connected to using sockets. Python offers a native sockets library to facilitate this connection. See the Shockline VNA's programming manual here. (link) The programming manual details how to probe the VNA for data. Before collecting data, we can set the trace parameters as desired. For example, we can set the trace to show either values in dB or in real + imaginary components. Once the trace parameters are set, we need to set a mark on the selected trace at the desired frequency. The following is taken from the VNA's API. Note, the following code is strictly the VNA's API, it does not include the surrounding python functions. See the programming manual or main\_control.py script to see how to set implement the VNA API in python code.&#x20;

```null
# to set the trace parameters to real/imaginary
:CALC1:PAR3:FORM REIM

# to set the mark at F frequency
:CALC1:PAR3:MARK1:X F
```

When we request data from the VNA, it is a two step process. First, we need to tell the VNA what data we want. This data will then be available in a buffer, which we have to request. This following code is taken from main\_control.py and shows the process. We first tell the VNA we are interested in the magnitude (`Y`) of s21 (`PAR3`) at the cursor (`MARK1`) we set earlier. Then, we receive the data and store it in a variable called `data`.

    vna.send(str.encode(":CALC1:PAR3:MARK1:Y?\n"))
    data = vna.recv(2056)

This is the general procedure for collecting data. We may also be interested in setting and configuring other parameters. Refer to the programming manual for more advanced configurations.&#x20;

## Raspberry Pi

There are wiki articles describing the set up of the raspberry pi for this project. Essentially, we use the raspberry pi's general purpose input output pins to generate pulses that will will serve as the control signals to the motor driver. The motor driver then supplies the appropriate amount of power to the windings. Two files are stored on the raspberry pi. One responsible for moving the motor clockwise and the other to move the motor counterclockwise.&#x20;

## Collecting Data & Moving the Motor

Since the main script is being executed on the client's Windows PC, we need to somehow connect to the raspberry pi to execute those scripts and turn the motor. This is done using gadget mode. The main script is responsible for the following

*   connecting to the vna

*   creating a csv file to store data

*   requesting and receiving data from the vna

*   write the data to the csv file

*   connecting to the raspberry pi

*   advance the motor, collect data, repeat for one full rotation

*   return the motor to the original position

