#!/home/i/Install/anaconda3/bin/python

## Author: ABC2XYZ


import datetime
# import pandas as pd
import os
from pandas_datareader import data
import numpy as np

# symbolDict={'wti':'CLM20.NYM','brent':'BZM20.NYM','gold':'GC=F','silver':'SI=F'}

from symbolDict import symbolDict

'''
*/1 * * * * /home/i/Qian/code/RecordData.py
'''

if os.getcwd()==os.environ['HOME']:
    folder=os.getcwd()+'/Qian/'
else:
    folder=os.path.dirname(os.getcwd())+'/'

os.makedirs(folder,exist_ok=True)


dataFolder=folder+'dataRecord/'

os.makedirs(dataFolder,exist_ok=True)


t0=datetime.datetime(2020,4,22,0,0,0)

for symbol in symbolDict:
    sym=symbolDict[symbol]

    price=data.get_quote_yahoo(sym).price.values[0]

    iDat=dataFolder+symbol+'.dat'

    try:
        dat=np.loadtxt(iDat)
    except :
        dat=np.zeros((365,1440))

    t=datetime.datetime.now()
    dT=(t-t0).seconds//60

    iRow=dT//1440
    iCol=dT % 1440


    dat[iRow,iCol]=price

    np.savetxt(iDat,dat,fmt='%.3f',)











#
