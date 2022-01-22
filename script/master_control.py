import time 
import sys
import csv 
from paramiko import SSHClient      # import the ssh client package
host = "rcvr.local"                 # hostname of the raspberry pi
user = "ted"                        # username of the rpi
client = SSHClient()                # load the sshclient object

client.load_system_host_keys()  

out1 = 13
out2 = 11
out3 = 15
out4 = 12

global i
global positive
global negative
global y

def move_motor(steps):
    client.connect(host, username=user, key_filename="C:/Users/nowak/.ssh/TeddysPC")        # connect to the raspi with the host, user, and ssh private key
    stdin, stdout, stderr = client.exec_command('python3 /home/ted/Documents/motor_control.py %d' %(steps))      # execute the desired file on the rpi

    # check for errors
    if stderr.read() == b'':   
        for line in stdout.readlines():   
            print(line.strip()) # strip the trailing line breaks   
    else:   
        print(stderr.read())  

def vna_data(pos, experiment):
    import socket
    vna = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    vna.connect(("127.0.0.1", 5001))

    # Set the trace parameters
    vna.send(str.encode(":CALC1:PAR3:FORM REIM\n"))
    vna.send(str.encode(":CALC1:PAR3:MARK1:X 4E9\n"))


    with open('creative_file_name.csv', 'a', newline='') as f:
        data_in = csv.writer(f, delimiter='\t')     # we need to initialize the object that writes data

        #data_in.writerow(['Position', 'Experiment', 'Real & Imag Field']) # this will write to a new column in the file

        # for loop to iterate over all position of rx
        # motor control code
        
        
    
        # request the data from the vna
        
        vna.send(str.encode(":CALC1:PAR3:MARK1:Y?\n"))
        string = vna.recv(2056)
        string = string.decode("utf-8")
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
        data = []
        
        # convert scientific notation to decimal
        # round to 6 decimal places
        data.append(round(num2[0] * pow(10, num2[1]),6))
        data.append(round(num2[2] * pow(10, num2[3]),6))   
        
        # now we append this data to the csv file
        # specify the delimiter 
        
        data_in.writerow([pos, experiment, data])
        time.sleep(1)

def main():
    experiment = input("Select the Experiment Number here: (0-18)")
    num_positions = int(sys.argv[2])
    steps = int(sys.argv[1])
    pos = 0
    for i in range(0, num_positions, 1):
        vna_data(pos, experiment)
        move_motor(steps)
        pos = pos + 1

if __name__ == "__main__":
    main()