import RPi.GPIO as GPIO
import time 
import sys

out1 = 13
out2 = 11
out3 = 15
out4 = 12

global i
global positive
global negative
global y



GPIO.setmode(GPIO.BOARD)
GPIO.setup(out1,GPIO.OUT)
GPIO.setup(out2,GPIO.OUT)
GPIO.setup(out3,GPIO.OUT)
GPIO.setup(out4,GPIO.OUT)

# print("First calibrate by giving some +ve and -ve values.....")

def move_motor(steps):
    i=0
    y=0
    positive=0
    negative=0
    start = steps
    try:
        while(start > 0):
            print(start)
            GPIO.output(out1,GPIO.LOW)
            GPIO.output(out2,GPIO.LOW)
            GPIO.output(out3,GPIO.LOW)
            GPIO.output(out4,GPIO.LOW)
            x = steps
            if x>0 and x<=3396:
                for y in range(x,0,-1):
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
                        #time.sleep(1)
                    if i==7:
                        i=0
                        continue
                    i=i+1
                start = start - 1
        
        
            elif x<0 and x>=-3396:
                x= steps * -1
                for y in range(x,0,-1):
                    if positive==1:
                        if i==0:
                            i=7
                        else:
                            i=i-1
                        y=y+3
                        positive=0
                    negative=1
                    #print((x+1)-y) 
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
                        #time.sleep(1)
                    if i==0:
                        i=7
                        continue
                    i=i-1 
        GPIO.cleanup()

                
    except KeyboardInterrupt:
        GPIO.cleanup()

def main():
    steps = int(sys.argv[1])
    move_motor(steps)

if __name__ == "__main__":
    main()