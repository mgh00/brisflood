#------------------------------------------------------------------------------
# Name:        Example timeseries plot of TUFLOW results
# Purpose:     Deomonsrate usage of TUFLOW_Results class
#
# Author:      MGH
#
# Created:     15/04/2015
# Copyright:   (c) BMT WBM
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Import the required modules

import matplotlib.pyplot as plt
from datetime import datetime as dt
from datetime import timedelta as td
import csv

#global G_head, G_data, M_head, M_data

#"D:\B21273.g.nc_Mayne v DTMR\Hydraulics\tuflow\results\COM_1012_exg_018_PO.csv"
#"D:\B21273.g.nc_Mayne v DTMR\Hydraulics\tuflow\results\plot\csv\COM_1012_exg_018_2d_Q.csv"
run_id = 'COM_1012_exg_018'
locations = [str("Q THE LAKE ALERT [%s]" % run_id), \
str("Q Springsure Creek Junction [%s]" % run_id), \
str("Q Lake Brown [%s]" % run_id), \
str("Q CometWeir [%s]" % run_id)]

#THELAKE_fid = open(r"S:\B21273.g.nc_Mayne v DTMR\Hydraulics\tulow_GPU\Calibration\130506A_201512.csv",'r')
#THELAKE_datum = 0 #185.695

Gauge_fid = open(r"S:\B21273.g.nc_Mayne v DTMR\Hydraulics\tulow_GPU\Calibration\Gauges_dec2010.csv",'r')
Gauges_datum = 0

Model_fid = open(str(r'D:\B21273.g.nc_Mayne v DTMR\Hydraulics\tuflow\results\plot\csv\%s_2d_Q.csv' % run_id),'r')
Model_start_date = dt.strptime('22/12/2010 09:00', "%d/%m/%Y %H:%M")

def main(Gauge_fid, Gauge_loc, datum, Model_fid, Model_loc):
    Gauge_time, Gauge_data = fetch_gauge(Gauge_fid, Gauge_loc, datum)
    model_time, model_data = fetch_model(Model_fid, Model_loc)
    draw_fig(Gauge_time, Gauge_data, model_time, model_data, Gauge_loc)
        
def fetch_gauge(Gauge_data_fid, dtype, Gauge_datum):
    G_head, G_raw = reader(Gauge_data_fid)
    G_time = []
    G_data = []
    for i in range(len(G_raw['date'])):
        G_time.append(dt.strptime(G_raw['date'][i], "%d/%m/%Y %H:%M"))
        G_data.append(Gauge_datum + float(G_raw[dtype][i]))
    return G_time, G_data

def fetch_model(Model_data_fid, dtype):
    M_head, M_raw = reader(Model_data_fid)
    M_time =[]
    M_data = []
    for i in range(len(M_raw['Time (h)'])):
        M_time.append(Model_start_date + td(hours=float(M_raw['Time (h)'][i])))
        M_data.append(float(M_raw[dtype][i]))
    return M_time, M_data

def draw_fig(G_time, G_data, M_time, M_data, title_text):
    fig = plt.figure() #create new figure
#    locs, labels = fig.xticks()
#    plt.setp(labels, rotation=90)
    
    ax = fig.add_axes((0.10, 0.15, 0.85,0.75)) #add axis to figure
    ax.plot(G_time, G_data,color='b',label='Gauge Flow Rate')
    ax.plot(M_time, M_data,color='r',label='Model Flow Rate')
    
    locs, labels =plt.xticks()
    plt.setp(labels, rotation=90)
    # manage plot
    ax.set_xlabel('Date')
    ax.set_ylabel('Flow Rate (m3/s)')
    ax.set_title(title_text)
    ax.grid()
    ax.legend(loc=2)
    plt.show()

def reader(f):
    f.seek(0)
    reader = csv.reader(f, delimiter=',', quotechar='"')
    header = reader.next()
    col = {}
    for i in header:
        col[i] = []
    for row in reader:
        for h, v in zip(header, row):
            col[h].append(v.strip())
    return header,col


#main(THELAKE_fid, Model_fid, locations[0])
main(Gauge_fid, 'Comet at the Lake', Gauges_datum, Model_fid, str("Q 130506A [%s]" % run_id))
#main(Gauge_fid, 'Lake Brown', Gauges_datum, Model_fid, locations[2])
#main(Gauge_fid, 'CometWeir', Gauges_datum, Model_fid, locations[3])
#main(Gauge_fid, 'Springsure Creek Junction', Gauges_datum, Model_fid, locations[1])

Gauge_fid.close()
Model_fid.close()