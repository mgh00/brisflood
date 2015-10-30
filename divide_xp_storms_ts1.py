#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
# this scrip take RAFTS csv output (Results >> Export Timeseries Results...)
# and converts all storms within the file to ts1 format
#-------------------
# DOESN"T QUITE WORK PROPERLY, DOESN"T OUTPUT LAST SET OF RESULTS
#-------------------
# Author:      mghughes
#
# Created:     11/02/2015
# Copyright:   (c) mghughes 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import csv

def main():
    XP_results = r"S:\B21273.g.nc_Mayne v DTMR\Hydrology\XPRAFTS\Local_MaxMayne\results\MM_RESULTS_ALLyr36hr_013.csv"
    path = r"S:\B21273.g.nc_Mayne v DTMR\Hydrology\XPRAFTS\Local_MaxMayne\results"
#    f_out = open('temp', 'w')
    with open(XP_results, 'rb') as f_in:
        count = 0
        data = []
        stormid = ''
        for line in f_in:
            if line == '':
                next
            if "Storm" in line:
                if count > 1:
                    outid = data[0].replace(' ', '').strip()
                    fid = str(path+'\%s.ts1' % outid)
                    f_out = open(fid, 'wb')
                    
                    h, d = reader(data[1:-1])
                    f_out.write('! %s\n' % outid)
                    f_out.write('%s, %s\n' % (str(len(h)), str(len(d['Time']))))
                    
                    f_out.write('Start_Index,')
                    for i in range(len(h)):
                        if i == 0:
                            next                    
                        elif i == len(h)-1:
                            f_out.write('1\n')
                        else:
                            f_out.write('1,')
                            
                    f_out.write('End_Index,')
                    for i in range(len(h)):
                        if i == 0:
                            next                        
                        elif i == len(h)-1:
                            f_out.write('%s\n' % len(d['Time']))
                        else:
                            f_out.write('%s,' % len(d['Time']))    
                    
                    f_out.write('Time (min),')
                    for i in range(len(h)):
                        if i == 0:
                            next
                        elif i == len(h)-1:
                            f_out.write('%s\n' % h[i])
                        else:
                            f_out.write('%s,' % h[i])    
                    
                    for i in range(len(d['Time'])):
                        for j in range(len(h)):
                            if j == len(h)-1:
                                f_out.write('%s\n' % d[h[j]][i])
                            elif j == 0:
                                f_out.write('%s,' % str(float(d[h[j]][i])*60))
                            else:
                                f_out.write('%s,' % d[h[j]][i])
     
                data = []
                count = 1
                f_in.next()
            if count >= 1:
                data.append(line)
                count = count + 1


def reader(f):
    reader = csv.reader(f, delimiter=',', quotechar='"')
    header = reader.next()
    col = {}
    for i in header:
        col[i] = []
    for row in reader:
        for h, v in zip(header, row):
            col[h].append(v.strip())
    return header,col

main()
