#!/usr/bin/env python
import itertools, operator, sys

sports_neighborhood = ['High Bridge'] 

def parseInput():    
    for line in sys.stdin:
        yield line.strip('\n').split('\t')

def reducer():    
    pick_up_stadium = list()
    drop_off_stadium = list()
    agg = list()
    current_day = -1
    current_hour = -1
    
    for key, values in itertools.groupby(parseInput(), operator.itemgetter(0)): 
        
        try:
            day     = int(key.split(',')[0].strip())
            hour    = int(key.split(',')[1].strip()) 
            pick_up = key.split(',')[2].strip()
        
            if ((day != current_day) | (hour != current_hour)) & (current_day != -1) & (current_hour != -1):                      
                if (len(pick_up_stadium) != 0):                  
                    top10 = sorted(pick_up_stadium, key=lambda tup: tup[1], reverse=True) [:10]
                    for x in top10:
                        print '%s\t%d' %(x[0],x[1])
                    pick_up_stadium[:] = []
                    
                if (len(drop_off_stadium) != 0):
                    top10 = sorted(drop_off_stadium, key=lambda tup: tup[1], reverse=True) [:10]
                    for x in top10:
                        print '%s\t%d' %(x[0],x[1])
                    drop_off_stadium[:] = []
                            
            count = sum(map(int, zip(*values)[1]))
            tup=(key,int(count))
            if pick_up in sports_neighborhood:            
                pick_up_stadium.append(tup)
            else:
                drop_off_stadium.append(tup)
            current_day = day
            current_hour = hour
            
        except:
            continue

    if (len(pick_up_stadium) != 0):
        top10 = sorted(pick_up_stadium, key=lambda tup: tup[1], reverse=True) [:10]
        for x in top10:
            print '%s\t%d' %(x[0],x[1])
        pick_up_stadium[:] = []
                    
    if (len(drop_off_stadium) != 0):     
        top10 = sorted(drop_off_stadium, key=lambda tup: tup[1], reverse=True) [:10]
        for x in top10:
            print '%s\t%d' %(x[0],x[1])
        drop_off_stadium[:] = []

if __name__=='__main__':
    reducer()   
