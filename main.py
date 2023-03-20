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
import tkinter as tk
from tkinter import filedialog

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time

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
            stats = sjf.processData(processQueue.processes)
            print(stats)
    
    def updateGraph(self):
        try:
            self.graphWindow.removeItem(self.graphWindow.itemAt(0))
        except TypeError:
            self.graphWindow.addWidget(Graph(self))
        self.graphWindow.addWidget(Graph(self))
        self.select_Algo()
    
    def input_File(self):
        processQueue.generateQueue()
        

class GUI: #Class to control GUI windows
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv) #Widgets is used to organize GUI windows
        self.screen =  QtWidgets.QStackedWidget() #Stacked widgets allows multiple windows to be created
        self.mainMenu = MainWindow() #Set first window to Main Menu UI
        
    def buildGUI(self): #Build the GUI
            self.screen.addWidget(self.mainMenu) #Screen Index 0
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
        left_coordinates=[1,2,3,4,5]
        heights=[10,20,30,15,40]
        bar_labels=['One','Two','Three','Four','Five']
        plt.bar(left_coordinates,heights,tick_label=bar_labels,width=1)
        plt.xlabel('Time')
        plt.ylabel('Process ID')
        plt.title("Graph Name Goes Here")
        
class ProcessReader:
    def __init__(self):
        self.filename = None
        
    def select_file(self):
        root = tk.Tk()
        root.withdraw()
        self.filename = filedialog.askopenfilename()

    def selectFile(self):
        self.select_file()
        NumbProcesses = []
        with open(self.filename, 'r') as f:
            next(f)
            for line in f:
                process_info = line.strip().split()
                pid = int(process_info[0])
                arrival_time = int(process_info[1])
                burst_time = int(process_info[2])
                NumbProcesses.append(Process(pid, arrival_time, burst_time))
        return NumbProcesses
    
    def generateQueue(self):
        self.processes = self.selectFile()
        print(self.processes)

        
if __name__ == "__main__":
    pygame.mixer.init()     # loads the background music
    pygame.mixer.music.load("bgm.mp3")
    pygame.mixer.music.play()
    processQueue = ProcessReader()
    processQueue.generateQueue()
    gui = GUI()
    gui.buildGUI()

