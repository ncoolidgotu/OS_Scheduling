import matplotlib.pyplot as plt

left_coordinates=[1,2,3,4,5]
heights=[10,20,30,15,40]
bar_labels=['One','Two','Three','Four','Five']
plt.bar(left_coordinates,heights,tick_label=bar_labels,width=1)
plt.xlabel('Time')
plt.ylabel('Process ID')
plt.title("Graph Name Goes Here")
plt.show()