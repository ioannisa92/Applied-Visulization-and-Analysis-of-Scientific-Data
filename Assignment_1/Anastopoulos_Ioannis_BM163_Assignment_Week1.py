#!/usr/bin/env python3
# Name: Ioannis Anastopoulos
# Date: 01/14/2018


import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches #patches in in charge of rectangles
import numpy as np
import math

plt.style.use('BME263.mplstyle') 
width=3.42
height=2
plt.figure(figsize=(width,height))  #units are always inches
panel_width=1/width #1 are the inches that the jounral wants the figures
panel_height=1/height

####-----------------------------panel_1----------------------------------####
panel1=plt.axes([0.1,0.2,panel_width,panel_height]) #this adds axis labels
RGB_colors=np.linspace(0,1,10)
pi_range=np.linspace(0,np.pi/2, 25)
for numbers in pi_range:
	panel1.plot([math.cos(numbers)],[math.sin(numbers)],
		        marker='o',
		        linewidth=0, 
		        markeredgecolor=None,
		        markerfacecolor=(math.cos(numbers),math.cos(numbers),math.cos(numbers)),
		        markeredgewidth=0,
		        markersize=2) 

panel1.tick_params(axis='both', which='both',bottom='off', labelbottom='off', left='off', labelleft='off', 
					right='off', labelright='off', 
					top='off', labeltop='off')
####-----------------------------panel_1----------------------------------####

####-----------------------------panel_2----------------------------------####
cyan=(0,1,1)
magenta=(1,0,1)
blue=(0,0,1)

panel2=plt.axes([0.55,0.2,panel_width,panel_height])
for numbers in range(10):
	for number in range(10):
		rectangle=mplpatches.Rectangle((number/10,numbers/10),0.1,0.1,
										facecolor=(number/10,numbers/10,1),
										edgecolor='black',
										linewidth=1) 
		panel2.add_patch(rectangle)


panel2.tick_params(axis='both', which='both',bottom='off', labelbottom='off', left='off', labelleft='off', 
					right='off', labelright='off', 
					top='off', labeltop='off')
####-----------------------------panel_2----------------------------------####

plt.savefig('Anastopoulos_Ioannis_BM163_Assignment_Week1.png', dpi=600)









