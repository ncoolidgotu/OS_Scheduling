#import the necessary modules
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

#We create a class for Shortest Job First
class SJF:
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
        self.list_of_processes.sort(key=lambda x: (x.arrival_time, x.remaining_time, -x.priority, x.pid))

        while True:
            #We run through our list of processes and if the arrival time is the same as our timer
            #then we add it to the ready queue (it has arrived)
            for arrival in self.list_of_processes[:]:
                if arrival.arrival_time == timer:
                    ready_queue.append(arrival)
                    if arrival in self.list_of_processes:
                        self.list_of_processes.remove(arrival)

            ready_queue.sort(key=lambda x: (x.remaining_time, -x.priority, x.pid))

            if self.state == "i":
                if len(ready_queue)>0:
                    self.state = "r"
                    self.current_process = ready_queue[0]
                    self.current_process.remaining_time -= tempo
                    self.graph_data.append((self.current_process.pid,timer))
                    timer+=1
                    
                    if self.current_process.remaining_time == 0:
                        self.state = "i"
                        self.current_process.completed_time = timer
                        ready_queue.remove(self.current_process)
                        self.completed.append(self.current_process)

                else:
                    #If we're just waiting on more processes, then we'll wait
                    if len(self.list_of_processes)>0:
                        self.graph_data.append(("i",timer))
                        timer +=1
                    #If there's nothing in the ready queue and we're waiting on nothing else
                    else:
                        #then we just end
                        break

                    

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
    