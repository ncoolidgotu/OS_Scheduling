class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.switch_time = arrival_time
        self.current = 0
        self.burst_used = 0

class Robin:
    def processData(self, processes, quantumTime, contextSwitchTime):
        process_data = []
        self.quantumTime = quantumTime
        self.contextSwitchTime = contextSwitchTime
        for process in processes:
            temporary = []
            temporary.extend([process.pid, process.arrival_time, process.burst_time, 0, process.burst_time])
            '''
            '0' is the state of the process. 0 means not executed and 1 means execution complete
            '''
            process_data.append(temporary)
        return Robin.schedulingProcess(self, process_data, quantumTime, contextSwitchTime)
    
    def schedulingProcess(self, process_data, quantumTime, contextSwitchTime):
        run_queue = []
        ready_queue = []
        completed = []
        time = 0
        repeat = False
        
        process_data.sort(key=lambda x: (x.arrival_time, -x.priority, x.pid)) #Sort according to arrival time
        
        while True:
            for i in range(len(process_data)):
                if process_data[0].arrival_time == time:
                    ready_queue.append(process_data[0])
                    process_data.remove(process_data[0])
                else:
                    break
            if len(ready_queue) != 0:
                ready_queue.sort(key=lambda x: (x.switch_time, -x.priority, x.pid))
        
                #Add process to CPU
                if time >= ready_queue[0].switch_time and len(run_queue) == 0 or repeat == True: #If CPU is empty
                    run_queue.append(ready_queue[0]) #Add process to running queue and remove from ready
                    ready_queue.remove(ready_queue[0])
                    
                    if run_queue[0].burst_used + quantum >= run_queue[0].burst_time: #If the burst time used exceeds next quantum
                        myTime = run_queue[0].burst_time - run_queue[0].burst_used #The time used will be the remaining burst time
                    else:
                        myTime = quantum #Otherwise the time used will be the quantum time
                        
                    run_queue[0].burst_used += myTime #The burst time used during this run
                    run_queue[0].current += myTime + time #current time is time used during this run + time already past
                    
                if run_queue[0].current == time: #if the current time flag on the process is the current time
                    if run_queue[0].burst_used == run_queue[0].burst_time: #If process has finished
                        repeat == False
                        completed.append(run_queue[0])
                        run_queue.remove(run_queue[0])
                        if len(ready_queue) == 0 and len(run_queue) == 0:
                            print("poop")
                            
                    elif len(ready_queue) == 0:
                        repeat == True
                            
                    else: #If process needs to move back to ready queue and save context
                        repeat == False
                        run_queue[0].switch_time = run_queue[0].current + contextSwitchTime
                        ready_queue.append(run_queue[0])
                        run_queue.remove(run_queue[0])
                        
                    
                for proc in run_queue:
                    print('proc', proc.pid, end='')
                    print(' burst', proc.burst_used, end='')
                print()
                    
                print(time)
                print(len(process_data))
                print(len(ready_queue))
                print(len(run_queue))
            
            if len(process_data) == 0 and len(ready_queue) == 0 and len(run_queue) == 0:
                break
            
            time +=1


#[pid,at,bt,pt] 
data = [[1,1,3,1]]
processes = []

for i in data:
    processes.append(Process(i[0],i[1],i[2],i[3]))

quantum = 2
context = 0

rb = Robin()

rb.schedulingProcess(processes,quantum,context)
