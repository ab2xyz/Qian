#!/home/i/Install/anaconda3/bin/python

## Author: ABC2XYZ


import datetime
import pandas as pd
import os
from pandas_datareader import data


symbols={'wti':'CLM20.NYM','brent':'BZM20.NYM','gold':'GC=F','silver':'SI=F'}


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


t0=datetime.datetime(2020,4,20,0,0,0)

for symbol in symbols:
    sym=symbols[symbol]
    price=data.get_quote_yahoo(sym).price.values[0]

    iCSV=dataFolder+symbol+'.csv'

    try:
        dataCSV=pd.read_csv(iCSV)
    except :
        dataCSV=pd.DataFrame(columns=list(range(1440)))

    t=datetime.datetime.now()
    dT=(t-t0).seconds//60

    iRow=dT//1440
    iCol=dT % 1440

    print(iRow,iCol)
    dataCSV.loc[iRow,iCol]=price

    print(dataCSV)

    dataCSV.to_csv(iCSV,index=False)










#
