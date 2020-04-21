#!/home/i/Install/anaconda3/bin/python

## Author: ABC2XYZ

from pandas_datareader import data
import pandas as pd
import os
import time
import datetime

import numpy as np

from skpy import Skype
from getpass import getpass

numItemSend=10
deltaTSecond=1


if os.getcwd()==os.environ['HOME']:
    folder=os.getcwd()+'/Qian/'
else:
    folder=os.path.dirname(os.getcwd())+'/'

os.makedirs(folder,exist_ok=True)


def DataRealTimeGet(symbol='wti'):
    if symbol=='wti':
        sym='CLM20.NYM'

    if symbol=='brent':
        sym='BZM20.NYM'

    if symbol=='gold':
        sym='GC=F'

    if symbol=='silver':
        sym='SI=F'

    if symbol=='rmb':
        sym='CNH=F'

    price=data.get_quote_yahoo(sym).price.values[0]

    return price

def DataRealTimeProcess(symbols=['wti'],dTSec=2,nRun=3):
    tLast=time.time()

    price=np.zeros((len(symbols)))
    for iRun in range(nRun):
        tNow=time.time()


        dt=tLast+dTSec-tNow
        while dt<0:
            dt+=dTSec

        time.sleep(dt)
        tLast=time.time()

        for idxSym in range(len(symbols)):
            symbol=symbols[idxSym]

            iPrice=DataRealTimeGet(symbol=symbol)
            iPrice=USD2RMB(symbol,iPrice)

            price[idxSym]+=iPrice

    price/=nRun

    return price



def USD2RMB(symbol,iPrice):
    rmb=DataRealTimeGet(symbol='rmb')
    if symbol in ['gold' ,'silver']:
        iPrice*=rmb/28.3495*0.9
    return iPrice


symbols=['brent','gold','wti' ,'silver']

os.makedirs(folder+'RealTimeData',exist_ok=True)
try:
    dataRealTime=pd.read_csv(folder+'RealTimeData/dataRealTime.csv')

except:
    dataRealTime=pd.DataFrame(columns=[symbols])

m,n=dataRealTime.shape

price=DataRealTimeProcess(symbols=symbols,dTSec=deltaTSecond,nRun=3)

dataRealTime.loc[m,:]=price

dataRealTime.to_csv(folder+'RealTimeData/dataRealTime.csv',index=False)




try:

    strNow=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    I="ab2xyz@outlook.com"

    sk = Skype(user=I,  pwd="JiangPeiyong")

    # try:
    #     sk = Skype(user=I, tokenFile=".tokens-ab2xyz")
    # except:
    #     sk = Skype(user=I,  pwd=getpass(), tokenFile=".tokens-ab2xyz")

    ch=sk.contacts["live:.cid.1e1b64af8c3d6bc5"].chat

    ch.sendMsg('                                 ')
    strNow=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    ch.sendMsg(strNow)

    head='{:>5s} {:>4s} {:>7s} {:>4s} {:>5s} {:>4s} {:>5s} {:>4s}'.format('b','%','g','%','w','%','s','%')
    ch.sendMsg(head)

    y=dataRealTime.values
    dy=(np.log(dataRealTime.values[1:,:]/dataRealTime.values[:-1,:]))
    mSend=min(numItemSend,dy.shape[0])

    ySend=y[-mSend:,:]
    dySend=dy[-mSend:,:]




    for idxSend in range(mSend):

        iContent='{:>2.2f} {:>+0.3f} | {:>4.2f} {:>+0.3f} | {:>2.2f} {:>+0.3f} | {:>2.2f} {:>+0.3f}' .format(ySend[idxSend,0],dySend[idxSend,0],
        ySend[idxSend,1],dySend[idxSend,1],\
        ySend[idxSend,2],dySend[idxSend,2],\
        ySend[idxSend,3],dySend[idxSend,3])

        ch.sendMsg(iContent)


except:

    print('Skype Failed')


'''
# crontab　{-l | -e|-r}
# -l  　显示当前的crontab
# -r　　删除当前的crontab
# -e　　使用编辑器编辑当前的crontab文件
# m h  dom mon dow   command
1 * * * * /home/i/Qian/code/LongPrediction.py
11 * * * * /home/i/Qian/code/LongPrediction.py
21 * * * * /home/i/Qian/code/LongPrediction.py
31 * * * * /home/i/Qian/code/LongPrediction.py
41 * * * * /home/i/Qian/code/LongPrediction.py
51 * * * * /home/i/Qian/code/LongPrediction.py

3 * * * * /home/i/Qian/code/ShortWatcher.py
13 * * * * /home/i/Qian/code/ShortWatcher.py
23 * * * * /home/i/Qian/code/ShortWatcher.py
33 * * * * /home/i/Qian/code/ShortWatcher.py
43 * * * * /home/i/Qian/code/ShortWatcher.py
53 * * * * /home/i/Qian/code/ShortWatcher.py


'''




#
