#!/home/i/Install/anaconda3/bin/python

## Author: ABC2XYZ
from pandas_datareader import data, wb
import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime,time
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

from skpy import Skype
from getpass import getpass


def DataGet(update=0,symbol='brent'):
    os.makedirs(folder+'DataPredictionLong',exist_ok=True)
    if not update:
        return

    if symbol=='brent':
        dataYahooBrent =  data.DataReader(name = 'BZM20.NYM',data_source = 'yahoo', start='1900-01-01')  # Brent     2020-01-03
        dataYahooBrent.to_csv(folder+'DataPredictionLong/dataYahooOilBrent.csv')

    if symbol=='wti':

        # WTI    2000-03-02
        dataYahooWTI =  data.DataReader(name = 'CLM20.NYM',data_source = 'yahoo', start='1900-01-01')  # WTI    2000-03-02
        dataYahooWTI.to_csv(folder+'DataPredictionLong/dataYahooOilWTI.csv')

    if symbol=='gold':
        # Gold    2000-02-28
        dataYahooGold =  data.DataReader(name = 'GC=F',data_source = 'yahoo', start='1900-01-01')  # Gold    2000-02-28
        dataYahooGold.to_csv(folder+'DataPredictionLong/dataYahooGold.csv')

    if symbol=='silver':
        # Silver    2000-02-28
        dataYahooSilver =  data.DataReader(name = 'SI=F',data_source = 'yahoo', start='1900-01-01')  # Silver    2000-02-28
        dataYahooSilver.to_csv(folder+'DataPredictionLong/dataYahooSilver.csv')


def DataPredict(xData,numPred=3,numSamples=200):
    x=xData.copy()
    dx=np.log(x[1:]/x[:-1])

    xCan=x[-1]*np.linspace(0.8,2.2,numSamples)


    windowList=[5,7,9]

    numXCan=len(xCan)
    rel=np.zeros((numXCan))

    for iNum in range(numPred):
        for idxCan in range(numXCan):
            xTmp=np.r_[x,xCan[idxCan]]
            dxTmp=np.r_[dx,np.log(xTmp[-1]/xTmp[-2])]

            for idxWindow in range(len(windowList)):
                iWindow=windowList[idxWindow]
                xTmpFilter=savgol_filter(xTmp,iWindow,3)
                dxTmpFilter=savgol_filter(dxTmp,iWindow,3)

                # errX=np.sum((xTmpFilter[-iWindow:-1]-x[-iWindow+1:])**2)
                # errDX=np.sum((dxTmpFilter[-iWindow:-1]-dx[-iWindow+1:])**2)

                # errX=np.sum((xTmpFilter[-iWindow:-1]-xTmp[-iWindow:-1])**2)
                # errDX=np.sum((dxTmpFilter[-iWindow:-1]-dxTmp[-iWindow:-1])**2)

                errX=np.sum((xTmpFilter[:-iNum-1]-xTmp[:-iNum-1])**2)
                errDX=np.sum((dxTmpFilter[:-iNum-1]-dxTmp[:-iNum-1])**2)

                rel[idxCan]+=errX*1+errDX


        xPred=xCan[np.argmin(rel)]
        x=np.r_[x,xPred]

    xPrediction=x.copy()

    return xPrediction





def DataProcess(symbol='wti',window=7,daysFrom=200,daysEnd=0,numPred=3,numSamples=200,columns=['Open','High','Low','Adj Close'],flagInterplate=1):
    if symbol=='brent':
        data=pd.read_csv(folder+'DataPredictionLong/dataYahooOilBrent.csv')
    if symbol=='wti':
        data=pd.read_csv(folder+'DataPredictionLong/dataYahooOilWTI.csv')
    if symbol=='gold':
        data=pd.read_csv(folder+'DataPredictionLong/dataYahooGold.csv')
    if symbol=='silver':
        data=pd.read_csv(folder+'DataPredictionLong/dataYahooSilver.csv')

    if len(columns)==1:
        columns.extend(columns)


    colsPreProcess=['Open','High','Low','Close','Adj Close']
    for iCol in colsPreProcess:
        data.loc[data[iCol]==0,iCol]=data.loc[data[iCol]==0,'Adj Close']





    cols=data.columns.to_list()

    tNow=datetime.datetime.now()

    t=np.array([(datetime.datetime.strptime(x,'%Y-%m-%d')-tNow).days if '-' in x else (datetime.datetime.strptime(x,'%Y/%m/%d')-tNow).days for x in data.Date])


    v=data[columns].values


    if daysEnd<=numPred:
        tUse=t[-daysFrom:]
        vUse=v[-daysFrom:,:]

    else:
        tUse=t[-daysFrom:-daysEnd+numPred]
        vUse=v[-daysFrom:-daysEnd+numPred,:]

    vUse[vUse<=0]=1


    fInterp=interp1d(tUse,vUse,axis=0)

    if flagInterplate==1:
        tInterp=np.arange(tUse[0],tUse[-1]+1)
    else:
        tInterp=tUse
    vInterp=fInterp(tInterp)


    tDateUse4Plot=data.iloc[-daysEnd-1].Date.replace('/','-')



    if numPred==0 or daysEnd==0:
        tInterp4Fit=tInterp
        vInterp4Fit=vInterp

    else:
        tInterp4Fit=tInterp[:-min(numPred,daysEnd)]
        vInterp4Fit=vInterp[:-min(numPred,daysEnd),:]


    numCols=vUse.shape[1]

    if flagInterplate==1:
        tPred=np.arange(tInterp4Fit[0],tInterp4Fit[-1]+1+numPred)
    else:
        tPred=np.r_[tUse,np.arange(tInterp4Fit[-1]+1,tInterp4Fit[-1]+1+numPred)]

    vPredAll=np.zeros((len(tPred),numCols))



    for iCol in range(numCols):
        xDataPred=vInterp4Fit[:,iCol]
        vPredTmp=DataPredict(xDataPred,numPred=numPred,numSamples=numSamples)
        vPredAll[:,iCol]=vPredTmp


    if numPred==0 or daysEnd==0:
        tDReal=tInterp[1:]
        vDReal=(np.log(vInterp[1:]/vInterp[:-1])).mean(axis=1)
    else:

        numInterp=len(tInterp)
        tDReal=tInterp[1:min(numInterp,numInterp-min(daysEnd,numPred))]
        vDReal=(np.log(vInterp[1:min(numInterp,numInterp-min(daysEnd,numPred))]/vInterp[:min(numInterp,numInterp-min(daysEnd,numPred))-1])).mean(axis=1)


    tReal=tInterp4Fit
    vReal=vInterp4Fit.mean(axis=1)

    tPred=tPred
    vPred=savgol_filter(vPredAll,window,3,axis=0).mean(axis=1)


    tDPred=tPred[1:]
    vDPred=savgol_filter((np.log(vPredAll[1:,:]/vPredAll[:-1,:])),window,3,axis=0).mean(axis=1)



    tCheck=tInterp
    vCheck=vInterp.mean(axis=1)

    tDCheck=tInterp[1:]
    vDCheck=np.log(vInterp[1:]/vInterp[:-1]).mean(axis=1)


    fig=plt.figure('Prediction-%s-%s- Price'%(tDateUse4Plot,symbol),figsize=(18,9))
    ax1 = fig.subplots()
    ax1.set_title('Prediction-%s-%s- Price'%(tDateUse4Plot,symbol))
    ax1.plot(tPred,vPred,'r-o',linewidth=1,markersize=5,label='Price : Prediction')
    ax1.plot(tCheck,vCheck,'g-o',linewidth=1,markersize=4,label='Price : check')
    ax1.plot(tReal,vReal,'b-o',linewidth=0.5,markersize=1,label='Price : Real')

    plt.grid(which='both')
    ax1.legend(loc='best')

    pngPrice=folder+'DataPredictionLong/Prediction-%s-%s- Price.png'%(tDateUse4Plot,symbol)
    pngPriceName='%s-Price-%s.png'%(symbol[0].upper(),tDateUse4Plot)
    plt.savefig(pngPrice)



    fig=plt.figure('Prediction-%s-%s-Delta Price'%(tDateUse4Plot,symbol),figsize=(18,9))
    ax2 = fig.subplots()
    ax2.set_title('Prediction-%s-%s-Delta Price'%(tDateUse4Plot,symbol))

    ax2.plot(tDPred,vDPred,'r-o',linewidth=1,markersize=5,label='delta Price : Prediction')
    ax2.plot(tDCheck,vDCheck,'g-o',linewidth=1,markersize=4,label='delta Price : check')
    ax2.plot(tDReal,vDReal,'b-o',linewidth=0.5,markersize=3,label='delta Price : Real')
    ax2.plot(tDPred,np.zeros_like(tDPred),'k-.',linewidth=1,label='cut')
    plt.grid(which='both')
    ax2.legend(loc='best')

    pngDeltaPrice=folder+'DataPredictionLong/Prediction-%s-%s-Delta PNamerice.png'%(tDateUse4Plot,symbol)
    pngDeltaPriceName='%s-Delta-%s.png'%(symbol[0].upper(),tDateUse4Plot)
    plt.savefig(pngDeltaPrice)

    ##


    dataHist=data.loc[data.shape[0]-daysFrom:data.shape[0]-daysEnd,['Open','High','Low','Adj Close']]
    dataHist[dataHist<1]=np.exp(dataHist[dataHist<1])
    numStd=6
    openClose=np.log(dataHist['Adj Close']/dataHist.Open+1e-6)
    openCloseStd=openClose.std()
    openClose[openClose>openCloseStd*numStd]=openCloseStd*numStd
    openClose[openClose<-openCloseStd*numStd]=-openCloseStd*numStd
    openCloseLimX=max(-openClose.min(),openClose.max())
    openCloseLess=openClose[openClose<0].sum()
    openCloseLarger=openClose[openClose>0].sum()
    openCloseLess_Large=-openCloseLess/openCloseLarger

    openHigh=np.log(dataHist['High']/dataHist.Open+1e-6)
    openHighStd=openHigh.std()
    openHigh[openHigh>openHighStd*numStd]=openHighStd*numStd
    openHigh[openHigh<-openHighStd*numStd]=-openHighStd*numStd
    openHighLimX=max(-openHigh.min(),openHigh.max())

    openLow=np.log(dataHist['Low']/dataHist.Open+1e-6)
    openLowStd=openLow.std()
    openLow[openLow>openLowStd*numStd]=openLowStd*numStd
    openLow[openLow<-openLowStd*numStd]=-openLowStd*numStd
    openLowLimX=max(-openLow.min(),openLow.max())


    xLim=min(openCloseLimX,openHighLimX,openLowLimX)


    fig=plt.figure('Hist of  %s as of %s'%(symbol,tDateUse4Plot),figsize=(18,9))

    plt.subplot(211)
    plt.hist(openClose,bins=30,density=1,log=True,label='Close/Open')

    plt.xlim((-xLim,xLim))
    plt.title('Close/Open')
    plt.grid(which='both')
    plt.legend(loc='best')
    plt.subplot(212)
    plt.hist(openHigh,bins=30,density=1,log=True,label='High/Open')
    plt.hist(openLow,bins=30,density=1,log=True,label='Low/Open')
    plt.xlim((-xLim,xLim))
    plt.title('Low/Open  VS  High/Open')
    plt.grid(which='both')
    plt.legend(loc='best')
    plt.suptitle('Hist of %s using data as of %s - Less : Larger= %.3f'%(symbol,tDateUse4Plot,openCloseLess_Large))

    pngHist=folder+'DataPredictionLong/Hist of  %s as of %s.png'%(symbol,tDateUse4Plot)
    pngHistName='%s-Hist-%s.png'%(symbol[0].upper(),tDateUse4Plot)
    plt.savefig(pngHist)

    plt.close('all')


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

        ch.sendMsg(' : '.join([symbol, strNow]))
        try:
            ch.sendFile(open(pngHist, "rb"), pngHistName)
            ch.sendFile(open(pngPrice, "rb"), pngPriceName)
            ch.sendFile(open(pngDeltaPrice, "rb"), pngDeltaPriceName)
        except:
            ch.sendMsg(symbol+'  :  Upload failed')

        ch.sendMsg(symbol+' : Less/Larger=%.3f'%openCloseLess_Large)


    except:
        print(symbol+'Failed')


update=1

if os.getcwd()==os.environ['HOME']:
    folder=os.getcwd()+'/Qian/'
else:
    folder=os.path.dirname(os.getcwd())+'/'

os.makedirs(folder,exist_ok=True)


flagInterplate=0
cols=['Open','Adj Close']
for symbol in ['gold','silver','wti','brent']:



    DataGet(update,symbol=symbol)


    DataProcess(symbol=symbol,window=7,daysFrom=120,daysEnd=0,numSamples=10,numPred=3,columns=cols,flagInterplate=flagInterplate)





'''
# crontab　{-l | -e|-r}
# -l  　显示当前的crontab
# -r　　删除当前的crontab
# -e　　使用编辑器编辑当前的crontab文件
# m h  dom mon dow   command
2 9 * * * /home/i/NewLife/LongPrediction20200418.py



'''



#
