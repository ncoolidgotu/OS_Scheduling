import tkinter as tk
from tkinter import filedialog

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
    
    def execute(self, time_quantum):
        # execute the process for the given time quantum
        if self.remaining_time > time_quantum:
            self.remaining_time -= time_quantum
            return time_quantum
        else:
            temp = self.remaining_time
            self.remaining_time = 0
            return temp

class Robin:
    def __init__(self, quantum):
        self.quantum = quantum

    def schedulingProcess(self, processes):
        start_time = []
        exit_time = []
        remaining_time = [p.burst_time for p in processes]
        time = 0
        i = 0
        while True:
            flag = True
            for j in range(len(processes)):
                if remaining_time[j] > 0:
                    flag = False
                    if remaining_time[j] > self.quantum:
                        start_time.append(time)
                        time += self.quantum
                        exit_time.append(time)
                        remaining_time[j] -= self.quantum
                    else:
                        start_time.append(time)
                        time += remaining_time[j]
                        exit_time.append(time)
                        remaining_time[j] = 0
            if flag == True:
                break
            i += 1
            if i == len(processes):
                i = 0

        return self.printData(processes, start_time, exit_time)

    def printData(self, processes, start_time, exit_time):
        total_waiting_time = 0
        total_turnaround_time = 0
        print("Process_ID  Arrival_Time  Burst_Time      Completed  Completion_Time  Turnaround_Time     Waiting_Time")
        for i in range(len(processes)):
            turnaround_time = exit_time[i] - processes[i].arrival_time
            total_turnaround_time += turnaround_time
            waiting_time = turnaround_time - processes[i].burst_time
            total_waiting_time += waiting_time
            print(f"{processes[i].pid}             {processes[i].arrival_time}             {processes[i].burst_time}                Yes           {exit_time[i]}                {turnaround_time}                {waiting_time}")
        print(f"Average Turnaround Time: {total_turnaround_time/len(processes)}")
        print(f"Average Waiting Time: {total_waiting_time/len(processes)}")
        
        NewArray = []
        for i in range(len(processes)):
            NewArray.append([exit_time[i], processes[i].pid])
            NewArray.sort()
        return NewArray
