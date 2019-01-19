#!/usr/bin/env python3
# Name: Ioannis Anastopoulos
# Date: 01/31/2018

import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches #patches in in charge of rectangles
import numpy as np
import sys
import math
from collections import defaultdict
from random import sample

def file_parse():
	data_dict=defaultdict(list)

	fn = open(sys.argv[1])
	lines = fn.readlines()
	for line in lines: 
		bins=int(line.split()[0].split('_')[3])
		reads=float(line.split()[1])
		if bins <= 10 and reads>=75:
			data_dict[bins].append(reads)
		if bins >10 and reads>=75:
			data_dict[11].append(reads)

	return data_dict

########----------------------Canvas--------------------##########

plt.style.use('BME163.mplstyle') 
width=7
height=3
plt.figure(figsize=(width,height))  #units are always inches
########----------------------Canvas--------------------##########

########----------------------Main panel dimensions--------------------##########
panel_width=5/width 
panel_height=2/height
panel=plt.axes([0.1,0.2,panel_width,panel_height]) #this adds axis labels
########----------------------Main panel dimensions--------------------##########

########----------------------Swarm PLot--------------------##########

panel.plot([0.491, 11.51], [95, 95], color='black', dashes=[4,8,8,8], linewidth=0.5, zorder=0)

for k in file_parse().keys():
	sorted_data=(sorted(sample(file_parse()[k],1000)))
	x_values=[k]*len(sorted_data)
	y_values=sorted_data

	median = np.median(y_values)
	rectangle=mplpatches.Rectangle((k-0.4,median),0.8,0.15,
										facecolor='red',
										edgecolor='red',
										linewidth=0) 
	panel.add_patch(rectangle)


	used_points=[(x_values[0],y_values[0])]
	#plot first point
	panel.scatter(used_points[0][0],used_points[0][1],s=0.5,
				linewidth=0,
				facecolor='black')	
	left=True
	c=0.023
	for i in range(1,len(y_values)): # skips first point because its already been plotted
		for used_point in used_points: # all the points in used_points are before y_values[i] because data is sorted
			y_pos= used_point[1]
			dy=y_values[i]-y_pos
			if dy<c: # checking distance to all the previous points
				dx=np.sqrt(c**2-dy**2) #calculating how much to shift on x-axis
				if left:
					x_values[i]-=dx
				elif not left:
					x_values[i]+=dx
			else:
				x_values[i]=k
		used_points.append((x_values[i],y_values[i])) #appending points below y_values[i] that have already been plotted

		left = not left #allows for symmetrical spread of points
	
	panel.scatter(x_values,y_values,s=0.5,linewidth=0,facecolor='black')

########----------------------Swarm PLot--------------------##########


panel.tick_params(axis='both', which='both',bottom='on', labelbottom='on', left='on', labelleft='on', 
					right='off', labelright='off', 
					top='off', labeltop='off')


panel.set_xlim(0.5,11.5)
panel.set_ylim(75,100)
panel.set_xticks([1,2,3,4,5,6,7,8,9,10,11])
x_labels=['1','2','3','4','5','6','7','8','9','10','>10']
panel.set_xticklabels(x_labels)
panel.set_ylabel(r'Identity (%)')
panel.set_xlabel(r'Subread coverage')
plt.savefig('Anastopoulos_Ioannis_BME163_Assignment_Week4.png', dpi=600)


