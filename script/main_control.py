import time 
import sys
import csv 
import socket
import os.path
import pyfiglet
import argparse                     # parser for command line arguments
from paramiko import SSHClient      # import the ssh client package

# this script will take several input arguments
# 1. location of file to store the data (data_file)
# 2. # of antennas (num_antennae)
# 3. experiment number (exp_number)
# 4. raspi user (raspi_user)
# 5. raspi hostname (raspi_hostname)
# ONE of the following are necessary:
# 6. raspi password (raspi_pwd) (optional)
# 7. raspi ssh-key (raspi_key) (optional)

# move the motor in the counter clockwise direction
def move_motor_ccw(host, user, raspi_key, raspi_pwd, steps):
    # establish the SSHClient so we can login & execute a script on the raspberry pi
    client = SSHClient()                # load the sshclient object
    client.load_system_host_keys()      # load system host keys (this is necessary to load the known-hosts file)

    # check which authentication method is used, use the appropriate one
    if (raspi_key == 'empty'):
        client.connect(host, username=user, password=raspi_pwd)                  # connect to the raspi with the host, user, and ssh private key
        stdin, stdout, stderr = client.exec_command('/home/yagi/venv/bin/python3 /home/yagi/motor/motor_ccw.py %d' %(steps))      # execute the desired file on the rpi
    else:
        client.connect(host, username=user, key_filename=raspi_key)                   # connect to the raspi with the host, user, and ssh private key
        stdin, stdout, stderr = client.exec_command('/home/yagi/venv/bin/python3 /home/yagi/motor/motor_ccw.py %d' %(steps))      # execute the desired file on the rpi

    # check for errors
    if stderr.read() == b'':   
        for line in stdout.readlines():   
            print(line.strip()) # strip the trailing line breaks   
    else:   
        print(stderr.read())

# move the motor clockwise
def move_motor_cw(host, user, raspi_key, raspi_pwd, steps):
    # establish the sshclient to connect to the raspberry pi
    client = SSHClient()                # load the sshclient object
    client.load_system_host_keys()      # load system host keys (may not be necessary when specifying the keyfile)
    
    #check which authentication method was used
    if (raspi_key == 'empty'):
        client.connect(host, username=user, password=raspi_pwd)                        # connect to the raspi with the host, user, and ssh private key
        stdin, stdout, stderr = client.exec_command('/home/yagi/venv/bin/python3 /home/yagi/motor/motor_cw.py %d' %(steps))      # execute the desired file on the rpi
    else :
        client.connect(host, username=user, key_filename=raspi_key)                        # connect to the raspi with the host, user, and ssh private key
        stdin, stdout, stderr = client.exec_command('/home/yagi/venv/bin/python3 /home/yagi/motor/motor_ccw.py %d' %(steps))      # execute the desired file on the rpi
    
    # check for errors
    if stderr.read() == b'':   
        for line in stdout.readlines():   
            print(line.strip()) # strip the trailing line breaks   
    else:   
        print(stderr.read())  

def get_args():
    # get the command line arguments that are passed to the script
    # the arguments WITHOUT double hyphens are positional and are REQUIRED (and be passed in the order listed)
    # the arguments WITH double hyphens are optional (but ONE of the two is required)
    parser = argparse.ArgumentParser(description="Lets collect some data, shall we? Visit https://github.com/tnowak22/e50 to find more specific instructions regarding usage and an overview of the project, project files, and other pertinent information.")
    parser.add_argument('data_file', help='Location of the file that will store data.')
    parser.add_argument('num_antennae', help='The number of tx/rx antenna locations.')
    parser.add_argument('exp_number', help='The iteration number or the experiment number.')
    parser.add_argument('rpi_user', help='Login username for the raspberry pi.')
    parser.add_argument('rpi_hostname', help='Hostname of the raspberry pi.')
    parser.add_argument('--rpi_pwd', help='Login password for the provided user of the raspberry pi.', default='empty')
    parser.add_argument('--ssh_key', help='Alternatively, login using a private ssh-key. Note: the public key must be properly stored on the raspberry pi.', default='empty')

    args = parser.parse_args()

    data_file = args.data_file
    num_antennae = args.num_antennae
    exp_number = args.exp_number
    raspi_user = args.rpi_user
    raspi_hostname = args.rpi_hostname
    raspi_pwd = args.rpi_pwd
    raspi_key = args.ssh_key

    # ensure that one of the authentication methods is passed
    if ((raspi_pwd == 'empty') and (raspi_key == 'empty')):
        print("Error: No credentials have been passed. Please either enter the raspberry pi user's password or supply an ssh-key.")
    else:
        return data_file, num_antennae, exp_number, raspi_user, raspi_hostname, raspi_pwd, raspi_key

def init_vna():
    # Initialize the connection with the shockline software
    # The shockline interface will be greyed out if this is successful
    global vna
    vna = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    vna.connect(("127.0.0.1", 5001))

    # Set the desired trace parameters
    # S21
    # vna.send(str.encode(":CALC1:PAR3:FORM REIM\n"))
    # vna.send(str.encode(":CALC1:PAR3:MARK1:X 3E9\n"))
    # S12 - initialize and set mark
    vna.send(str.encode(":CALC1:PAR2:FORM REIM\n"))
    vna.send(str.encode(":CALC1:PAR2:MARK1:X 3E9\n"))  
    # S11 - initialize & set mark
    vna.send(str.encode(":CALC1:PAR1:MARK1:X 3E9\n"))
    # S22 - initialize & set mark
    vna.send(str.encode(":CALC1:PAR4:MARK1:X 3E9\n"))

def does_file_exist(data_file):
    # check if the supplied data file exists
    # if it doesnt exist, create it and initialize the data to be stored
    if os.path.isfile(data_file) == True:
        print('The specified file already exists. Continuing...')
    else:
        print('The file does not exist. Creating a new file...')
        with open(data_file, 'w', newline='') as newFile:
            # after creating the file, we want to initialize the variables that will be stored
            header = csv.writer(newFile, delimiter='\t')
            header.writerow(['Position', 'Experiment','S11 - LogMag' ,'S22 - LogMag' ,'S12 - Real', 'S12 - Imag'])

def get_vna_data():
    # get data from the vna
    # to obtain different data modify this function
    # vna.send(str.encode(":CALC1:PAR3:MARK1:Y?\n"))
    # data = vna.recv(2056)

    # get s11 data (refl. coeff of transmit)
    vna.send(str.encode(":CALC1:PAR1:MARK1:Y?\n"))
    s11 = vna.recv(2056)
    # get s12 data (out at 1 in at 2) - total field
    vna.send(str.encode(":CALC1:PAR2:MARK1:Y?\n"))
    s12 = vna.recv(2056)
    # get s22 data (refl. coeff of receive)
    vna.send(str.encode(":CALC1:PAR4:MARK1:Y?\n"))
    s22 = vna.recv(2056)
    return s11.decode(), s12.decode(), s22.decode()

def process_data(data):
    s11, s12, s22 = data
    # print(s11)
    # print(s22)
    # print(s21)
    # AT THIS POINT WE HAVE WHAT WE NEED, THE REST IS AESTHETIC... #

    s11_a, s11_b = s11.split('E')
    s22_a, s22_b = s22.split('E')

    # split s12 into real and imag
    real, imag = s12.split(',')

    # convert everything to floats
    s11_a = float(s11_a)
    s11_b = float(s11_b[3])
    s22_a = float(s22_a)
    s22_b = float(s22_b[3])
    real = float(real)
    imag = float(imag)

    final_data = []
    # convert scientific notation to decimal
    final_data.append(format(s11_a * pow(10, s11_b), '.8f'))
    final_data.append(format(s22_a * pow(10, s22_b), '.8f'))
    final_data.append(real)
    final_data.append(imag)

    return final_data

def write_data(data_file, position, experiment, data):
    # now we can write the data to the created csv file
    with open(data_file, 'a', newline='') as f:
        data_in = csv.writer(f, delimiter='\t')     # we need to initialize the object that writes data
        s11, s22, s12_real, s12_imag = data
        # now we append this data to the csv file
        data_in.writerow([position, experiment, s11, s22, s12_real, s12_imag])
        time.sleep(1)

def steps_forward(num_antennae):
    num_positions = num_antennae
    steps_for_full_rotation = 29700

    steps_increment = steps_for_full_rotation / num_positions
    return steps_increment

def steps_reverse(num_antennae):
    num_positions = num_antennae
    steps_for_full_rotation = 29700

    steps_increment = steps_for_full_rotation / num_positions
    steps_to_return_to_start = steps_for_full_rotation - (steps_increment * 3)
    return steps_to_return_to_start

def main():
    # get the input arguments:
    arguments = get_args()
    data_file = arguments[0]
    num_antennae = int(arguments[1])
    exp_number = int(arguments[2])
    raspi_user = arguments[3]
    raspi_hostname = arguments[4]
    raspi_pwd = arguments[5]
    raspi_key = arguments[6]

    # print the banner
    banner = pyfiglet.figlet_format("Scattered Field Measurement", font = "doom", width=100 )
    print(banner)
    print("Courtesy Senior Design Team E50. Marquette University 2021-2022.\n\n")
    print("The main_control.py script is now running. To EXIT, press CTRL+C.\n\n")

    # calculate the number of steps needed based on 
    # the number of antenna locations
    # note that we calibrated the system to determine how many steps were needed
    # for one full rotaion. this is hard coded in the two functions below
    steps_forw = steps_forward(num_antennae)
    steps_rev = steps_reverse(num_antennae)

    # first check if the data file exists
    does_file_exist(data_file)

    # initialize the vna
    init_vna()

    # we'll loop over the number of positions (# of receive antenna locations)
    # collect data, process, save to file, move motor, repeat
    # the number of times the motor will move forward will be the number of antenna locations - 2
    position = 0
    num_positions = num_antennae - 2

    for i in range(0, num_positions, 1):
        # get the data from vna
        data = get_vna_data()
        # process the data
        final_data = process_data(data)
        # write the data to file
        write_data(data_file, position, exp_number, final_data)
        # move the motor to the next position
        move_motor_ccw(raspi_hostname, raspi_user, raspi_key, raspi_pwd, steps_forw)
        # wait for the system to settle
        time.sleep(3)
        # increment the position by 1
        position = position + 1

    # move motor to original position +1 for the next experiment
    # need to write a function to calculate the number of steps needed to return
    # to the original position
    move_motor_cw(raspi_hostname, raspi_user, raspi_key, raspi_pwd, steps_rev)

if __name__ == "__main__":
    main()