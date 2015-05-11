#!/usr/bin/env python
import sys
sys.path.append('.')
import matplotlib
matplotlib.use('Agg')
from matplotlib.path import Path
from rtree import index as rtree
import numpy, shapefile, time, datetime

sports_neighborhood = ['Flushing'] 

def findNeighborhood(location, index, neighborhoods):
    match = index.intersection((location[0], location[1], location[0], location[1]))
    for a in match:
        if any(map(lambda x: x.contains_point(location), neighborhoods[a][1])):
            return a
    return -1

def readNeighborhood(shapeFilename, index, neighborhoods):
    sf = shapefile.Reader(shapeFilename)
    for sr in sf.shapeRecords():
        if sr.record[1] not in ['New York', 'Kings', 'Queens', 'Bronx']: continue
        paths = map(Path, numpy.split(sr.shape.points, sr.shape.parts[1:]))
        bbox = paths[0].get_extents()
        map(bbox.update_from_path, paths[1:])
        index.insert(len(neighborhoods), list(bbox.get_points()[0])+list(bbox.get_points()[1]))
        neighborhoods.append((sr.record[3], paths))
    neighborhoods.append(('UNKNOWN', None))

def parseInput():
    for line in sys.stdin:
        line = line.strip('\n')
        values = line.split(',')
        if len(values)>1 and values[0]!='medallion': 
            yield values

def dayStrToNum(dayStr):
    if dayStr == "Sunday":
        return 1
    elif dayStr == "Monday":
        return 2
    elif dayStr == "Tuesday":
        return 3
    elif dayStr == "Wednesday":
        return 4
    elif dayStr == "Thursday":
        return 5
    elif dayStr == "Friday":
        return 6
    elif dayStr == "Saturday":
        return 7
        
    
def mapper():
    index = rtree.Index()
    neighborhoods = []
    readNeighborhood('ZillowNeighborhoods-NY.shp', index, neighborhoods)
    agg = {}
    
    for values in parseInput():
        
        try:
            #Day of the week    
            year, month, day = values[5].split()[0].strip().split('-')
            temp = datetime.date(int(year), int(month), int(day))
            dayStr = temp.strftime("%A")
            dayNum = dayStrToNum(str(dayStr))
        
            #Time of the day
            hour  = values[5].split()[1].strip().split(':')[0]

            print values[12], values[13]
            pickup_location = (float(values[10]), float(values[11]))
            dropoff_location = (float(values[12]), float(values[13]))
            pickup_neighborhood = findNeighborhood(pickup_location, index, neighborhoods)
            dropoff_neighborhood = findNeighborhood(dropoff_location, index, neighborhoods)              
    
            if pickup_neighborhood!=-1 & dropoff_neighborhood!=-1:   
                pickup_nh_name  = neighborhoods[pickup_neighborhood][0]
                dropoff_nh_name =  neighborhoods[dropoff_neighborhood][0]          
                if (pickup_nh_name in sports_neighborhood) | (dropoff_nh_name in sports_neighborhood):
                    print '%d,%d,%s,%s\t%d' % (dayNum, int(hour), pickup_nh_name, dropoff_nh_name,1)
        except:
            continue
       
if __name__=='__main__':
    mapper()

