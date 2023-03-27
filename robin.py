import tkinter as tk
from tkinter import filedialog

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = self.burst_time


class Robin:
    
    def __init__(self, quantum, context_switching):
        self.quantum = quantum
        self.context_switching = context_switching
        self.cpu_queue = []
        self.timer = 0
        
    def execute(self, process):
        if process.remaining_time <= self.quantum:
            time = process.remaining_time
            process.remaining_time = 0
        else:
            time = self.quantum
            process.remaining_time -= self.quantum
        return time

    def schedulingProcess(self, processes):
        ready_queue = processes.copy()
        start_time = []
        exit_time = []
        i = 0
        while True:
            flag = True
            for j in range(len(ready_queue)):
                if ready_queue[j].arrival_time <= self.timer:
                    self.cpu_queue.append(ready_queue[j])
                    ready_queue.pop(j)
                    flag = False
                    break
            if flag and not self.cpu_queue:
                self.timer += 1
                continue

            self.cpu_queue.sort(key=lambda x: x.pid)
            current_process = self.cpu_queue.pop(0)
            if current_process.remaining_time > self.quantum:
                start_time.append(self.timer)
                print(dir(processes[0]))
                time = self.execute(current_process)
                self.timer += time
                self.cpu_queue.append(current_process)
                self.timer += self.context_switching
            else:
                start_time.append(self.timer)
                time = self.execute(current_process)
                self.timer += time
                exit_time.append(self.timer)
                i += 1
            
            for j in range(len(ready_queue)):
                if ready_queue[j].arrival_time <= self.timer:
                    for k in range(len(self.cpu_queue)):
                        if (ready_queue[j].arrival_time < self.cpu_queue[k].arrival_time) or (ready_queue[j].arrival_time == self.cpu_queue[k].arrival_time and ready_queue[j].priority < self.cpu_queue[k].priority):
                            self.cpu_queue.insert(k, ready_queue.pop(j))
                            break
                    break

            if i == len(processes) and not self.cpu_queue:
                break

        return self.print_data(processes, start_time, exit_time)

    def print_data(self, processes, start_time, exit_time):
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
        
        new_array = [[exit_time[i], processes[i].pid] for i in range(len(processes))]
        new_array.sort()
        return new_array

