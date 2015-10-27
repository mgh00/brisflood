# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 08:12:09 2015

@author: mghughes
"""


fid = r"S:\B21273.g.nc_Mayne v DTMR\Hydrology\Rainfall_analysis\Events\JAN2008\MM_Jan08_03d_Meta.out"

with open(fid, 'rb') as f:
    found = False
    for line in f:
        if "START_HYDROGRAPHS" in line:
            print line
            