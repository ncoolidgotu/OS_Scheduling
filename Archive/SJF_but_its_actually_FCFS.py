#import the necessary modules
import  tkinter as     tk
from    tkinter import filedialog
from time import sleep
from copy import deepcopy

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        #process id
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.crt = 0
        self.contextS = 0
        self.completed_time = 0

#class used to read and open the files
class ProcessReader:
    #Initiate and stablish a default filename of 'none'
    def __init__(self):
        self.filename = None
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

#We create a class for Shortest Remaining Time First
class SRTF:
    #we need a self initialization function to get the data the user specified
    def __init__(self):
        #"i" = idle, "c" = context switching, "r" = running
        self.state = "i"
        self.current_process = Process(999,999,999,999)
        self.completed = []
        self.graph_data = []

    def scheduling(self,list_of_processes):
        self.list_of_processes = deepcopy(list_of_processes)
        #ready queue for process
        ready_queue = []
        #these 2 values let us keep track of times, and when they finish
        timer = 0
        tempo = 1
        #Sort the initial list of processes
        self.list_of_processes.sort(key=lambda x: (x.arrival_time, -x.priority, x.pid))

        while True:
            print("hi, the timer is:",timer)
            #We run through our list of processes and if the arrival time is the same as our timer
            #then we add it to the ready queue (it has arrived)
            for arrival in self.list_of_processes[:]:
                if arrival.arrival_time == timer:
                    ready_queue.append(arrival)
                    if arrival in self.list_of_processes:
                        self.list_of_processes.remove(arrival)

            ready_queue.sort(key=lambda x: (x.arrival_time, -x.priority, x.pid))

            if self.state == "i":
                if len(ready_queue)>0:
                    self.state = "r"
                    self.current_process = ready_queue[0]
                    self.current_process.remaining_time -= tempo
                    self.graph_data.append((self.current_process.pid,timer))
                    timer+=1

                else:
                    #If we're just waiting on more processes, then we'll wait
                    if len(self.list_of_processes)>0:
                        self.graph_data.append(("i",timer))
                        timer +=1
                    #If there's nothing in the ready queue and we're waiting on nothing else
                    else:
                        print("Program ended at:",timer)
                        #then we just end
                        break

                    if self.current_process.remaining_time == 0:
                        self.state = "i"
                        self.current_process.completed_time = timer
                        ready_queue.remove(self.current_process)
                        self.completed.append(self.current_process)

            else:
                self.current_process.remaining_time -= tempo
                self.current_process.crt += 1
                self.graph_data.append((self.current_process.pid,timer))
                timer +=1

                if self.current_process.remaining_time == 0:
                    self.state = "i"
                    self.current_process.completed_time = timer
                    ready_queue.remove(self.current_process)
                    self.completed.append(self.current_process)

        print (self.graph_data)
        return self.graph_data
    
if __name__ == '__main__':
    #initialize an object of the process reader class
    reader = ProcessReader()
    #get the list of "process objects" from the chosen "file reader" object
    processes = reader.selectFile()

    srtf = SRTF()
    srtf.scheduling(processes)