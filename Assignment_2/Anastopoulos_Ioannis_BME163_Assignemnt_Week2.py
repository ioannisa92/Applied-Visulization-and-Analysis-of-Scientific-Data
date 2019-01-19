#!/usr/bin/env python3
# Name: Ioannis Anastopoulos
# Date: 01/20/2018

import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches #patches in in charge of rectangles
import numpy as np
import sys
import math

##Parsing file from command line input
def file_parse():
	x_values=[]
	y_values=[]
	fn = open(sys.argv[1])
	lines = fn.readlines()[1:]
	for line in lines:
		x_values.append(float(line.split('\t')[1:][0].strip()))
		y_values.append(float(line.split('\t')[1:][1].strip()))
	return x_values, y_values
###Getting x and y values and log2 converting them
x_values,y_values = file_parse()
log_x_values=list(map(lambda x: math.log2(x+1), x_values))
log_y_values=list(map(lambda y: math.log2(y+1), y_values))


########----------------------Canvas--------------------##########
plt.style.use('BME163.mplstyle') #you ge the the style sheet from him
width=5
height=2
plt.figure(figsize=(width,height))  #units are always inches
########----------------------Canvas--------------------##########

panel1_width=1/width 
panel1_height=1/height
side_panel1_width=0.25/width 
side_panel1_height=1/height
top_panel1_width=1/width 
top_panel1_height=0.25/height

panel1=plt.axes([0.14,0.15,panel1_width,panel1_height]) #this adds axis labels
side_panel1=plt.axes([0.076,0.15,side_panel1_width,side_panel1_height]) #this adds axis labels
top_panel1=plt.axes([0.14,0.685,top_panel1_width,top_panel1_height]) #this adds axis labels

########----------------------Main panel--------------------##########
panel1.scatter(log_x_values,log_y_values,s=2,
				linewidth=0,
				facecolor='black',
				alpha = 0.1)
########----------------------Main panel--------------------##########


########----------------------Top panel--------------------##########

x_histo, bins=np.histogram(log_x_values,np.arange(0,15,0.5))
for values in np.arange(0,len(x_histo)):
	left=bins[values]
	bottom=0
	height=x_histo[values]
	width=bins[values+1]-bins[values]
	rectangle=mplpatches.Rectangle((left,bottom),width,math.log2(height+1),
									facecolor=(0.5,0.5,0.5),
									edgecolor='black',
									linewidth=0.1) 
	top_panel1.add_patch(rectangle)
y_histo, bins=np.histogram(log_y_values,np.arange(0,15,0.5))
########----------------------Top panel--------------------##########


########----------------------Side panel--------------------##########
for values in np.arange(0,len(y_histo)):
	left=0
	bottom=bins[values]
	height=y_histo[values]
	width=bins[values+1]-bins[values]
	rectangle=mplpatches.Rectangle((left,bottom),math.log2(height+1),width,
									facecolor=(0.5,0.5,0.5),
									edgecolor='black',
									linewidth=0.1) 
	side_panel1.add_patch(rectangle)
########----------------------Side panel--------------------##########


########----------------------Modifying panel axis labels--------------------##########

panel1.tick_params(axis='both', which='both',bottom='on', labelbottom='on', left='off', labelleft='off', 
					right='off', labelright='off', 
					top='off', labeltop='off')
side_panel1.tick_params(axis='both', which='both',bottom='on', labelbottom='on', left='on', labelleft='on', 
					right='off', labelright='off', 
					top='off', labeltop='off')
top_panel1.tick_params(axis='both', which='both',bottom='off', labelbottom='off', left='on', labelleft='on', 
					right='off', labelright='off', 
					top='off', labeltop='off')
panel1.set_xlim(0,15)
panel1.set_ylim(0,15)
side_panel1.set_xlim(20,0)
side_panel1.set_ylim(0,15)
top_panel1.set_xlim(0,15)
top_panel1.set_ylim(0,20)
########----------------------Modifying panel axis labels--------------------##########


plt.savefig('Anastopoulos_Ioannis_BME163_Assignemnt_Week2.png', dpi=600)

