import RPi.GPIO as GPIO
import time 
import sys

out1 = 13
out2 = 11
out3 = 15
out4 = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(out1,GPIO.OUT)
GPIO.setup(out2,GPIO.OUT)
GPIO.setup(out3,GPIO.OUT)
GPIO.setup(out4,GPIO.OUT)

def move_motor_cw(steps):
    i=0
    start = steps

    try:
        while(1):
            # print(start)
            GPIO.output(out1,GPIO.LOW)
            GPIO.output(out2,GPIO.LOW)
            GPIO.output(out3,GPIO.LOW)
            GPIO.output(out4,GPIO.LOW)

            for y in range(start,0,-1):
                if i==0:
                    GPIO.output(out1,GPIO.HIGH)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(0.001)
                    #time.sleep(1)
                elif i==1:
                    GPIO.output(out1,GPIO.HIGH)
                    GPIO.output(out2,GPIO.HIGH)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(0.001)
                    #time.sleep(1)
                elif i==2:  
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.HIGH)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(0.001)
                    #time.sleep(1)
                elif i==3:    
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.HIGH)
                    GPIO.output(out3,GPIO.HIGH)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(0.001)
                    #time.sleep(1)
                elif i==4:  
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.HIGH)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(0.001)
                    #time.sleep(1)
                elif i==5:
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.HIGH)
                    GPIO.output(out4,GPIO.HIGH)
                    time.sleep(0.001)
                    #time.sleep(1)
                elif i==6:    
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.HIGH)
                    time.sleep(0.001)
                    #time.sleep(1)
                elif i==7:    
                    GPIO.output(out1,GPIO.HIGH)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.HIGH)
                    time.sleep(0.001)
                    i = 0
                    #time.sleep(1)
                i=i+1
            print('Motor moved the desired number of steps.')
            break       # once the for loop is completed break from the infinite while loop
        GPIO.cleanup()
        print('Motor in position.')
       
    except KeyboardInterrupt:
        GPIO.cleanup()

def main():
    steps = int(sys.argv[1])
    move_motor_cw(steps)

if __name__ == "__main__":
    main()