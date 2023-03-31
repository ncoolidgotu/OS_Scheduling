#import the necessary modules
import  tkinter as     tk
from    tkinter import filedialog
from time import sleep

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
        self.switch_time = arrival_time

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
class RR:
    #we need a self initialization function to get the data the user specified
    def __init__(self, quantum, context_switching_amount,list_of_processes):
        self.quantum = quantum
        self.context_switching_amount = context_switching_amount
        self.list_of_processes = list_of_processes
        self.state = "i" 
        #"i" = idle, "c" = context switching, "r" = running
        self.current_process = Process(999,999,999,999)
        self.completed = []
        self.graph_data = []

    def scheduling(self):
        #ready queue for process
        ready_queue = []
        #these 2 values let us keep track of times, and when they finish
        timer = 0
        tempo = 1
        #Sort the initial list of processes
        self.list_of_processes.sort(key=lambda x: (x.arrival_time, x.switch_time, -x.priority, x.pid))

        print("INITIAL DATA")
        for i in self.list_of_processes:
            print(i.pid,i.arrival_time,i.burst_time,i.priority,i.remaining_time,i.crt,i.contextS,i.completed_time,i.switch_time)

        while True:
            print("hi, the timer is:",timer)
            #We run through our list of processes and if the arrival time is the same as our timer
            #then we add it to the ready queue (it has arrived)
            for arrival in self.list_of_processes[:]:
                if arrival.arrival_time == timer:
                    ready_queue.append(arrival)
                    if arrival in self.list_of_processes:
                        self.list_of_processes.remove(arrival)

            ready_queue.sort(key=lambda x: (x.switch_time, -x.priority, x.pid))

            #If the processor is idle
            if self.state == "i":

                #First try to see if something is in the ready queue
                if len(ready_queue)>0:
                    #If there is, because it's sorted, and the process is doing nothing, we start running
                    self.state = "r"
                    #the process with the shortest remaining time
                    self.current_process = ready_queue[0]
                    #it runs for for 1s, so the remaining time is decreased by 1s
                    self.current_process.remaining_time -=tempo
                    #because it ran for 1s, the "current running time" increases by 1
                    #this will be used in conjunction with the Quantum time later on
                    self.current_process.crt +=tempo
                    self.graph_data.append((self.current_process.pid,timer))
                    timer +=1
                    if self.current_process.remaining_time == 0:
                        self.state = "i"
                        self.current_process.completed_time = timer
                        ready_queue.remove(self.current_process)
                        self.completed.append(self.current_process)
                        print(ready_queue)
                        print(self.current_process)

                    elif self.quantum == 1 and self.context_switching_amount == 0:
                        self.state = "i"

                    else:
                        if self.current_process.crt == quantum:
                            self.current_process.switch_time = timer
                            self.current_process.crt = 0
                            for arrival in self.list_of_processes:
                                #check the object's "arrival time" attribute
                                if arrival.arrival_time == timer:
                                    #if it's time to enter the ready queue, it does
                                    ready_queue.append(arrival)
                                    #and then gets removed from the list_of_processes (we need to clear it all to end the cycle)
                                    self.list_of_processes.remove(arrival)
                            ready_queue.sort(key=lambda x: (x.switch_time, -x.priority, x.pid))

                            if self.current_process == ready_queue[0]:
                                self.state = "i"
                            
                            else:
                                self.state = "c"

                #If not 2 cases happen
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

            #if the cpu is busy saving a context, we are in the "context saving" state (aka. "c")
            #we would only ever enter here if the context switching time is > 1:
            elif self.state == "c":
                #increase the processes' contextS state
                self.current_process.contextS += tempo
                #increase the timer
                timer += tempo
                #if we're done context switching
                if self.current_process.contextS == self.context_switching_amount:
                    #reset the contextS time, for the next time it may need to context switch
                    self.current_process.contextS = 0
                    self.current_process.switch_time = timer
                    #make the state of the cpu idle, so that it can properly run the latest process
                    self.state = "i"

            #if the cpu is busy running, we are in the "running" state (aka "c")
            #we would only ever enter here if the quantum > 1. 
            elif self.state == "r":
                self.current_process.remaining_time -= tempo
                self.current_process.crt += 1
                self.graph_data.append((self.current_process.pid,timer))
                timer +=1
                print(self.current_process.remaining_time)
                if self.current_process.remaining_time == 0:
                    self.state = "i"
                    self.current_process.completed_time = timer
                    ready_queue.remove(self.current_process)
                    self.completed.append(self.current_process)
                else:
                    print(self.current_process.crt)
                    if self.current_process.crt == self.quantum:
                        self.current_process.crt = 0
                        self.current_process.switch_time = timer
                        for arrival in self.list_of_processes:
                            #check the object's "arrival time" attribute
                            if arrival.arrival_time == timer:
                                #if it's time to enter the ready queue, it does
                                ready_queue.append(arrival)
                                #and then gets removed from the list_of_processes (we need to clear it all to end the cycle)
                                self.list_of_processes.remove(arrival)
                        ready_queue.sort(key=lambda x: (x.switch_time, -x.priority, x.pid))

                        if self.current_process == ready_queue[0]:
                            self.state = "i"
                        else:
                            if self.context_switching_amount == 0:
                                self.state = "i"
                            else:
                                self.state = "c"
            
            print("hi im looping")
            sleep(0.1)
            print("\n")
            if self.state == "c":
                self.graph_data.append(("c",timer))


if __name__ == '__main__':

    '''
    
    FOR TESTING PURPOSES ONLY
    
    '''
    quantum = 1
    context_quantum = 0
    '''
    
    FOR TESTING PURPOSES ONLY
    
    '''
    #initialize an object of the process reader class
    reader = ProcessReader()
    #get the list of "process objects" from the chosen "file reader" object
    processes = reader.selectFile()

    #initialize an object of the process reader class
    reader = ProcessReader()
    #get the list of "process objects" from the chosen "file reader" object
    processes = reader.selectFile()

    rr = RR(quantum,context_quantum,processes)
    rr.scheduling()
    for i in rr.completed:
        print ("The process",i.pid,"finished at time",i.completed_time)
    print(rr.graph_data)