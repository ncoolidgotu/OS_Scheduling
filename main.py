import sys
from PyQt6 import QtWidgets #For Changing GUI Screens
from PyQt6.QtCore import QDate, QDateTime
from PyQt6.QtWidgets import QApplication, QMainWindow, QErrorMessage, QMessageBox #For GUI Functionality
from PyQt6.uic import loadUi #For UI importing
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pygame   #For background music

class MainWindow(QMainWindow): #Derived class of QMainWindow to control functionality inside the windows
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("MainWindow.ui",self)  # Loads the window from main menu .ui file
        #self.inputFile.clicked.connect(ProcessReader.selectFile)  
        self.showGraph.clicked.connect(Graph.show)              
        
class Graph(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(5, 4), dpi=200)
        super().__init__(fig)
        self.setParent(parent)

        """ 
        Matplotlib Script
        """
        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)
        
        self.ax.plot(t, s)

        self.ax.set(xlabel='time (s)', ylabel='voltage (mV)',
            title='About as simple as it gets, folks')
        self.ax.grid()
