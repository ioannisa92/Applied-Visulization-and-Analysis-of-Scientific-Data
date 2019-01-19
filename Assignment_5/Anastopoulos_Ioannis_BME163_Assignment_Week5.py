#!/usr/bin/env python3
# Name: Ioannis Anastopoulos
# Date: 01/31/2018

import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import matplotlib.image as mpimg
import sys
from collections import defaultdict
import math

#parsing the bed file
def file_parse():
	fn = open(sys.argv[2])
	lines = fn.readlines()
	for line in lines: 
		chromosome=line.split()[0].strip()
		splice_position=int(line.split()[1].strip())
		splice_type= line.split()[3][0].strip()
		yield chromosome,splice_position,splice_type
#parsing the fasta file
def readFasta ():
	header = ''
	sequence = ''
	
	with open(sys.argv[1]) as fileH:
		header = ''
		sequence = ''
		# skip to first fasta header
		line = fileH.readline()
		while not line.startswith('>') :
			line = fileH.readline()
		header = line[1:].rstrip()

		for line in fileH:
			if line.startswith ('>'):
				yield header,sequence
				header = line[1:].rstrip()
				sequence = ''
			else :
				sequence += ''.join(line.rstrip().split()).upper()
					
		yield header,sequence



plt.style.use('BME163.mplstyle')

########----------------------Canvas--------------------##########

plt.style.use('BME163.mplstyle') 
width=6
height=3
plt.figure(figsize=(width,height))  #units are always inches
########----------------------Canvas--------------------##########

########----------------------Main panel dimensions--------------------##########
panel_width=2.4/width 
panel_height=1/height
panel1=plt.axes([0.1,0.3,panel_width,panel_height])
panel2=plt.axes([0.55,0.3,panel_width,panel_height])
########----------------------Main panel dimensions--------------------##########

###variables for each image###
A=mpimg.imread('A.png')
C=mpimg.imread('C.png')
T=mpimg.imread('T.png')
G=mpimg.imread('G.png')
###variables for each image###

total_reads_5=0 #total counts for 5 prime reads
total_reads_3=0 #total counts for 3 prime reads
five_prime_dict = {k:'' for k in range(20)} #{position: all bases in that position}
three_prime_dict = {k:'' for k in range(20)} #{position: all bases in that position}

for h,s in readFasta():
	for chromosome,splice_position,splice_type in file_parse():
		chr_length=list(map(int, h.split()[2].split(':')[3:5])) #length of each chromosome
		### transforming 1 to chr1, etc.
		if h.split()[0].isdigit() or h.split()[0]=='X' or h.split()[0]=='Y':
			k = (h.split()[0].replace(h.split()[0],'chr'+h.split()[0]), chr_length, s) #tuple of (chr,chr length,sequence)
		if h.split()[0]=='MT':
			k = (h.split()[0].replace(h.split()[0],'chrM'),chr_length, s) #tuple of (chr,chr length,sequence)

		if k[0]==chromosome and splice_position in range(int(k[1][0]),int(k[1][1])): #if chromosomes match and splice site within chromosome length
			if splice_type=='5':
				total_reads_5+=1
				sequence=k[2][splice_position-10:splice_position+10].upper() #getting sequence -10 +10 bases 
				for i in range(20):
					five_prime_dict[i]+=sequence[i]
			if splice_type=='3':
				total_reads_3+=1
				sequence=k[2][splice_position-10:splice_position+10].upper()#getting sequence -10 +10 bases 
				rev_sequence=sequence[::-1].upper() #reversing sequence
				for i in range(20):
					###getting complements of reverse sequence
					if rev_sequence[i]=='A':
						three_prime_dict[i]+='T'
					if rev_sequence[i]=='C':
						three_prime_dict[i]+='G'
					if rev_sequence[i]=='G':
						three_prime_dict[i]+='C'
					if rev_sequence[i]=='T':
						three_prime_dict[i]+='A'
					###getting complements of reverse sequence

def logo_plot(panel,dct, total_reads):
	e_n=(1/np.log(2))*(3/(2*(total_reads)))			
	for k,v in dct.items():
		Hi=[]
		#counts and freq of A#
		A_count=v.count('A')
		freq_A=A_count/(total_reads)
		Hi_A=(freq_A)*np.log2(freq_A)
		Hi.append(Hi_A)
		#counts and freq of A#

		#counts and freq of C#
		C_count=v.count('C')
		freq_C=C_count/(total_reads)
		Hi_C=(freq_C)*np.log2(freq_C)
		Hi.append(Hi_C)
		#counts and freq of C#

		#counts and freq of G#
		G_count=v.count('G')
		freq_G=G_count/(total_reads)
		Hi_G=(freq_G)*np.log2(freq_G)
		Hi.append(Hi_G)

		#counts and freq of T#
		T_count=v.count('T')
		freq_T=T_count/(total_reads)
		Hi_T=(freq_T)*np.log2(freq_T)
		Hi.append(Hi_T)
		#counts and freq of G#

		Hi_sum=sum(Hi)
		Ri=np.log2(4)-(-Hi_sum+e_n)
		height_A=freq_A*Ri
		height_C=freq_C*Ri
		height_G=freq_G*Ri
		height_T=freq_T*Ri
		heights=[(height_A,A), (height_C,C), (height_G,G), (height_T,T)]
		heights_sorted=sorted(heights)

		panel.imshow(heights_sorted[0][1],extent=[k-10,k-9,0,heights_sorted[0][0]],aspect='auto')
		panel.imshow(heights_sorted[1][1],extent=[k-10,k-9,heights_sorted[0][0],heights_sorted[0][0]+heights_sorted[1][0]],aspect='auto')
		panel.imshow(heights_sorted[2][1],extent=[k-10,k-9,heights_sorted[0][0]+heights_sorted[1][0],heights_sorted[0][0]+heights_sorted[1][0]+heights_sorted[2][0]],aspect='auto')
		panel.imshow(heights_sorted[3][1],extent=[k-10,k-9,heights_sorted[0][0]+heights_sorted[1][0]+heights_sorted[2][0],heights_sorted[0][0]+heights_sorted[1][0]+heights_sorted[2][0]+heights_sorted[3][0]],aspect='auto')

logo_plot(panel1,five_prime_dict,total_reads_5)
logo_plot(panel2,three_prime_dict,total_reads_3)
##plotting perpendicular line and directionality
panel1.plot([0, 0], [0, 2.0], color='black', linewidth=0.5, zorder=2)
panel1.text(0, 2.22,"5'SS", va='center',ha='center', fontsize=9.5)
panel2.plot([0, 0], [0, 2.0], color='black', linewidth=0.5, zorder=2)
panel2.text(0, 2.22,"3'SS", va='center',ha='center', fontsize=9.5)
##plotting perpendicular line and directionality

panel1.set_xlim(-10,10)
panel1.set_ylim(0,2.0)

panel2.set_xlim(-10,10)
panel2.set_ylim(0,2.0)

panel1.set_xticks([-10,-5,0,5,10])
panel2.set_xticks([-10,-5,0,5,10])
x_labels=[r'-10',r'-5',r'0',r'5',r'10']
panel1.set_xticklabels(x_labels)
panel2.set_xticklabels(x_labels)


panel1.set_ylabel('Bits')
panel1.set_xlabel('Distance to'+'\n'+'Splice Site')
panel2.set_xlabel('Distance to'+'\n'+'Splice Site')

panel1.tick_params(axis='both', which='both',bottom='on', labelbottom='on', left='on', labelleft='on', 
					right='off', labelright='off', 
					top='off', labeltop='off')

panel2.tick_params(axis='both', which='both',bottom='on', labelbottom='on', left='off', labelleft='off', 
					right='off', labelright='off', 
					top='off', labeltop='off')

plt.savefig('Anastopoulos_Ioannis_BME163_Assignment_Week5.png')
		