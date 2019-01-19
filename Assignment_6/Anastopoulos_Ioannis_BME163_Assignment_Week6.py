#!/usr/bin/env python3
# Name: Ioannis Anastopoulos
# Date: 02/21/2018
import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import matplotlib.image as mpimg
import sys
from collections import defaultdict
import math

def file_parser():
	total_list=[]
	fn = open(sys.argv[1])
	lines = fn.readlines()
	for line in lines[1:]:
		lst=np.array(list(map(int,(line.split()[4:12]))))
		total_list.append((lst,float(line.split()[13])))
	return total_list
########----------------------Canvas--------------------##########

plt.style.use('BME163.mplstyle') 
width=5
height=3
plt.figure(figsize=(width,height))  #units are always inches
########----------------------Canvas--------------------##########

########----------------------Main panel dimensions--------------------##########
panel1_width=0.75/width 
panel1_height=2.5/height
panel2_width=2.5/width 
panel2_height=2.5/height
panel1=plt.axes([0.1,0.1,panel1_width,panel1_height])
panel2=plt.axes([0.35,0.1,panel2_width,panel2_height],frameon=False)
########----------------------Main panel dimensions--------------------##########

########----------------------heatmap--------------------##########

R=np.linspace(255/255,56/255,101)
G=np.linspace(225/255,66/255,101)
B=np.linspace(40/255,157/255,101)


lst=sorted(file_parser(),key=lambda x:x[1], reverse=True)

y_pos=0

peak_lst=[]
for random_list in lst:
	ct=random_list[1]
	peak_lst.append(random_list[1])

	normalized_y_data=((random_list[0]-min(random_list[0]))/(max(random_list[0])-min(random_list[0])))*100
	x_pos=-1
	for point in normalized_y_data:
		rectangle=mplpatches.Rectangle([x_pos,y_pos],3,1,facecolor=(R[int(point)],G[int(point)],B[int(point)]),linewidth=0)
		panel1.add_patch(rectangle)
		x_pos+=3
	y_pos+=1

panel1.set_xlim(-1,23)
panel1.set_ylim(0,len(lst))
########----------------------heatmap--------------------##########

for circle_tuple in ((np.pi*2,0,200),(np.pi*2,0,300),(np.pi*2,0,400)):
	x_list=[]
	y_list=[]
	for rad in np.linspace(circle_tuple[0],circle_tuple[1],50):
		x_pos=np.cos(rad)*circle_tuple[2]
		y_pos=np.sin(rad)*circle_tuple[2]
		x_list.append(x_pos)
		y_list.append(y_pos)

	panel2.plot(x_list,y_list,color='black',dashes=[6,8,12,8],linewidth=0.3, zorder=3)

thick_radius=np.arange(80,100,1)
for circle_tuple in ((np.pi/2,3*np.pi/2,thick_radius),(np.pi/2,3*np.pi/2,thick_radius),(3*np.pi/2,9*np.pi/2,80),(3*np.pi/2,9*np.pi/2,100)):
	x_list=[]
	y_list=[]
	for rad in np.linspace(circle_tuple[0],circle_tuple[1],100):
		x_pos=np.cos(rad)*circle_tuple[2]
		y_pos=np.sin(rad)*circle_tuple[2]
		x_list.append(x_pos)
		y_list.append(y_pos)

	panel2.plot(x_list,y_list,color='black',linewidth=0.3, zorder=3)

y_histo, bins=np.histogram(peak_lst, np.arange(0,26,2))

start=np.pi/2
end=(np.pi/2)-(np.pi/6)
#Lori helped with this: thanks lori!
for i in range(len(y_histo)):
	angle_tuple = ((np.pi*(((-1/6)*i)+0.5)),(np.pi*(((-1/6)*(i+1)+0.5))))

	start_x=np.cos(angle_tuple[0])*100
	start_y=np.sin(angle_tuple[0])*100

	next_start_x = np.cos(angle_tuple[0]-(np.pi/6))*100
	next_start_y = np.sin(angle_tuple[0]-(np.pi/6))*100

	end_x = np.cos(angle_tuple[1]+(np.pi/6))*(y_histo[i]+100)
	end_y = np.sin(angle_tuple[1]+(np.pi/6))*(y_histo[i]+100)

	next_end_x = np.cos(angle_tuple[1])*(y_histo[i]+100)
	next_end_y = np.sin(angle_tuple[1])*(y_histo[i]+100)
	#plotting vertical lines
	panel2.plot([start_x,end_x],[start_y,end_y], color='black', linewidth=0.4, zorder=3)
	panel2.plot([next_start_x,next_end_x],[next_start_y,next_end_y], color='black', linewidth=0.4, zorder=3)

for y in y_histo:
	grey_area=np.arange(100,(100+y),1)

	circle_tuple = (start,end,100+y)
	grey_tuple=(start,end,grey_area)
	x_list=[]
	y_list=[]
	for rad in np.linspace(circle_tuple[0],circle_tuple[1],100):
		x_pos=np.cos(rad)*circle_tuple[2]
		y_pos=np.sin(rad)*circle_tuple[2]
		x_list.append(x_pos)
		y_list.append(y_pos)
		
	panel2.plot(x_list,y_list,color='black',linewidth=0.4)
	grey_x=[]
	grey_y=[]
	for rad in np.linspace(grey_tuple[0],grey_tuple[1],50):
		x_pos=np.cos(rad)*grey_tuple[2]
		y_pos=np.sin(rad)*grey_tuple[2]
		grey_x.append(x_pos)
		grey_y.append(y_pos)
	panel2.plot(grey_x,grey_y,color='grey',linewidth=1, zorder=0) #grey panels

		
	start=end
	end-=np.pi/6


panel2.set_xlim(-400,400)
panel2.set_ylim(-400,400)

panel2.tick_params(axis='both',which='both', bottom='off', right='off', left='off', top='off',labelbottom='off',labelleft='off',labeltop='off',labelright='off') 
panel2.text(-244.5, -7, '100', fontsize=6, horizontalalignment='left')
panel2.text(-344.5, -7, '200', fontsize=6, horizontalalignment='left')
panel2.text(-444.5, -7, '300', fontsize=6, horizontalalignment='left')

panel2.text(0, 0, 'CT', fontsize=6, horizontalalignment='center',verticalalignment='center')
panel2.text(0, 50, '0', fontsize=6, horizontalalignment='center',verticalalignment='center')
panel2.text(0, -50, '12', fontsize=6, horizontalalignment='center',verticalalignment='center')
panel2.text(43, 25, '4', fontsize=6, horizontalalignment='center',verticalalignment='center')
panel2.text(-43, 25, '20', fontsize=6, horizontalalignment='center',verticalalignment='center')
panel2.text(43, -25, '8', fontsize=6, horizontalalignment='center',verticalalignment='center')
panel2.text(-43, -25, '16', fontsize=6, horizontalalignment='center',verticalalignment='center')
x_labels=['0','','6','','12','','18','']
panel1.set_xticks([0.5,3.5,6.5,9.5,12.5,15.5,18.5,21.5])

panel1.set_xticklabels(x_labels)
panel1.set_ylabel(r'Number of genes')
panel1.set_xlabel(r'CT')
plt.savefig('Anastopoulos_Ioannis_BME163_Assignment_Week6.png')
