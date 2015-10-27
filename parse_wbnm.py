# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 08:12:09 2015

@author: mghughes
"""
from datetime import datetime as dt
from datetime import timedelta as td

fid = r"S:\B21273.g.nc_Mayne v DTMR\Hydrology\Rainfall_analysis\Events\JAN2008\MM_Jan08_03d_Meta.out"
t0 = dt.strptime('15/01/2008 09:00', "%d/%m/%Y %H:%M")
tmin = dt.strptime('16/01/2008 09:00', "%d/%m/%Y %H:%M")
tmax = dt.strptime('19/01/2008 09:00', "%d/%m/%Y %H:%M")

def main(fid):
    with open(fid, 'rb') as f:
        found = False
        for line in f:
            if "END_HYDROGRAPHS" in line:
                found = False
                h, d = reader(x)
                w = []
                t = []
                for i in range(len(d['Rain'])):
                    t = t0 + td(hours=float(d['Time'][i])/60)
                    if t >= tmin and t <= tmax:
                        #print t, d['Time'][i], d['Rain'][i]
                        w.append(float(d['Rain'][i]))                  
                        y = sum(w)

                #print str("loc_%s, " % loc[0]), y
                print loc[0], y
                
            if found == True:
                try:
                    x.append(line.split())
                except:
                    continue
                
            if "START_HYDROGRAPHS" in line:
                found = True
                loc = line[23:27].split()
                x = []

def reader(f):
    header = f[0]
    reader = f[1:-1]
    col = {}
    for i in header:
        col[i] = []
    for row in reader:
        for h, v in zip(header, row):
            col[h].append(v.strip())
    return header,col

main(fid)