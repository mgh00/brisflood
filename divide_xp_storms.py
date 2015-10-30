#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mghughes
#
# Created:     11/02/2015
# Copyright:   (c) mghughes 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():


#    path = 'K:\\B20047.k.abm_Cal South DA Assistance\\Flood_Modelling\\Hydrology\\Area_1to4_Consolidation\\RAFTS\\WDB\\'
#    XP_results = path+'Results_DIS_loc.csv'
    XP_results = 'B21273_10y_all_tot.csv'
#    f_out = open(path+'temp', 'w')
    f_out = open('temp', 'w')


    with open(XP_results, 'rb') as f_in:
        for line in f_in:
            if "Storm" in line:
                fid = 'MAX_'+line.strip()+'_tot.csv'
#                f_out = open(path+fid, 'w')
                f_out = open(fid, 'w')
                next(f_in)
            else:
                f_out.write(line.strip()+'\n')

main()

