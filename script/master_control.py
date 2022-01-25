import time 
import sys
import csv 
import socket
import os.path
from paramiko import SSHClient      # import the ssh client package

# this script will take several input arguments
# 1. location of file to store the data
# 2. # of steps to turn the motor
# 3. experiment number
# 4. # of antenna locations

def move_motor_ccw(steps):
    host = "rcvr.local"                 # hostname of the raspberry pi
    user = "ted"                        # username of the rpi
    
    client = SSHClient()                # load the sshclient object
    client.load_system_host_keys()      # load system host keys (may not be necessary when specifying the keyfile)
    client.connect(host, username=user, key_filename="C:/Users/nowak/.ssh/TeddysPC")                        # connect to the raspi with the host, user, and ssh private key
    stdin, stdout, stderr = client.exec_command('/home/ted/venv/bin/python3 /home/ted/Documents/motor/motor_ccw.py %d' %(steps))      # execute the desired file on the rpi

    # check for errors
    if stderr.read() == b'':   
        for line in stdout.readlines():   
            print(line.strip()) # strip the trailing line breaks   
    else:   
        print(stderr.read())

def move_motor_cw(steps):
    host = "rcvr.local"                 # hostname of the raspberry pi
    user = "ted"                        # username of the rpi
    
    client = SSHClient()                # load the sshclient object
    client.load_system_host_keys()      # load system host keys (may not be necessary when specifying the keyfile)
    client.connect(host, username=user, key_filename="C:/Users/nowak/.ssh/TeddysPC")                        # connect to the raspi with the host, user, and ssh private key
    stdin, stdout, stderr = client.exec_command('/home/ted/venv/bin/python3 /home/ted/Documents/motor/motor_cw.py %d' %(steps))      # execute the desired file on the rpi

    # check for errors
    if stderr.read() == b'':   
        for line in stdout.readlines():   
            print(line.strip()) # strip the trailing line breaks   
    else:   
        print(stderr.read())  

def init_vna():
    # Initialize the connection with the shockline software
    # The shockline interface will be greyed out if this is successful
    global vna
    vna = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    vna.connect(("127.0.0.1", 5001))

    # Set the desired trace parameters
    vna.send(str.encode(":CALC1:PAR3:FORM REIM\n"))
    vna.send(str.encode(":CALC1:PAR3:MARK1:X 4E9\n"))

def does_file_exist():
    if os.path.isfile(data_file) == True:
        print('The specified file already exists. Continuing...')
    else:
        print('The file does not exist. Creating a new file...')
        with open(data_file, 'w', newline='') as newFile:
            # after creating the file, we want to initialize the variables that will be stored
            header = csv.writer(newFile, delimiter='\t')
            header.writerow(['Position', 'Experiment', 'Real & Imag Field'])

def get_vna_data():
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

def write_data(position, experiment, data):
    # now we can write the data to the created csv file
    with open(data_file, 'a', newline='') as f:
        data_in = csv.writer(f, delimiter='\t')     # we need to initialize the object that writes data
       
        # now we append this data to the csv file
        data_in.writerow([position, experiment, data])
        time.sleep(1)

def main():
    global data_file
    global steps
    global exp_num
    global num_positions
    # input arguments:
    data_file = sys.argv[1]
    steps = int(sys.argv[2])
    exp_num = int(sys.argv[3])
    num_positions = int(sys.argv[4])

    # first check if the data file exists
    does_file_exist()

    # initialize the vna
    init_vna()

    # we'll loop over the number of positions (# of receive antenna locations)
    # collect data, process, save to file, move motor, repeat
    position = 0
    for i in range(0, num_positions, 1):
        # get the data from vna
        data = get_vna_data()
        # process the data
        final_data = process_data(data)
        # write the data to file
        write_data(position, exp_num, final_data)
        # move the motor to the next position
        move_motor_cw(steps)
        # wait for the system to settle
        time.sleep(1)
        # increment the position by 1
        position = position + 1

    # move motor to original position +1 for the next experiment
    # need to write a function to calculate the number of steps needed to return
    # to the original position
    move_motor_ccw(steps)
if __name__ == "__main__":
    main()