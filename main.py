import sys
import numpy as np
from PyQt6 import QtWidgets #For Changing GUI Screens
from PyQt6.QtCore import QDate, QDateTime
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout #For GUI Functionality
from PyQt6.uic import loadUi #For UI importing
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pygame   #For background music
import SJF_Caleb
import RR
import SRTF
import tkinter as tk
from tkinter import filedialog

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.crt = 0
        self.contextS = 0
        self.completed_time = 0
        self.switch_time = arrival_time

class MainWindow(QMainWindow): #Derived class of QMainWindow to control functionality inside the windows
    def __init__(self):
        # Create a QMdiArea widget
        self.mdiArea = QtWidgets.QMdiArea()
        super(MainWindow,self).__init__()
        loadUi("MainWindow.ui",self)  # Loads the window from main menu .ui file
        #self.inputFile.clicked.connect(ProcessReader.selectFile)  
        self.showGraph.clicked.connect(self.updateGraph)
        self.inputFile.clicked.connect(self.input_File)

    def select_Algo(self):
        print(self.selectAlgo.currentText())
        if self.selectAlgo.currentText() == "SJF":
            sjf = SJF_Caleb.SJF()
            print(processQueue.processes)
            self.stats = sjf.processData(processQueue.processes)
            print(self.stats)
        elif self.selectAlgo.currentText() == "RR":
            quantumTime=int(self.quantumTime.text())
            contextSwitchTime=int(self.switchTime.text())
            rr = RR.RR()
            print((quantumTime, contextSwitchTime, processQueue.processes))
            self.stats = rr.scheduling(quantumTime, contextSwitchTime, processQueue.processes)
            print(self.stats)
        elif self.selectAlgo.currentText() == "SRTF":
            quantumTime=int(self.quantumTime.text())
            contextSwitchTime=int(self.switchTime.text())
            srtf = SRTF.SRTF()
            print((quantumTime, contextSwitchTime, processQueue.processes))
            self.stats = srtf.scheduling(quantumTime, contextSwitchTime, processQueue.processes)
            print(self.stats)
    
    def updateGraph(self):
        self.select_Algo()
        try:
            self.graphWindow.removeItem(self.graphWindow.itemAt(0))
        except TypeError:
            self.graphWindow.addWidget(Graph(self))
        self.graphWindow.addWidget(Graph(self))
    
    def input_File(self):
        processQueue.generateQueue()
        

class GUI: #Class to control GUI windows
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv) #Widgets is used to organize GUI windows
        self.screen =  QtWidgets.QStackedWidget() #Stacked widgets allows multiple windows to be created
        self.mainWindow = MainWindow() #Set first window to Main Menu UI
        
    def buildGUI(self): #Build the GUI
            self.screen.addWidget(self.mainWindow) #Screen Index 0
            self.screen.setFixedHeight(720) #constrain window dimensions
            self.screen.setFixedWidth(1280)
            self.screen.show() #Display window
            self.app.exec() #Execute GUI


class Graph(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(4, 3), dpi=200)
        super().__init__(fig)
        self.setParent(parent)

        """ 
        Matplotlib Script
        """
        coord=gui.mainWindow.stats
        time = [0]
        proc_id = [0]
        for i in coord:
            time.append(i[1])
            proc_id.append(i[0])
        left_coordinates = time
        heights=proc_id
        plt.step(left_coordinates,heights)
        plt.xlabel('Time')
        plt.ylabel('Process ID')
        plt.title(gui.mainWindow.selectAlgo.currentText())

        
class ProcessReader:
    #Initiate and stablish a default filename of 'none'
    def __init__(self):
        self.filename = None
        self.processes = self.selectFile()
        
        
    #Prompts the user through tkinter to open a file, in which we get the appropiate file
    def select_file(self):
        root = tk.Tk()
        root.withdraw()
        self.filename = filedialog.askopenfilename()

    #This function opens the file and then creates the process objects based on the information provided
    def selectFile(self):
        #Value necessary for the while loop to make sure the program doesnt break and the user can try again
        self.incorrectFile = True
        while self.incorrectFile:
            try:
                #if this class no attribute "filename" (initialized as such)
                #then prompt it to select it, by using the previous function (named unfortunately similar)
                if not self.filename or self.incorrectFile:
                    self.select_file()
                NumbProcesses = []
                #open the file if possible (inside try)
                with open(self.filename, 'r') as f:
                    next(f)
                    #go through each line in the file, and fill a list with Process OBJECTS
                    for line in f:
                        #We parse the info as specified in the assignment
                        process_info = line.strip().split()
                        pid = int(process_info[0])
                        arrival_time = int(process_info[1])
                        burst_time = int(process_info[2])
                        priority = int(process_info[3])
                        NumbProcesses.append(Process(pid, arrival_time, burst_time,priority))
                #to exit the loop
                self.incorrectFile = False
                #return the list of process objects 
                return NumbProcesses
            #Print an error message if the user chooses an invalid file
            except:
                print("UNEXPECTED ERROR! Please choose the file again or contact the developer :)")
                
    def generateQueue(self):
        self.processes = self.selectFile()
        print(self.processes)

    def createProcess(self, pid, burst_time, priority):
        process = Process(pid, burst_time, priority)
        process.remaining_time = burst_time  # add remaining_time attribute
        return process

        
if __name__ == "__main__":
    #pygame.mixer.init()     # loads the background music
    #pygame.mixer.music.load("bgm.mp3")
    #pygame.mixer.music.play()
    processQueue = ProcessReader()
    gui = GUI()
    gui.buildGUI()

