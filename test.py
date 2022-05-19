import serial
import time
import sys
import trace
import threading
from serial import SerialException
from PyQt5.QtWidgets import QPushButton, QMessageBox

# port_name = 'COM4'
#mac port
port_name = '/dev/cu.usbmodem14201'


class  MainTest(threading.Thread):
    """A subclass of threading.Thread, with a kill() method"""
    def __init__(self, data):
        threading.Thread.__init__(self)
        self.state = threading.Condition()
        
        #local variables
        self.info = data
        
        self.killed= False
        
        #test flags to pass to main.py finished (ran through)
        self.finished = False
        
        #Set up serial connection
        self.connect()
        
        
        
        
        
    def connect(self):
        try: 
            self.ser = serial.Serial(port_name, 9600, timeout=1)
        except SerialException:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('ERROR CONNECTING')
            msgBox.setText("Issue connecting. Test aborted")
            msgBox.addButton(QPushButton('Ok'), QMessageBox.YesRole)
            ret = msgBox.exec_()
            self.killed = True
            
            
            
    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run     
        threading.Thread.start(self)
        
        
        
    def __run(self):
        # self.resume()
        #RUN TESTS
        """Hacked run function, which installs the
        trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup
        
        #TODO --> abort test immediately if click stop
        while True: 
            #If user stops - or test has completed (stop)
            if self.finished:
                break
            #TEST HERE
            self.ser.write(str.encode('<TEST>'))
            time.sleep(1)
            x = self.ser.readline().decode('UTF-8', 'strict')
            print("DATA", x)
            time.sleep(.5)
            
            #test
            self.test1 = "katie"
                
                
            self.ser.write(str.encode('<PROGRAM_NORDIC>'))
            time.sleep(1)    
            
            # if ser.inWaiting()>0:
            x = self.ser.readline().decode('UTF-8', 'strict')
            print("DATA2", x)
            time.sleep(.5)
            self.test2 = "hi"
            
            
            #finished sucessfully
            self.finished = True
            
            print("done")
        
    
    
    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None
        
    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
            return self.localtrace
            
           
    #this will exit thread immediately 
    def kill(self):
        self.killed = True
        
