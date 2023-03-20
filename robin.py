class processDetails:
    def __init__(self, process_number, arrival_time, burst_time, priority):
        self.process_number = process_number
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
            time_to_complete = self.remaining_time
            self.remaining_time = 0
            return time_to_complete


# read in the input file
filename = "input.txt"
with open(filename) as f:
    num_processes = int(f.readline())
    processes = []
    for i in range(num_processes):
        process_params = f.readline().strip().split()
        process_number, arrival_time, burst_time, priority = [int(x) for x in process_params]
        processes.append(Process(process_number, arrival_time, burst_time, priority))


time_quantum = 2
ready_queue = deque()
current_time = 0
num_processes_executed = 0
total_wait_time = 0
total_turnaround_time = 0