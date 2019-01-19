#!/usr/bin/env python3
# Name: Ioannis Anastopoulos
# Date: 01/28/2018

import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches #patches in in charge of rectangles
import numpy as np
import sys
import math

def file_parse():
	fold_change=[]
	p_value=[]
	genes =[]
	data=[]
	fn = open(sys.argv[1])
	lines = fn.readlines()
	for line in lines:
		# data.append((line.split('\t')[0].strip(),float(line.split('\t')[1].strip().replace('NA','1')),float(line.split('\t')[2].strip().replace('NA','1'))))
		genes.append(line.split('\t')[0].strip())
		fold_change.append(float(line.split('\t')[1].strip().replace('NA','1')))
		p_value.append(float(line.split('\t')[2].strip().replace('NA','1')))
	return genes,fold_change,p_value
###Getting gene names, fold change, and converting p values to -log10
genes, fold_change,p_value = file_parse()
neg_log10_p_values=list(map(lambda y: -1*np.log10(y), p_value))
########----------------------Canvas--------------------##########
plt.style.use('BME163.mplstyle') 
width=3
height=3
plt.figure(figsize=(width,height))  #units are always inches
########----------------------Canvas--------------------##########

########----------------------Main panel dimensions--------------------##########
panel_width=2/width 
panel_height=2/height
panel=plt.axes([1/6,1/6,panel_width,panel_height]) #this adds axis labels
########----------------------Main panel dimensions--------------------##########

x_values3=[]
y_values3=[]
x_values1=[]
y_values1=[]
genes1=[] # gene names if their fold-change (not log2(fold-change)) is larger than 10 (only down) and their -log10(p-value) is greater than 30.
x_values2=[]
y_values2=[]
for i,e in enumerate(neg_log10_p_values):
	if fold_change[i]<-np.log2(10) and e>30:
		x_values1.append(fold_change[i])
		y_values1.append(e)
		genes1.append(genes[i])
	if fold_change[i]>+np.log2(10) and e>8 or fold_change[i]<-np.log2(10) and e>8:
		x_values2.append(fold_change[i])
		y_values2.append(e)
	else:
		x_values3.append(fold_change[i])
		y_values3.append(e)

panel.scatter(x_values3,y_values3,s=2,
				linewidth=0,
				facecolor='black')
panel.scatter(x_values2,y_values2,s=2.2,
				linewidth=0,
				facecolor='red')
panel.scatter(x_values1,y_values1,s=2.2,
				linewidth=0,
				facecolor='red')
for i,e in enumerate(genes1):
	panel.text(x_values1[i]-0.3, y_values1[i],e, va='center',ha='right', fontsize=6)

########----------------------Modifying panel axis labels--------------------##########

panel.tick_params(axis='both', which='both',bottom='on', labelbottom='on', left='on', labelleft='on', 
					right='off', labelright='off', 
					top='off', labeltop='off')

panel.set_xlim(-12,12)
panel.set_ylim(0,60)
panel.set_xlabel(r'$log_2(fold$ change)')
panel.set_ylabel(r'-log$_{10}$(p-value)')

plt.savefig('Anastopoulos_Ioannis_BME163_Assignemnt_Week3.png', dpi=600)
