
class FCFS:
    print("FIRST COME FIRST SERVE SCHEDULLING")
    n = int(input("Enter number of processes : ")) #number of processes in the program
    d = dict() #dictionary of algorithm
    for i in range(n):
        key = "P" + str(i + 1)
        arrival = int(input("Enter arrival time of process " + str(i + 1) + ": "))
        burst = int(input("Enter burst time of process " + str(i + 1) + ": "))
        list = []
        list.append(arrival)
        list.append(burst)
        d[key] = list
        print(d[key])
    print(d) #print the list
    d = sorted(d.items(), key=lambda item: item[1][0]) #sorts based on arrival time
    print(d)
    print(len(d)) #length of the list
    ET = [] #exit time list
    for i in range(len(d)):
        # first process
        if (i == 0): #takes the first arriving process and stores it in the exit time list
            ET.append(d[i][1][1])

        # get prevET + newBT
        else: #algorithm for checking exit times of other elements
            if d[i][1][0] > ET[i-1]: #checking if the arrival time is greater than the exit time, to account for if there are gaps between processes running
                ET.append(d[i][1][0] +d[i][1][1])
            else: #checking burst time and arrival times
                ET.append(ET[i - 1] + d[i][1][1]) #check if arrival time  > completion time of last process
                print(ET[i - 1])
                print(d[i][1][1])
    print(ET)
    TAT = []
    for i in range(len(d)): #creating the turn around values
        TAT.append(ET[i] - d[i][1][0])

    WT = []
    for i in range(len(d)):
        if TAT[i] - d[i][1][1] < 0:
            WT.append(0)
        else:
            WT.append(TAT[i] - d[i][1][1])

    avg_WT = 0
    for i in WT:
        avg_WT += i
    avg_WT = (avg_WT / n)

    print("Process | Arrival | Burst | Exit | Turn Around | Wait | Response Time")
    for i in range(n):
        print("   ", d[i][0], "   |   ", d[i][1][0], " |    ", d[i][1][1], " |    ", ET[i], "  |    ", TAT[i], "  |   ",
              WT[i], "   |  ", WT[i])
    print("Average Waiting Time: ", avg_WT)

FCFS()