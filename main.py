
from this import d
from PyQt5 import QtGui, QtCore, uic, QtWidgets
from PyQt5.QtWidgets import (QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)

from PyQt5.QtWidgets import QMainWindow, QPushButton, QMessageBox, QFileDialog
import sys
from mainWindow import Ui_Programming
from tests import MainTest
import time



##DETAIL FOR TEST THREAD 
#In tests.py PCB test --> pass in any values you want to have in the output
#Test thread use variables on the PCBTEST class to update the UI - in the update
#function on this page 

#TODO --> 
##Test order?
##Test bluetooth, once passes, test power - then program and test other components


#UI_Programming custom class inherit
class MyWindow(QtWidgets.QWidget, Ui_Programming):
    main_test = None  # threaded class initiated on test start


    def __init__(self):
        super(MyWindow, self).__init__()
        
        self.setupUi(self)  

        #Set up UI connections
        self.start_btn.clicked.connect(self.start_test)    
        self.stop_btn.clicked.connect(self.stop_test) 
        
        # testing flag
        self.test_in_progress = False
        
        
        
    # Start test from test.py file - separate thread
    def start_test(self):
        print("starting")
        
        data = ""
        #--------------------
        #TEST STARTS HERE 
        #--------------------
        self.main_test = MainTest(data)
        self.test_in_progress = True
        self.aborted_test = False
        self.main_test.start()
        self.update()
        
        
    #Stop test thread
    def stop_test(self):
        print("stop!!!")
        self.main_test.kill()
        self.reset_test_thread()

        
    #Reset test thread
    def reset_test_thread(self):
        #reset test
        self.main_test = None
        self.test_in_progress = False
        
        #clear input values
        
        #Display info to user
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle('Test Alert')
        
        #If reset test thread
        if self.aborted_test:
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Test exited early due to manual stop")
            msgBox.addButton(QPushButton('OK'), QMessageBox.YesRole)
            msgBox.exec_()
        else:
            msgBox.setText("Test Finished")
            msgBox.addButton(QPushButton('OK'), QMessageBox.YesRole)
            msgBox.exec_()
        
        
    #runs every 100ms to update data only if test is running
    def update(self):
        QtCore.QTimer.singleShot(100, self.update) #Refresh ~100ms
        if self.test_in_progress and self.main_test !=None:
            if not self.main_test.isAlive():
                print("not alive")
                self.reset_test_thread()
            else: 
                print("running")
                print("data", self.main_test.test1)
                #update each test            
                #update DATA HERE ON GUI
                
    

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    #init global variables
    w = MyWindow()
    w.show()
    #calls update function every 100 ms
    w.update()
    sys.exit(app.exec_())
        
        
        
        