import sys
import numpy as np
from PyQt6 import QtWidgets #For Changing GUI Screens
from PyQt6.QtCore import QDate, QDateTime
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout #For GUI Functionality
from PyQt6.uic import loadUi #For UI importing
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pygame   #For background music

class MainWindow(QMainWindow): #Derived class of QMainWindow to control functionality inside the windows
    def __init__(self):
        # Create a QMdiArea widget
        super(MainWindow,self).__init__()
        loadUi("MainWindow.ui",self)  # Loads the window from main menu .ui file
        #self.inputFile.clicked.connect(ProcessReader.selectFile)  
        self.showGraph.clicked.connect(Graph.show)
        subWindow = SubWindow()
        self.mdiArea.addSubWindow(subWindow)
        

class SubWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Add some content to the subwindow
        chart = Graph(self)
        layout = QVBoxLayout(self)
        layout.addWidget(chart)
        
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
        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)
        
        self.ax.plot(t, s)

        self.ax.set(xlabel='time (s)', ylabel='voltage (mV)',
            title='About as simple as it gets, folks')
        self.ax.grid()
        
if __name__ == "__main__":
    pygame.mixer.init()     # loads the background music
    pygame.mixer.music.load("bgm.mp3")
    pygame.mixer.music.play()
    gui = GUI()
    gui.buildGUI()

