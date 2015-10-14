# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 12:34:47 2015

@author: mgh
"""

from pydap.client import open_url
import numpy as np
from datetime import datetime as dt
from datetime import timedelta as td

global xmin, xmax, ymin, ymax, tmin, tmax, tdel
xmin = 140
xmax = 150
ymin = -12
ymax = -2
tmin = dt.strptime('04/08/2002 00:00', "%d/%m/%Y %H:%M") #missing data around 3-4/08/2002 
tmax = dt.strptime('31/07/2015 00:00', "%d/%m/%Y %H:%M")
tdel = 3

def main():
#    time_range = td.hours(tmax - tmin)
#    print time_range
    time_range = 50000
    for i in range(0,time_range,tdel):
        print i
        URL, fout = make_URL(i)
        data, LLX, LLY = fetch_data(URL)
        write_data(fout, data, LLX, LLY)

def make_URL(ts_hours):
    TRMM_URL = 'http://disc2.nascom.nasa.gov/opendap/hyrax/TRMM_3Hourly_3B42/'
    TRMM_DateTime  = tmin + td(hours=ts_hours)
    TRMM_prevday   = tmin + td(hours=ts_hours-1)
    year_prevday = TRMM_prevday.strftime('%Y')
    doy_prevday  = TRMM_prevday.strftime('%j')
    year = TRMM_DateTime.strftime('%Y')
    dom  = TRMM_DateTime.strftime('%d')
    month= TRMM_DateTime.strftime('%m')
    hour = TRMM_DateTime.strftime('%H')
    if int(year) < 2000:
        URL  = str('%s%s/%s/3B42.%s%s%s.%s.7.HDF.Z') % (TRMM_URL, year_prevday, doy_prevday, year, month, dom, hour)
        fout = str('output\TRMM_%s%s%s%s.asc' % (year, month, dom, hour))
    else:
        URL  = str('%s%s/%s/3B42.%s%s%s.%s.7A.HDF.Z') % (TRMM_URL, year_prevday, doy_prevday, year, month, dom, hour)
        fout = str('output\TRMM_%s%s%s%s.asc' % (year, month, dom, hour))
    return URL, fout

def fetch_data(URL):
    cnt = 0
    while True:
        if cnt > 10:
            break
        else:
            try:
                dataset = open_url(URL)
                var = dataset['precipitation']
                lon = np.array(dataset['nlon'])
                lat = np.array(dataset['nlat'])
                ind_LonMin = int(np.argmin(abs(lon-float(xmin))))
                ind_LonMax = int(np.argmin(abs(lon-float(xmax))))
                ind_LatMin = int(np.argmin(abs(lat-float(ymin))))
                ind_LatMax = int(np.argmin(abs(lat-float(ymax))))
                Data = var[ind_LonMin:ind_LonMax, ind_LatMin:ind_LatMax]
                LLX  = lon[ind_LonMin]
                LLY  = lat[ind_LatMin]
            except:
                cnt = cnt + 1
                print 'fetch atempt ', cnt
                continue
            break

    d = np.flipud(Data.T)
    return d, LLX, LLY

def write_data(fout, var, XLL, YLL):
    fout = open(fout, 'wb')
    fout.write('NCOLS %s\n' % str(var.shape[0]))
    fout.write('NROWS %s\n' % str(var.shape[1]))
    fout.write('XLLCENTER %s\n' % XLL)
    fout.write('YLLCENTER %s\n' % YLL)
    fout.write('CELLSIZE 0.25\n')
    fout.write('NODATA_VALUE -999.0\n')
    np.savetxt(fout, var, fmt='%.2f', delimiter=' ')
    fout.close()

main()

