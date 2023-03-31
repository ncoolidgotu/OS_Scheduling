#import the necessary modules
from copy import deepcopy
#we create a process class here even though it exists in main
#because we need to create a dummy process object for the logic
class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        #process id
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        #remaining time will get modified, burst will not | this was done in case calculations were necessary
        #(now we know, they are really not, whoops)
        self.remaining_time = burst_time
        #self.crt means "current running time" | this checks with quantum, to see if it has
        #to stop running and context switch
        self.crt = 0
        #this keeps track of how long the proces has been saving its context for
        #this is so we can compare with the total amount of context switching to stop and pick a new process
        self.contextS = 0
        #this keeps track of the completed time. When the process' remaining time reaches 0
        #the current time gets appended.
        self.completed_time = 0
#We create a class for Shortest Remaining Time First
class SRTF:
    #we need a self initialization function to get the data the user specified
    def __init__(self):
        #"i" = idle, "c" = context switching, "r" = running
        #because the processor always starts in idle mode at time 0, we give it that state
        self.state = "i"
        #we create a dummy process object needed for comparisons in the logic
        #this will also serve as the indicator of the current process that it's being run
        self.current_process = Process(999,999,999,999)
        #as process complete we're going to put them in this list
        self.completed = []
        #and put the information of their timers in this graph data
        #these are essentially, the results
        self.graph_data = []
    #this function is self explanatory, has all the logic
    def scheduling(self,quantum,context_switching_amount,list_of_processes):
        self.quantum = quantum
        self.context_switching_amount = context_switching_amount
        self.list_of_processes = deepcopy(list_of_processes) 
        #ready queue for process
        ready_queue = []
        #these 2 values let us keep track of times, and when they finish
        timer = 0
        tempo = 1
        #Sort the initial list of processes, by arrival time, with some tiebreakers
        self.list_of_processes.sort(key=lambda x: (x.arrival_time, x.remaining_time, -x.priority, x.pid))

        #The following loop has all of the logic of the scheduling
        #It will run for as long as there are processes that have not

        while True:
            #We run through our list of processes and if the arrival time is the same as our timer
            #then we add it to the ready queue (it has arrived)
            for arrival in self.list_of_processes:
                #check the object's "arrival time" attribute
                if arrival.arrival_time == timer:
                    #if it's time to enter the ready queue, it does
                    ready_queue.append(arrival)
                    #and then gets removed from the list_of_processes (we need to clear it all to end the cycle)
                    self.list_of_processes.remove(arrival)

            ready_queue.sort(key=lambda x: (x.remaining_time, -x.priority, x.pid))
            #then we sort the ready queue by the processes with the least remaining time
            #followed by the biggest priority as a tiebreaker
            #and the final tiebreaker being the smallest process ID (unique)

            #From now on, there are 3 states the processor is going to be in
            #and therefore 3 things it can do accordingly

            #If the processor is in the idle state (aka i gotta pick a new process to run)
            if self.state == "i":
                #First try to see if something is in the ready queue
                if len(ready_queue)>0:
                    #If there is a process we can run, we move to the running state
                    self.state = "r"
                    #the process with the shortest remaining time is always at [0], so we run that
                    self.current_process = ready_queue[0]
                    #it runs for for 1s, so the remaining time is decreased by 1s
                    self.current_process.remaining_time -=tempo
                    #because it ran for 1s, the "current running time" increases by 1
                    #this will be used in conjunction with the Quantum time later on
                    self.current_process.crt +=tempo
                    #we then put the data of what process is being ran at the current time (eg. at time 0)
                    self.graph_data.append((self.current_process.pid,timer))
                    #and then we advance the timer (otherwise it'd say it was running at time 1, not 0)
                    timer +=1
                    #If the process is done after being ran for 1s (just got picked)
                    if self.current_process.remaining_time == 0:
                        #then we put the processor in idle (pick another processor) state
                        self.state = "i"
                        #give the process object it's own completed time
                        self.current_process.completed_time = timer
                        #and change the lists its in
                        ready_queue.remove(self.current_process)
                        self.completed.append(self.current_process)
                    #If for some reason the quantum is 1 and the context switching is 0 (there's no context switching)
                    elif self.quantum == 1 and self.context_switching_amount == 0:
                        #then that means we're going to have pick a new process every time
                        self.state = "i"
                    #if the process is not complete, and the processor doesnt have to choose a new process
                    #every single time, we do a few other checks
                    else:
                        #if the processor has reached quantum (usually, if quantum is 1)
                        if self.current_process.crt == quantum:
                            #reset it's running state
                            self.current_process.crt = 0
                            for arrival in self.list_of_processes:
                                #check the object's "arrival time" attribute
                                if arrival.arrival_time == timer:
                                    #if it's time to enter the ready queue, it does
                                    ready_queue.append(arrival)
                                    #and then gets removed from the list_of_processes (we need to clear it all to end the cycle)
                                    self.list_of_processes.remove(arrival)
                            ready_queue.sort(key=lambda x: (x.remaining_time, -x.priority, x.pid))
                            #after we did another sort (and checking if a new process arrived)
                            #we check to see if the new process to be run is what we're running
                            #or if it's a new process; because if it's new, we have context switch
                            if self.current_process == ready_queue[0]:
                                self.state = "i"
                            else:
                                self.state = "c"
                #If there's nothing int the ready queue, 2 cases happen
                else:
                    #If we're just waiting on more processes, then we'll wait
                    if len(self.list_of_processes)>0:
                        self.graph_data.append(("i",timer))
                        timer +=1
                    #If there's nothing in the ready queue and we're waiting on nothing else
                    else:
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
                    #make the state of the cpu idle, so that it can properly run the latest process
                    self.state = "i"
            #if the cpu is busy running, we are in the "running" state (aka "r")
            #we would only ever enter here if the quantum > 1. 
            elif self.state == "r":
                self.current_process.remaining_time -= tempo
                self.current_process.crt += 1
                self.graph_data.append((self.current_process.pid,timer))
                timer +=1
                #Quick check to see if the process is done
                if self.current_process.remaining_time == 0:
                    self.state = "i"
                    self.current_process.completed_time = timer
                    ready_queue.remove(self.current_process)
                    self.completed.append(self.current_process)
                else:
                    #check to see if the process has reached quantum
                    if self.current_process.crt == self.quantum:
                        self.current_process.crt = 0
                        for arrival in self.list_of_processes:
                            #check the object's "arrival time" attribute
                            if arrival.arrival_time == timer:
                                #if it's time to enter the ready queue, it does
                                ready_queue.append(arrival)
                                #and then gets removed from the list_of_processes (we need to clear it all to end the cycle)
                                self.list_of_processes.remove(arrival)
                        ready_queue.sort(key=lambda x: (x.remaining_time, -x.priority, x.pid))
                        #again, even if we've reached quantum, but the process to run is the same
                        #we run it without going to context switching
                        if self.current_process == ready_queue[0]:
                            self.state = "i"
                        else:
                            #if context switching is 0, then immediately pick another process
                            if self.context_switching_amount == 0:
                                self.state = "i"
                            #if not, spend a minimum of 1 in context switching
                            else:
                                self.state = "c"
            #this is for the graph data, we need to append it before we increase the timer
            if self.state == "c":
                self.graph_data.append(("c",timer))
        #once the entire code runs, we return graph data, with everything necessary for the correct graph!
        return self.graph_data