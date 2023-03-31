import tkinter as tk
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

class FCFS:
    def __init__(self, processes):
        self.processes = processes

    def processData(self):
        process_data = []
        # Gets the values for each process
        for process in self.processes:
            temporary = []
            temporary.extend([process.pid, process.arrival_time, process.burst_time, process.priority])
            process_data.append(temporary)
        return FCFS.schedulingProcess(self, process_data)

    def schedulingProcess(self, process_data):
        exit_time = []
        process_data.sort(key=lambda x: (x[1],-x[3],x[0]))
        
        
        for x in range(len(process_data)):
            #appends the first process to the exit list
            if(x==0):
                exit_time.append(process_data[x][2]+process_data[x][1])
            #for all other elements
            else:#if the arrival is greater than the last exit time
                if (process_data[x][1]> exit_time[x-1]):
                    exit_time.append(process_data[x][1]+process_data[x][2]) #append the arrival time
                    #process_data.append(process_data[x][1]+process_data[x][2])
                else: #if the arrival time is the same as the exit time of the last process, just append the next completion time (completion time of last + burst time of this process)
                    exit_time.append(exit_time[x-1]+process_data[x][2])
                    #process_data.append(exit_time[x-1]+process_data[x][2])
        pHold = 0
        for y in exit_time:
            process_data[pHold].append(exit_time[pHold])
            pHold +=1

        print(exit_time)
        print(process_data)

        t_time = FCFS.calculateTurnaroundTime(self, process_data)
        w_time = FCFS.calculateWaitingTime(self, process_data)
        return FCFS.printData(self, process_data, t_time, w_time)

    def calculateTurnaroundTime(self, process_data):
        total_turnaround_time = 0
        for i in range(len(process_data)):
            # turnaround_time = completion_time - arrival_time
            turnaround_time = process_data[i][4] - process_data[i][1]
            if turnaround_time < 0: #if turnaround is negative, just set to 0 because time cant be negative
                turnaround_time = 0
            else:
                turnaround_time = process_data[i][4] - process_data[i][1]

            total_turnaround_time = total_turnaround_time + turnaround_time
            if total_turnaround_time < 0:#if total turnaround is negative, just set to 0 because time cant be negative
                total_turnaround_time = 0
            else:
                total_turnaround_time = total_turnaround_time + turnaround_time
            process_data[i].append(turnaround_time)
        # average_turnaround_time = total_turnaround_time / no_of_processes
        average_turnaround_time = total_turnaround_time / len(process_data)
        return average_turnaround_time

    def calculateWaitingTime(self, process_data):
        total_waiting_time = 0
        for i in range(len(process_data)):
            # waiting_time = turnaround_time - burst_time
            waiting_time = process_data[i][5] - process_data[i][2]
            if waiting_time < 0: #if waiting time is negative, just set to 0, time cant be negative
                waiting_time = 0
            else:
                waiting_time = process_data[i][5] - process_data[i][2]
            
            total_waiting_time = total_waiting_time + waiting_time
            if total_waiting_time < 0: #if total wait time is negative, just set to 0, time cant be negative
                total_waiting_time = 0
            else:
                total_waiting_time = total_waiting_time + waiting_time
            process_data[i].append(waiting_time)
        # average_waiting_time = total_waiting_time / no_of_processes
        average_waiting_time = total_waiting_time / len(process_data)
        return average_waiting_time

    def printData(self, process_data, average_turnaround_time, average_waiting_time):
        process_data.sort(key=lambda x: x[0])
        # Sort processes according to the Process ID
        print("Process_ID  Arrival_Time  Burst_Time      Priority  Completion_Time  Turnaround_Time     Waiting_Time")

        for i in range(len(process_data)):
            for j in range(len(process_data[i])):
                print(process_data[i][j], end="	       ")
            print()

        print(f'Average Turnaround Time: {average_turnaround_time}')

        print(f'Average Waiting Time: {average_waiting_time}')

        NewArray = []
        for i in range(len(process_data)):
            NewArray.append([process_data[i][4], process_data[i][0]])
            NewArray.sort()
        return NewArray


if __name__ == '__main__':
    '''
    
    FOR TESTING PURPOSES ONLY
    
    '''
    quantum = 2
    context_quantum = 1
    '''
    
    FOR TESTING PURPOSES ONLY
    
    '''
    #initialize an object of the process reader class
    reader = ProcessReader()
    #get the list of "process objects" from the chosen "file reader" object
    processes = reader.selectFile()

    fcfs = FCFS(processes)
    fcfs.processData()

