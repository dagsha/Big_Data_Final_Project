
# coding: utf-8

# In[76]:

#!/usr/bin/env python
import sys
sys.path.append('.')
import matplotlib
matplotlib.use('Agg')
from matplotlib.path import Path
from rtree import index as rtree
import numpy, shapefile, time, datetime
import numpy as np
import csv
import pandas as pd
import itertools
from operator import itemgetter

#Read the neibhourhood centriod lat lon file
centriod_info = pd.read_csv('centriod.csv')

def sort_input(filename):
    #Open the input file to read the data
    
    list_t =[]
    with open(filename+".csv") as data:
        content = data.readlines()  
        
    for line in content:  
        line = line.strip('\n')
        
        list_t.append(line)
        
        
    list_t = sorted(list_t, key=itemgetter(0,1))
    for i in list_t:
        print i
    
   
        
        
    
#Creat a csv file corresponding to each input file. This new file has additional centriod Lat Lon information
#for each pickup and dropof neibhourhoods
def parseInput(filename):
    
    #Open the output file to write the final results
    writer = csv.writer(open(filename+".csv", 'wb'))
    
    #Open the input file to read the data    
    with open(filename) as data:
        content = data.readlines()      
  
    #dictionary = {}
    for line in content:   
        line = line.strip('\n')
        #print line
        key, count            = line.split('\t')
        day, hour, pick, drop = key.strip().split(',')
        if (pick != "UNKNOWN") & (drop != "UNKNOWN"):        
            pick_lat = centriod_info[(centriod_info['Neibhourhood'] == pick)].Lat.values[0]
            pick_lon = centriod_info[(centriod_info['Neibhourhood'] == pick)].Lon.values[0]            
            drop_lat = centriod_info[(centriod_info['Neibhourhood'] == drop)].Lat.values[0]
            drop_lon = centriod_info[(centriod_info['Neibhourhood'] == drop)].Lon.values[0]
            
            tmp = str(pick)+"," +"("+str(pick_lat)+","+str(pick_lon)+")"+","+str(drop)+","+"("+str(drop_lat)+","+str(drop_lon)+")"
            tmp = str(day)+","+str(hour)+","+tmp+","+count
            pick_lat_lon = "("+str(pick_lat)+","+str(pick_lon)+")"
            drop_lat_lon = "("+str(drop_lat)+","+str(drop_lon)+")"
            
            #value = pick+drop+count
            #keys  = (day,hour)
            #if dictionary.has_key(keys):
            #    dictionary[keys] += value
            #else:
            #    dictionary[keys]  = value
                
            writer.writerow([day,hour,pick,pick_lat_lon,drop,drop_lat_lon,count])  
    
    #print dictionary
        
if __name__=='__main__':
    
    for fname in ['Top10_Pick_Drop']: #,'Stadium_High_Bridge','Stadium_Flushing','Stadium_Garment','Stadium_Fort_Green']:
        parseInput(fname)
        sort_input(fname)
    
    
    


# In[ ]:



