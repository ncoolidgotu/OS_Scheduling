import tkinter as tk
from tkinter import filedialog
class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time

class ProcessReader:
    def __init__(self):
        self.filename = None
        
    def select_file(self):
        root = tk.Tk()
        root.withdraw()
        self.filename = filedialog.askopenfilename()

    def selectFile(self):
        if not self.filename:
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


reader = ProcessReader()
processes = reader.selectFile()


class SJF:

    def processData(self):
        process_data = []
        #Gets the values for each process
        for process in processes:

            temporary = []
            temporary.extend([process.pid, process.arrival_time, process.burst_time, 0])
            process_data.append(temporary)


        SJF.schedulingProcess(self, process_data)
    def schedulingProcess(self, process_data):
        start_time = []
        exit_time = []
        s_time = 0
        process_data.sort(key=lambda x: x[1])
        #Sort processes according to the Arrival Time
        for i in range(len(process_data)):
            ready_queue = []
            temp = []
            normal_queue = []

            for j in range(len(process_data)):
                #Adds processes that havent been completed but have arrived to the ready queue
                if (process_data[j][1] <= s_time) and (process_data[j][3] == 0):
                    temp.extend([process_data[j][0], process_data[j][1], process_data[j][2]])
                    ready_queue.append(temp)
                    temp = []
                #Creates a normal queue with the processes that havent been completed and havent arrived
                elif process_data[j][3] == 0:
                    temp.extend([process_data[j][0], process_data[j][1], process_data[j][2]])
                    normal_queue.append(temp)
                    temp = []
                    
            #Runs the process with the shortest burst time from the ones that have arrived (ready queue)
            if len(ready_queue) != 0:
                ready_queue.sort(key=lambda x: x[2])
                #Sort the processes according to the Burst Time
                start_time.append(s_time)
                s_time = s_time + ready_queue[0][2]
                e_time = s_time
                exit_time.append(e_time)
                for k in range(len(process_data)):
                    if process_data[k][0] == ready_queue[0][0]:
                        break
                process_data[k][3] = 1
                process_data[k].append(e_time)

            elif len(ready_queue) == 0:
                if s_time < normal_queue[0][1]:
                    s_time = normal_queue[0][1]
                start_time.append(s_time)
                s_time = s_time + normal_queue[0][2]
                e_time = s_time
                exit_time.append(e_time)
                for k in range(len(process_data)):
                    if process_data[k][0] == normal_queue[0][0]:
                        break
                process_data[k][3] = 1
                process_data[k].append(e_time)

        t_time = SJF.calculateTurnaroundTime(self, process_data)
        w_time = SJF.calculateWaitingTime(self, process_data)
        SJF.printData(self, process_data, t_time, w_time)


    def calculateTurnaroundTime(self, process_data):
        total_turnaround_time = 0
        for i in range(len(process_data)):
            #turnaround_time = completion_time - arrival_time
            turnaround_time = process_data[i][4] - process_data[i][1]
            total_turnaround_time = total_turnaround_time + turnaround_time
            process_data[i].append(turnaround_time)
        #average_turnaround_time = total_turnaround_time / no_of_processes    
        average_turnaround_time = total_turnaround_time / len(process_data)
        return average_turnaround_time
    
    def calculateWaitingTime(self, process_data):
        total_waiting_time = 0
        for i in range(len(process_data)):
            #waiting_time = turnaround_time - burst_time
            waiting_time = process_data[i][5] - process_data[i][2]
            total_waiting_time = total_waiting_time + waiting_time
            process_data[i].append(waiting_time)
        #average_waiting_time = total_waiting_time / no_of_processes    
        average_waiting_time = total_waiting_time / len(process_data)
        return average_waiting_time


    def printData(self, process_data, average_turnaround_time, average_waiting_time):
        process_data.sort(key=lambda x: x[0])
        #Sort processes according to the Process ID
        print("Process_ID  Arrival_Time  Burst_Time      Completed  Completion_Time  Turnaround_Time     Waiting_Time")

        for i in range(len(process_data)):
            for j in range(len(process_data[i])):

                print(process_data[i][j], end="	       ")
            print()

        print(f'Average Turnaround Time: {average_turnaround_time}')

        print(f'Average Waiting Time: {average_waiting_time}')

if __name__ == "__main__":
    sjf = SJF()
    sjf.processData()


print()