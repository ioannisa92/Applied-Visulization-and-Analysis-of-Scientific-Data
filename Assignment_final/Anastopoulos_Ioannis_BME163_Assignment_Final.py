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


########----------------------Canvas--------------------##########

plt.style.use('BME163.mplstyle') 
width=10
height=5
plt.figure(figsize=(width,height))  #units are always inches
########----------------------Canvas--------------------##########

########----------------------Main panel dimensions--------------------##########
panel_width=10/width 
panel_height=1.25/height

panel1=plt.axes([0,0.05,panel_width,panel_height])
panel2=plt.axes([0,0.35,panel_width,panel_height])
panel3=plt.axes([0,0.65,panel_width,panel_height])

########----------------------Main panel dimensions--------------------##########



def gtf_parser():
	t_ID=defaultdict(list)
	total=0
	with open(sys.argv[1]) as f:
		lines=f.readlines()
		for line in lines:
			line=line.split()
			if line[0]=='chr7':
				r_type=line[2]
				if int(line[3]) in range(45232945,45240000) or int(line[4]) in range(45232945,45240000):
					if r_type=='CDS' or r_type=='exon' or r_type=='transcript':
						t_ID[line[11]].append((line[2],int(line[3]),int(line[4])))
					
						total+=1
	print('total shit', total)
	return t_ID

t_ID=gtf_parser()
t_ID_coordinates=[]
for k,v in t_ID.items():
	for element in v:
		if element[0]=='transcript':
			t_ID_coordinates.append((k,element))
t_ID_coordinates=sorted(t_ID_coordinates, key=lambda x:x[1][2])

def plot_panel3(ens_id,y_pos):
	v=t_ID[ens_id[0]]
	for element in v:
		width=element[2]-element[1]
		if element[0]=='CDS':
			rectangle=mplpatches.Rectangle([element[1],y_pos],width,0.5,facecolor='black',linewidth=0)
			panel3.add_patch(rectangle)
		elif element[0]=='exon':
			rectangle=mplpatches.Rectangle([element[1],y_pos+0.125],width,0.25,facecolor='black',linewidth=0, zorder=3)
			panel3.add_patch(rectangle)
		elif element[0]=='transcript':
			rectangle=mplpatches.Rectangle([element[1],y_pos+0.175],width,0.1,facecolor='black',linewidth=0, zorder=3)
			panel3.add_patch(rectangle)
plotted=[]
y_pos=-0.21
for k in t_ID_coordinates:
	if k not in plotted:
		y_pos+=1
		plotted.append(k)
		plot_panel3(k,y_pos)
	for v in t_ID_coordinates:
		last_element=plotted[-1]
		range1=range(last_element[1][1],last_element[1][2])
		range2=range(v[1][1],v[1][2])
		overlap=set(range1).intersection(range2)
		if len(overlap)==0 and v not in plotted:
			plotted.append(v)
			plot_panel3(v,y_pos)
		else:
			continue


def psl_parser(psl,reverse=False):
	coordinates=[]
	with open(psl) as f:
		lines=f.readlines()
		for line in lines:
			line=line.split()
			if line[13] == 'chr7':
				al_start=int(line[15])
				al_end=int(line[16])
				block_width=line[18]
				block_start=line[20]
				if al_start in range(45232945,45240000) or al_end in range(45232945,45240000):
					coordinates.append((al_start,al_end,block_width,block_start))
	if reverse:
		coordinates=sorted(coordinates, key=lambda x:x[1])
	else:
		coordinates=sorted(coordinates, key=lambda x:x[0])
	return coordinates

panel2_file=sys.argv[2]
panel1_file=sys.argv[3]

coordinates=psl_parser(panel2_file, reverse=True)
coordinates2=psl_parser(panel1_file, reverse=True)


def plot_panel1(coordinates):
	y=0
	for element in coordinates:

		block_starts=list(map(int,element[3].split(',')[:-1]))
		block_widths=list(map(int,element[2].split(',')[:-1]))
		# print(block_starts, block_widths)
		line=element[1]-element[0]
		rectangle1=mplpatches.Rectangle([element[0],y+0.15],line,0.01,facecolor='grey',linewidth=0,zorder=3)
		panel1.add_patch(rectangle1)
		
		for i in range(len(block_starts)):
			start=block_starts[i]
			width=block_widths[i]
			rectangle2=mplpatches.Rectangle([start,y],width,0.3,facecolor='grey',linewidth=0)
			panel1.add_patch(rectangle2)

		y+=0.225
plot_panel1(coordinates2)


def plot_panel2(element, y):
	block_starts=list(map(int,element[3].split(',')[:-1]))
	block_widths=list(map(int,element[2].split(',')[:-1]))
	# print(block_starts, block_widths)
	line=element[1]-element[0]
	rectangle1=mplpatches.Rectangle([element[0],y+0.15],line,0.01,facecolor='black',linewidth=0,zorder=3)
	panel2.add_patch(rectangle1)
	
	for i in range(len(block_starts)):
		start=block_starts[i]
		width=block_widths[i]
		rectangle2=mplpatches.Rectangle([start,y],width,0.3,facecolor='black',linewidth=0)
		panel2.add_patch(rectangle2)

plotted2=[]
y=0
for i in range(len(coordinates)):
	if i not in plotted2:
		y+=0.575
		plotted2.append(i)
		plot_panel2(coordinates[i], y)
	for j in range(len(coordinates)):
		last=plotted2[-1]
		if j not in plotted2:
			if coordinates[j][0]>coordinates[last][1]:
				plotted2.append(j)
				plot_panel2(coordinates[j],y)



panel1.tick_params(axis='both',which='both', bottom='off', right='off', left='off', top='off',labelbottom='off',labelleft='off',labeltop='off',labelright='off') 
panel2.tick_params(axis='both',which='both', bottom='off', right='off', left='off', top='off',labelbottom='off',labelleft='off',labeltop='off',labelright='off') 
panel3.tick_params(axis='both',which='both', bottom='off', right='off', left='off', top='off',labelbottom='off',labelleft='off',labeltop='off',labelright='off') 
panel3.set_xlim(45232945,45240000)
panel3.set_ylim(0,10)
panel2.set_xlim(45232945,45240000)
panel2.set_ylim(0,40)
panel1.set_xlim(45232945,45240000)
panel1.set_ylim(0,100)
panel1.set_xticks([])
panel2.set_xticks([])
panel3.set_xticks([])
plt.savefig('Anastopoulos_Ioannis_BME163_Assignment_Final.png', dpi=1200)
