class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.switch_time = arrival_time
        self.current = 0

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
        time = 0
        context_switching = False
        im_context_switching = 0
        
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
                if time >= ready_queue[0].switch_time and len(run_queue) == 0:
                    run_queue.append(ready_queue[0])
                    run_queue[0].current += quantum
                    
                if run_queue[0].current == time:
                    run_queue[0].switch_time = run_queue[0].switch_time + self.contextSwitchTime
                    ready_queue.append(run_queue[0])
                    
                
                print(ready_queue)
                print(time)
                
            time +=1

            
            #if context_switching
                #im_context_switching += 1

            #else
                #if CPU len == 0
                    #get a process in
                #else
                    #work on the process

            

            #QUANTUM AT THE END
            #have i reached my limit      
            #if im_context_switching == self.contextswitch
            #reset value
            #process in cpu switch time update
            #move process from cpu to the ready queue

            time +=1

#[pid,at,bt,pt] 
data = [[1,1,3,1],[2,1,6,6],[3,2,2,2],[4,4,2,3]]
processes = []

for i in data:
    processes.append(Process(i[0],i[1],i[2],i[3]))

quantum = 2
context = 1

rb = Robin()

rb.schedulingProcess(processes,quantum,context)
