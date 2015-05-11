#!/usr/bin/env python
import itertools, operator, sys

def parseInput():    
    for line in sys.stdin:
        yield line.strip('\n').split('\t')

def reducer():    
    agg = list()
    current_day = -1
    current_hour = -1
    
    for key, values in itertools.groupby(parseInput(), operator.itemgetter(0)):
  
        try:
            day = int(key.split(',')[0].strip())
            hour = int(key.split(',')[1].strip()) 
          
            if ((day != current_day) | (hour != current_hour)) & (current_day != -1) & (current_hour != -1):
                top10 = sorted(agg, key=lambda tup: tup[1], reverse=True) [:10]
                for x in top10:
                    print '%s\t%d' %(x[0],x[1])
                agg[:] = []
            
            count = sum(map(int, zip(*values)[1]))
            tup=(key,int(count))
            agg.append(tup)
            current_day = day
            current_hour = hour
            
        except:
            continue
  
    if (len(agg) != 0):
        top10 = sorted(agg, key=lambda tup: tup[1], reverse=True) [:10]
        for x in top10:
            print '%s\t%d' %(x[0],x[1])                
        
            
if __name__=='__main__':
    reducer()
