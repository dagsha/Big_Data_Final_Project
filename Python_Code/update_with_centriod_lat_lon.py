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
    
#Creat a csv file corresponding to each input file. 
#This new file has additional centriod Lat Lon information for each pickup and dropof neibhourhoods
def parseInput(filename):
    
    #Open the output file to write the final results
    writer = csv.writer(open(filename+".csv", 'wb'))
    
    #Open the input file to read the data    
    with open(filename) as data:
        content = data.readlines()      
  
    for line in content:   
        line = line.strip('\n')
        key, count            = line.split('\t')
        day, hour, pick, drop = key.strip().split(',')
        if (pick != "UNKNOWN") & (drop != "UNKNOWN"):        
            pick_lat = centriod_info[(centriod_info['Neibhourhood'] == pick)].Lat.values[0]
            pick_lon = centriod_info[(centriod_info['Neibhourhood'] == pick)].Lon.values[0]            
            drop_lat = centriod_info[(centriod_info['Neibhourhood'] == drop)].Lat.values[0]
            drop_lon = centriod_info[(centriod_info['Neibhourhood'] == drop)].Lon.values[0]
            
            pick_lat_lon = "("+str(pick_lat)+","+str(pick_lon)+")"
            drop_lat_lon = "("+str(drop_lat)+","+str(drop_lon)+")"
          
        writer.writerow([day,hour,pick,pick_lat_lon,drop,drop_lat_lon,count])  
        
if __name__=='__main__':
    
    for fname in ['Top10_Pick_Drop', 'Stadium_High_Bridge','Stadium_Flushing','Stadium_Garment','Stadium_Fort_Green']:
        parseInput(fname)
    
