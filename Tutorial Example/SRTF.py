n = int(input('Enter no of processes: '))
bt = [0] * (n + 1) #processes list set to be same as number of processes
at = [0] * (n + 1) #arrival times same as number of processes
abt = [0] * (n + 1) #burst times same as number of processes
#For loop to get the input
for i in range(n):
	abt[i] = int(input('Enter the burst time for process {} : '.format(i + 1)))
	at[i] = int(input('Enter the arrival time for process {} : '.format(i + 1))) 
	bt[i] = [abt[i], at[i], i]
bt.pop(-1)
ll = []
#for loop for the sum of burst times, total time that it will take to run
for i in range(0, sum(abt)):
	l = [j for j in bt  if j[1] <= i] #gets the processes that have arrived
	l.sort(key=lambda x: x[0]) #sorts them out by remaning burst time
	bt[bt.index(l[0])][0] -= 1 #dimish the remanining burst time by  1 to the one with less time 
	#checks if a process finished executing, if so adds it to ll followed by the exit time
	for k in bt:
		if k[0] == 0:
			t = bt.pop(bt.index(k))
			ll.append([k, i + 1])
	
ct = [0] * (n + 1)
tat = [0] * (n + 1)
wt = [0] * (n + 1)

#Lists all completion times by process number
for i in ll:
	ct[i[0][2]] = i[1] 

#Calculates turn around time and waiting time for each one
for i in range(len(ct)):
	tat[i] = ct[i] - at[i]
	wt[i] = tat[i] - abt[i]
ct.pop(-1)
wt.pop(-1)
tat.pop(-1)
abt.pop(-1)
at.pop(-1)
#Prints the results 
print('BT\tAT\tCT\tTAT\tWT')
for i in range(len(ct)):
	print("{}\t{}\t{}\t{}\t{}\n".format(abt[i], at[i], ct[i], tat[i], wt[i]))
print('Average Waiting Time = ', sum(wt)/len(wt))
print('Average Turnaround Time = ', sum(tat)/len(tat))