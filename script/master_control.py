import time 
import sys
import csv 
import socket
import os.path
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
    vna.send(str.encode(":CALC1:PAR3:FORM REIM\n"))
    vna.send(str.encode(":CALC1:PAR3:MARK1:X 3E9\n"))

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
            header.writerow(['Position', 'Experiment', 'Real & Imag Field'])

def get_vna_data():
        # get data from the vna
        # to obtain different data modify this function
        vna.send(str.encode(":CALC1:PAR3:MARK1:Y?\n"))
        data = vna.recv(2056)
        return data

def process_data(data):
        # this function is responsible for processing the data into a usable format
        string = data.decode("utf-8")
        string = string.strip()
        
        split = string.split("\\")    # remove the leading B
        split2 = split[0].split(',')   # split the items by the backslashes
        
        num = []
        
        # ***** we can keep it in scientific notation ******
        # now we need to split the 'E' from the real/imaginary parts
        for i in range(len(split2)):
            num.append(split2[i].split("E"))
            
        num2 = []
        
        # creating a new list to remove the nested list
        for i in range(0, len(num)):
            for j in range(0, len(num[i])):
                num2.append(num[i][j])
        
        # converting all the strings in the list to floats
        for i in range(len(num2)):
                num2[i] = float(num2[i])

        # at this point we can work with the data
        processed_data = []
        
        # convert scientific notation to decimal
        # round to 6 decimal places
        processed_data.append(format(num2[0] * pow(10, num2[1]), '.8f'))
        processed_data.append(format(num2[2] * pow(10, num2[3]), '.8f'))
        return processed_data

def write_data(data_file, position, experiment, data):
    # now we can write the data to the created csv file
    with open(data_file, 'a', newline='') as f:
        data_in = csv.writer(f, delimiter='\t')     # we need to initialize the object that writes data
       
        # now we append this data to the csv file
        data_in.writerow([position, experiment, data])
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
        move_motor_cw(raspi_hostname, raspi_user, raspi_key, raspi_pwd, steps_forw)
        # wait for the system to settle
        time.sleep(1)
        # increment the position by 1
        position = position + 1

    # move motor to original position +1 for the next experiment
    # need to write a function to calculate the number of steps needed to return
    # to the original position
    move_motor_ccw(raspi_hostname, raspi_user, raspi_key, raspi_pwd, steps_rev)

if __name__ == "__main__":
    main()