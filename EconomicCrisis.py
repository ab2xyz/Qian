import os
import datetime

import pandas as pd
from pandas_datareader import data, wb
import quandl

import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from tqdm import tqdm


def Interplate(dataPD):

    tNow=datetime.datetime.now()

    t=np.array([(datetime.datetime.strptime(x,'%Y-%m-%d')-tNow).days if '-' in x else (datetime.datetime.strptime(x,'%Y/%m/%d')-tNow).days for x in dataPD.Date])
    cols=dataPD.columns.to_list()

    tNew=np.arange(t[0],1)
    tNewDate=np.array([(tNow+ datetime.timedelta(int(iT))).strftime('%Y-%m-%d') for iT in tNew])

    dataPDNew=pd.DataFrame(columns=cols)
    dataPDNew['Date']=tNewDate

    cols.remove('Date')

    for iCol in range(len(cols)):
        f = interp1d(t, dataPD[cols[iCol]], kind='cubic', fill_value="extrapolate")
        yNew=f(tNew)

        dataPDNew[cols[iCol]]=yNew

    return dataPDNew



def QuandlGet():
    os.makedirs('Qian/Finance/dataQuandl',exist_ok=True)

    print('Qian/Finance/dataQuandlOilWTI.csv')
    if not os.path.exists('Qian/Finance/dataQuandl/dataQuandlOilWTI.csv'):
        dataOilWTI = quandl.get("EIA/PET_RWTC_D", collapse="daily")  #    WTI
        dataOilWTI.to_csv('Qian/Finance/dataQuandl/dataQuandlOilWTI.csv')


    print('Qian/Finance/dataQuandlOilBrent.csv')
    if not os.path.exists('Qian/Finance/dataQuandl/dataQuandlOilBrent.csv'):
        dataOilBrent = quandl.get("EIA/PET_RBRTE_D", collapse="daily")  #    Brent
        dataOilBrent.to_csv('Qian/Finance/dataQuandl/dataQuandlOilBrent.csv')


    print('Qian/Finance/dataQuandlUSDIndex.csv')
    if not os.path.exists('Qian/Finance/dataQuandl/dataQuandlUSDIndex.csv'):
        dataUSDIndex = quandl.get("CHRIS/ICE_DX1", collapse="daily")  #    USD index
        dataUSDIndex.to_csv('Qian/Finance/dataQuandl/dataQuandlUSDIndex.csv')

    print('Qian/Finance/dataQuandlGold.csv')
    if not os.path.exists('Qian/Finance/dataQuandl/dataQuandlGold.csv'):
        dataGold = quandl.get("LBMA/GOLD", collapse="daily")  #    Gold
        dataGold.to_csv('Qian/Finance/dataQuandl/dataQuandlGold.csv')

    print('Qian/Finance/dataQuandlSilver.csv')
    if not os.path.exists('Qian/Finance/dataQuandl/dataQuandlSilver.csv'):
        dataSilver=quandl.get("LBMA/SILVER", collapse="daily")  #    Silver
        dataSilver.to_csv('Qian/Finance/dataQuandl/dataQuandlSilver.csv')

    print('Qian/Finance/dataQuandlCPIUSA.csv')
    if not os.path.exists('Qian/Finance/dataQuandl/dataQuandlCPIUSA.csv'):
        dataCPIUSA=quandl.get("RATEINF/CPI_USA", collapse="daily")  #    CPI-SUA
        dataCPIUSA.to_csv('Qian/Finance/dataQuandl/dataQuandlCPIUSA.csv')

    print('Qian/Finance/dataQuandlMiseryUS.csv')
    if not os.path.exists('Qian/Finance/dataQuandl/dataQuandlMiseryUS.csv'):
        dataMiseryUS=quandl.get("USMISERY/INDEX", collapse="daily")  #    MiseryUS   苦难指数
        dataMiseryUS.to_csv('Qian/Finance/dataQuandl/dataQuandlMiseryUS.csv')

    return True




def QuandlProcess():
    os.makedirs('Qian/Finance/dataQuandl4Merge',exist_ok=True)

    ## WTI
    dataOilWTI=pd.read_csv('Qian/Finance/dataQuandl/dataQuandlOilWTI.csv')
    dataOilWTIDate=dataOilWTI.Date.values
    for idxData in range(len(dataOilWTIDate)):
        if '-' in dataOilWTIDate[idxData]:
            dataOilWTIDate[idxData]=dataOilWTIDate[idxData].replace('/','-')
    dataOilWTI['Date']=dataOilWTIDate
    dataOilWTI.to_csv('Qian/Finance/dataQuandl4Merge/dataQuandlOilWTI.csv',index=False)

    ## Brent
    dataOilBrent=pd.read_csv('Qian/Finance/dataQuandl/dataQuandlOilBrent.csv')
    dataOilBrentDate=dataOilBrent.Date.values
    for idxData in range(len(dataOilBrentDate)):
        if '-' in dataOilBrentDate[idxData]:
            dataOilBrentDate[idxData]=dataOilBrentDate[idxData].replace('/','-')
    dataOilBrent['Date']=dataOilBrentDate
    dataOilBrent.to_csv('Qian/Finance/dataQuandl4Merge/dataQuandlOilBrent.csv',index=False)

    ## USD Index

    dataUSDIndex=pd.read_csv('Qian/Finance/dataQuandl/dataQuandlUSDIndex.csv')
    dataUSDIndexDate=dataUSDIndex.Date.values
    for idxData in range(len(dataUSDIndexDate)):
        if '-' in dataUSDIndexDate[idxData]:
            dataUSDIndexDate[idxData]=dataUSDIndexDate[idxData].replace('/','-')
    dataUSDIndex['Date']=dataUSDIndexDate
    dataUSDIndex['Value']=dataUSDIndex['Settle']
    dataUSDIndex[['Date','Value']].to_csv('Qian/Finance/dataQuandl4Merge/dataQuandlUSDIndex.csv',index=False)


    ## Gold
    dataGold=pd.read_csv('Qian/Finance/dataQuandl/dataQuandlGold.csv')
    dataGoldDate=dataGold.Date.values
    for idxData in range(len(dataGoldDate)):
        if '-' in dataGoldDate[idxData]:
            dataGoldDate[idxData]=dataGoldDate[idxData].replace('/','-')
    dataGold['Date']=dataGoldDate

    dataGold['Value']=dataGold['USD (PM)']

    dataGold.loc[dataGold['USD (PM)'].isna(),'Value']=dataGold.loc[dataGold['USD (PM)'].isna(),'USD (AM)']
    dataGold[['Date','Value']].to_csv('Qian/Finance/dataQuandl4Merge/dataQuandlGold.csv',index=False)



    # Silver
    dataSilver=pd.read_csv('Qian/Finance/dataQuandl/dataQuandlSilver.csv')
    dataSilverDate=dataSilver.Date.values
    for idxData in range(len(dataSilverDate)):
        if '-' in dataSilverDate[idxData]:
            dataSilverDate[idxData]=dataSilverDate[idxData].replace('/','-')
    dataSilver['Date']=dataSilverDate

    dataSilver['Value']=dataSilver['USD']
    dataSilver[['Date','Value']].to_csv('Qian/Finance/dataQuandl4Merge/dataQuandlSilver.csv',index=False)


    ##  CPI-USA
    try:     # Update
        print('Qian/Finance/dataQuandlCPIUSA.csv')
        dataCPIUSA=quandl.get("RATEINF/CPI_USA", collapse="daily")  #    CPI-SUA
        dataCPIUSA.to_csv('Qian/Finance/dataQuandl/dataQuandlCPIUSA.csv')
    except:
        pass

    dataCPIUSA=pd.read_csv('Qian/Finance/dataQuandl/dataQuandlCPIUSA.csv')
    dataCPIUSADate=dataCPIUSA.Date.values
    for idxData in range(len(dataCPIUSADate)):
        if '-' in dataCPIUSADate[idxData]:
            dataCPIUSADate[idxData]=dataCPIUSADate[idxData].replace('/','-')
    dataCPIUSA['Date']=dataCPIUSADate

    dataCPIUSA=Interplate(dataCPIUSA)

    dataCPIUSA.to_csv('Qian/Finance/dataQuandl4Merge/dataQuandlCPIUSA.csv',index=False)


    ## MiseryUS   苦难指数
    try:     # Update
        print('Qian/Finance/dataQuandlMiseryUS.csv')
        dataMiseryUS=quandl.get("USMISERY/INDEX", collapse="daily")  #    MiseryUS   苦难指数
        dataMiseryUS.to_csv('Qian/Finance/dataQuandl/dataQuandlMiseryUS.csv')
    except:
        pass

    dataMiseryUS=pd.read_csv('Qian/Finance/dataQuandl/dataQuandlMiseryUS.csv')
    dataMiseryUSDate=dataMiseryUS.Date.values
    for idxData in range(len(dataMiseryUSDate)):
        if '-' in dataMiseryUSDate[idxData]:
            dataMiseryUSDate[idxData]=dataMiseryUSDate[idxData].replace('/','-')
    dataMiseryUS['Date']=dataMiseryUSDate

    dataMiseryUS=Interplate(dataMiseryUS)

    dataMiseryUS.to_csv('Qian/Finance/dataQuandl4Merge/dataQuandlMiseryUS.csv',index=False)



###

def YahooGet():
    os.makedirs('Qian/Finance/dataYahoo',exist_ok=True)

    # SPX   : Standard Pool Index  1927-12-30
    if not os.path.exists('Qian/Finance/dataYahoo/dataYahooSPX.csv'):
        dataYahooSPX =  data.DataReader(name = '^GSPC',data_source = 'yahoo', start='1900-01-01')    # SPX  : Standard Pool Index  1927-12-30
        dataYahooSPX.to_csv('Qian/Finance/dataYahoo/dataYahooSPX.csv')

    # Brent     2020-01-03
    if not os.path.exists('Qian/Finance/dataYahoo/dataYahooOilBrent.csv'):
        dataYahooBrent =  data.DataReader(name = 'BZ=F',data_source = 'yahoo', start='1900-01-01')  # Brent     2020-01-03
        dataYahooBrent.to_csv('Qian/Finance/dataYahoo/dataYahooOilBrent.csv')

    # WTI    2000-03-02
    if not os.path.exists('Qian/Finance/dataYahoo/dataYahooOilWTI.csv'):
        dataYahooWTI =  data.DataReader(name = 'CL=F',data_source = 'yahoo', start='1900-01-01')  # WTI    2000-03-02
        dataYahooWTI.to_csv('Qian/Finance/dataYahoo/dataYahooOilWTI.csv')

    # USD index    1971-01-04
    if not os.path.exists('Qian/Finance/dataYahoo/dataYahooUSDIndex.csv'):
        dataYahooUSD =  data.DataReader(name = 'DX-Y.NYB',data_source = 'yahoo', start='1900-01-01')  # USD index    1971-01-04
        dataYahooUSD.to_csv('Qian/Finance/dataYahoo/dataYahooUSDIndex.csv')

    # Gold    2000-02-28
    if not os.path.exists('Qian/Finance/dataYahoo/dataYahooGold.csv'):
        dataYahooGold =  data.DataReader(name = 'GC=F',data_source = 'yahoo', start='1900-01-01')  # Gold    2000-02-28
        dataYahooGold.to_csv('Qian/Finance/dataYahoo/dataYahooGold.csv')

    # Silver    2000-02-28
    if not os.path.exists('Qian/Finance/dataYahoo/dataYahooSilver.csv'):
        dataYahooSilver =  data.DataReader(name = 'SI=F',data_source = 'yahoo', start='1900-01-01')  # Silver    2000-02-28
        dataYahooSilver.to_csv('Qian/Finance/dataYahoo/dataYahooSilver.csv')



def YahooProcess():
    os.makedirs('Qian/Finance/dataYahoo4Merge',exist_ok=True)

    # SPX
    dataSPX=pd.read_csv('Qian/Finance/dataYahoo/dataYahooSPX.csv')
    dataSPXDate=dataSPX.Date.values
    for idxData in range(len(dataSPXDate)):
        if '-' in dataSPXDate[idxData]:
            dataSPXDate[idxData]=dataSPXDate[idxData].replace('/','-')
    dataSPX['Date']=dataSPXDate

    dataSPX['Value']=dataSPX['Adj Close']
    dataSPX[['Date','Value']].to_csv('Qian/Finance/dataYahoo4Merge/dataYahooSPX.csv',index=False)


    # Brent
    dataOilBrent=pd.read_csv('Qian/Finance/dataYahoo/dataYahooOilBrent.csv')
    dataOilBrentDate=dataOilBrent.Date.values
    for idxData in range(len(dataOilBrentDate)):
        if '-' in dataOilBrentDate[idxData]:
            dataOilBrentDate[idxData]=dataOilBrentDate[idxData].replace('/','-')
    dataOilBrent['Date']=dataOilBrentDate

    dataOilBrent['Value']=dataOilBrent['Adj Close']
    dataOilBrent[['Date','Value']].to_csv('Qian/Finance/dataYahoo4Merge/dataYahooOilBrent.csv',index=False)


    # WTI
    dataOilWTI=pd.read_csv('Qian/Finance/dataYahoo/dataYahooOilWTI.csv')
    dataOilWTIDate=dataOilWTI.Date.values
    for idxData in range(len(dataOilWTIDate)):
        if '-' in dataOilWTIDate[idxData]:
            dataOilWTIDate[idxData]=dataOilWTIDate[idxData].replace('/','-')
    dataOilWTI['Date']=dataOilWTIDate

    dataOilWTI['Value']=dataOilWTI['Adj Close']
    dataOilWTI[['Date','Value']].to_csv('Qian/Finance/dataYahoo4Merge/dataYahooOilWTI.csv',index=False)


    # USD index
    dataUSDIndex=pd.read_csv('Qian/Finance/dataYahoo/dataYahooUSDIndex.csv')
    dataUSDIndexDate=dataUSDIndex.Date.values
    for idxData in range(len(dataUSDIndexDate)):
        if '-' in dataUSDIndexDate[idxData]:
            dataUSDIndexDate[idxData]=dataUSDIndexDate[idxData].replace('/','-')
    dataUSDIndex['Date']=dataUSDIndexDate

    dataUSDIndex['Value']=dataUSDIndex['Adj Close']
    dataUSDIndex[['Date','Value']].to_csv('Qian/Finance/dataYahoo4Merge/dataYahooUSDIndex.csv',index=False)

    # Gold
    dataGold=pd.read_csv('Qian/Finance/dataYahoo/dataYahooGold.csv')
    dataGoldDate=dataGold.Date.values
    for idxData in range(len(dataGoldDate)):
        if '-' in dataGoldDate[idxData]:
            dataGoldDate[idxData]=dataGoldDate[idxData].replace('/','-')
    dataGold['Date']=dataGoldDate

    dataGold['Value']=dataGold['Adj Close']
    dataGold[['Date','Value']].to_csv('Qian/Finance/dataYahoo4Merge/dataYahooGold.csv',index=False)


    # Silver
    dataSilver=pd.read_csv('Qian/Finance/dataYahoo/dataYahooSilver.csv')
    dataSilverDate=dataSilver.Date.values
    for idxData in range(len(dataSilverDate)):
        if '-' in dataSilverDate[idxData]:
            dataSilverDate[idxData]=dataSilverDate[idxData].replace('/','-')
    dataSilver['Date']=dataSilverDate

    dataSilver['Value']=dataSilver['Adj Close']
    dataSilver[['Date','Value']].to_csv('Qian/Finance/dataYahoo4Merge/dataYahooSilver.csv',index=False)


def Merge(aPd,bPd):
    tBStart=bPd.loc[0,'Date'].replace('/','-')
    tBStartDate=datetime.datetime.strptime(tBStart,'%Y-%m-%d')

    tA=np.array([(datetime.datetime.strptime(x,'%Y-%m-%d')-tBStartDate).days if '-' in x else (datetime.datetime.strptime(x,'%Y/%m/%d')-tBStartDate).days for x in aPd.Date])

    aPdUse=aPd.loc[tA<0,:]

    cPd=pd.concat((aPdUse,bPd))

    return cPd


def DataMerge():
    os.makedirs('Qian/Finance/data',exist_ok=True)

    ## CPI
    dataCPIUSA=pd.read_csv('Qian/Finance/dataQuandl4Merge/dataQuandlCPIUSA.csv')
    dataCPIUSA.rename(columns={'Value':'cpi'},inplace=True)
    dataCPIUSA.to_csv('Qian/Finance/data/dataCPIUSA.csv',index=False)

    ## Misery
    dataMiseryUS=pd.read_csv('Qian/Finance/dataQuandl4Merge/dataQuandlMiseryUS.csv')
    dataMiseryUS.rename(columns={'Unemployment Rate':'unemployment','Inflation Rate':'inflation','Misery Index':'misery'},inplace=True)
    dataMiseryUS[['Date','misery']].to_csv('Qian/Finance/data/dataMiseryUS.csv',index=False)
    dataMiseryUS[['Date','inflation']].to_csv('Qian/Finance/data/dataInflationUS.csv',index=False)
    dataMiseryUS[['Date','unemployment']].to_csv('Qian/Finance/data/dataUnemploymentUS.csv',index=False)

    ## SPX
    dataSPX=pd.read_csv('Qian/Finance/dataYahoo4Merge/dataYahooSPX.csv')
    dataSPX.rename(columns={'Value':'spx'},inplace=True)
    dataSPX.to_csv('Qian/Finance/data/dataSPX.csv',index=False)

    ## USD index
    dataUSDIndexQuandl=pd.read_csv('Qian/Finance/dataQuandl4Merge/dataQuandlUSDIndex.csv')
    dataUSDIndexYahoo=pd.read_csv('Qian/Finance/dataYahoo4Merge/dataYahooUSDIndex.csv')
    dataUSDIndex=Merge(dataUSDIndexQuandl,dataUSDIndexYahoo)
    dataUSDIndex.rename(columns={'Value':'usd'},inplace=True)
    dataUSDIndex.to_csv('Qian/Finance/data/dataUSDIndex.csv',index=False)

    # ## Gold
    dataGoldQuandl=pd.read_csv('Qian/Finance/dataQuandl4Merge/dataQuandlGold.csv')
    dataGoldYahoo=pd.read_csv('Qian/Finance/dataYahoo4Merge/dataYahooGold.csv')
    dataGold=Merge(dataGoldQuandl,dataGoldYahoo)
    dataGold.rename(columns={'Value':'gold'},inplace=True)
    dataGold.to_csv('Qian/Finance/data/dataGold.csv',index=False)


    ## Silver
    dataSilverQuandl=pd.read_csv('Qian/Finance/dataQuandl4Merge/dataQuandlSilver.csv')
    dataSilverYahoo=pd.read_csv('Qian/Finance/dataYahoo4Merge/dataYahooSilver.csv')
    dataSilver=Merge(dataSilverQuandl,dataSilverYahoo)
    dataSilver.rename(columns={'Value':'silver'},inplace=True)
    dataSilver.to_csv('Qian/Finance/data/dataSilver.csv',index=False)

    ## OilBrent
    dataOilBrentQuandl=pd.read_csv('Qian/Finance/dataQuandl4Merge/dataQuandlOilBrent.csv')
    dataOilBrentYahoo=pd.read_csv('Qian/Finance/dataYahoo4Merge/dataYahooOilBrent.csv')
    dataOilBrent=Merge(dataOilBrentQuandl,dataOilBrentYahoo)
    dataOilBrent.rename(columns={'Value':'brent'},inplace=True)
    dataOilBrent.to_csv('Qian/Finance/data/dataOilBrent.csv',index=False)


    ## OilWTI
    dataOilWTIQuandl=pd.read_csv('Qian/Finance/dataQuandl4Merge/dataQuandlOilWTI.csv')
    dataOilWTIYahoo=pd.read_csv('Qian/Finance/dataYahoo4Merge/dataYahooOilWTI.csv')
    dataOilWTI=Merge(dataOilWTIQuandl,dataOilWTIYahoo)
    dataOilWTI.rename(columns={'Value':'wti'},inplace=True)
    dataOilWTI.to_csv('Qian/Finance/data/dataOilWTI.csv',index=False)


def MergeAll(symbols=[]):
    csvList=symbols.copy()
    if csvList ==[]:
        csvList=[x for x in os.listdir('Qian/Finance/data') if (x[-4:]=='.csv' and x!='data.csv')]
    else:
        for idxCSV in range(len(csvList)):
            if csvList[idxCSV]=='cpi':
                csvList[idxCSV]='dataCPIUSA.csv'

            if csvList[idxCSV]=='gold':
                csvList[idxCSV]='dataGold.csv'

            if csvList[idxCSV]=='misery':
                csvList[idxCSV]='dataMiseryUS.csv'

            if csvList[idxCSV]=='brent':
                csvList[idxCSV]='dataOilBrent.csv'

            if csvList[idxCSV]=='wti':
                csvList[idxCSV]='dataOilWTI.csv'

            if csvList[idxCSV]=='silver':
                csvList[idxCSV]='dataSilver.csv'

            if csvList[idxCSV]=='spx':
                csvList[idxCSV]='dataSPX.csv'

            if csvList[idxCSV]=='usd':
                csvList[idxCSV]='dataUSDIndex.csv'

            if csvList[idxCSV]=='inflation':
                csvList[idxCSV]='dataInflationUS.csv'

            if csvList[idxCSV]=='unemployment':
                csvList[idxCSV]='dataUnemploymentUS.csv'


    for iCSV in csvList:

        iData=pd.read_csv('Qian/Finance/data/'+iCSV)
        if 'data' not in locals():
            data=iData
            data=iData
        else:
            data=pd.merge(left=data,right=iData,how='inner')

    data.rename(columns={'Date':'date'},inplace=True)

    data.to_csv('Qian/Finance/data/data.csv',index=False)

    return data




def PlotDateY(date,y,yLabel='yLabel',title='title',figName='fig',figSize=(10,8),monthDelta=12):

    fig=plt.figure(figName,figsize=figSize)
    ax=fig.subplots()

    ax.get_xaxis().set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.plot(date,y,'r',label=yLabel)
    ax.grid()
    ax.legend(loc='best')
    ax.set_xticks(pd.date_range(date[0],date[-1],freq='%dM'%(monthDelta)))

    plt.title(title)
    fig.autofmt_xdate()

    return fig




def PicSymbol(symbols=['cpi','gold','misery','brent','wti','silver','spx','usd','unemployment','inflation'],window=31,dateStart='1900-01-01',dateEnd=None,monthDelta=12):
    os.makedirs('Qian/Finance/picSymbol',exist_ok=True)

    sym=symbols.copy()

    if dateEnd is None:
         dateEnd=datetime.datetime.today().date()
    else:
        dateEnd=dateEnd.replace('/','-')
        dateEnd=datetime.datetime.strptime(dateEnd, '%Y-%m-%d').date()


    dateStart=dateStart.replace('/','-')
    dateStart=datetime.datetime.strptime(dateStart, '%Y-%m-%d').date()

    dateStart_,dateEnd_=dateStart,dateEnd




    for idxSym in range(len(symbols)):

        iSym=sym[idxSym]

        data=MergeAll([iSym])

        date=data['date'].values


        iY=data[iSym].values


        date=np.array([datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in date])

        iY=iY[date>=dateStart_]
        date=date[date>=dateStart_]


        iY=iY[date<=dateEnd_]
        date=date[date<=dateEnd_]

        if len(date)<window+1:
            continue

        date=date[1:]
        dateStart,dateEnd= date[0],date[-1]


        iY[np.isnan(iY)]=1e-6

        iY[iY==0]=1e-6

        idY=np.log(iY[1:]/iY[:-1])

        iY=iY[1:]

        iData=[iY,idY]

        dataType=['Ori','Log']

        for idxI in [0,1]:

            iI=iData[idxI]

            iI[np.isnan(iI)]=1e-6



            figName=dataType[idxI]+iSym.capitalize()

            title='%s(%s)'%(iSym.capitalize(),dataType[idxI])
            yLabel=dataType[0]+iSym.capitalize()

            if window==0:
                iI=iI
            else:
                iI=savgol_filter(iI,window,3)


            fig=PlotDateY(date,iI,yLabel=yLabel,title=title,figName=figName,figSize=(10,8),monthDelta=monthDelta)


            os.makedirs('Qian/Finance/picSymbol/%d-%s-%s'%(window,dateStart_,dateEnd_),exist_ok=True)
            plt.savefig('Qian/Finance/picSymbol/%d-%s-%s/%s.png'%(window,dateStart_,dateEnd_,figName))
            plt.close(fig)






def PlotDateYY(date,y1,y2,figName='fig',title='title',yLabel=['1','2'],figSize=(15,8),monthDelta=12):
    fig=plt.figure(figName,figsize=figSize)
    ax=fig.subplots()

    ax.get_xaxis().set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.plot(date,y1,'r',label=yLabel[0])
    ax.grid()
    ax.legend(loc='upper left')
    ax.set_xticks(pd.date_range(date[0],date[-1],freq='%dM'%(monthDelta)))

    ax2=ax.twinx()
    ax2.plot(date,y2,'b',label=yLabel[1])
    ax2.grid()
    ax2.legend(loc='upper right')

    plt.title(title)
    fig.autofmt_xdate()

    return fig


def PicSymbolCorr(symbols=['cpi','gold','misery','brent','wti','silver','spx','usd','unemployment','inflation'],window=31,dateStart='1900-01-01',dateEnd=None,monthDelta=12,corrCut=0.6):
    os.makedirs('Qian/Finance/picSymbolCorr',exist_ok=True)

    if dateEnd is None:
         dateEnd=datetime.datetime.today().date()
    else:
        dateEnd=dateEnd.replace('/','-')
        dateEnd=datetime.datetime.strptime(dateEnd, '%Y-%m-%d').date()


    dateStart=dateStart.replace('/','-')
    dateStart=datetime.datetime.strptime(dateStart, '%Y-%m-%d').date()

    dateStart_,dateEnd_=dateStart,dateEnd



    for idxSym in range(len(symbols)):
        for jdxSym in range(idxSym):
            iSym=symbols[idxSym]
            jSym=symbols[jdxSym]

            data=MergeAll([iSym,jSym])

            os.makedirs('Qian/Finance/dataCorr/',exist_ok=True)
            data.to_csv('Qian/Finance/dataCorr/%s-%s.csv'%(iSym,jSym),index=False)


            date=data['date'].values
            iY=data[iSym].values
            jY=data[jSym].values

            date=np.array([datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in date])

            iY=iY[date>=dateStart_]
            jY=jY[date>=dateStart_]
            date=date[date>=dateStart_]


            iY=iY[date<=dateEnd_]
            jY=jY[date<=dateEnd_]
            date=date[date<=dateEnd_]

            if len(date)<window+1:
                continue

            date=date[1:]
            dateStart,dateEnd= date[0],date[-1]


            iY[np.isnan(iY)]=1e-6
            jY[np.isnan(jY)]=1e-6

            iY[iY==0]=1e-6
            jY[jY==0]=1e-6

            idY=np.log(iY[1:]/iY[:-1])
            jdY=np.log(jY[1:]/jY[:-1])

            iY=iY[1:]
            jY=jY[1:]


            iData=[iY,idY]
            jData=[jY,jdY]

            flagData=['Ori','Log']

            for idxI in [0,1]:
                for idxJ in [0,1]:
                    iI=iData[idxI]
                    iJ=jData[idxJ]

                    iI[np.isnan(iI)]=1e-6
                    iJ[np.isnan(iJ)]=1e-6

                    corr=np.corrcoef(iI,iJ)

                    if np.abs(corr[0,1]) < corrCut:
                        continue

                    if np.isnan(corr[0,1]):
                        continue


                    dataType=[flagData[idxI],flagData[idxJ]]

                    figName='Corr'+dataType[0]+iSym.capitalize()+dataType[1]+jSym.capitalize()

                    title='%s(%s) - %s(%s) : %.3f'%(iSym.capitalize(),dataType[0],jSym.capitalize(),dataType[1],corr[0,1])
                    yLabel=[dataType[0]+iSym.capitalize(),dataType[1]+jSym.capitalize()]

                    if window==0:
                        iI=iI
                        iJ=iJ
                    else:
                        iI=savgol_filter(iI,window,3)
                        iJ=savgol_filter(iJ,window,3)

                    fig=PlotDateYY(date,y1=iI,y2=iJ,figName=figName,title=title,figSize=(15,8),monthDelta=monthDelta,yLabel=yLabel)

                    os.makedirs('Qian/Finance/picSymbolCorr/%d-%s-%s'%(window,dateStart_,dateEnd_),exist_ok=True)
                    plt.savefig('Qian/Finance/picSymbolCorr/%d-%s-%s/%.3f-%s.png'%(window,dateStart_,dateEnd_,np.abs(corr[0,1]),figName))
                    plt.close(fig)


            #

def DateCenter2DateBounday(dateCenter='2008-08-08',monthInterval=30):
    from dateutil.relativedelta import relativedelta
    dateCenter=dateCenter.replace('/','-')
    dateCenter=datetime.datetime.strptime(dateCenter,'%Y-%m-%d')
    dateStart=dateCenter+relativedelta(months=-monthInterval)
    dateEnd=dateCenter+relativedelta(months=monthInterval)

    dateStart=dateStart.strftime('%Y-%m-%d')
    dateEnd=dateEnd.strftime('%Y-%m-%d')

    return dateStart,dateEnd





def DateCenter2DateBounday(dateCenter='2008-08-08',monthInterval=30):
    from dateutil.relativedelta import relativedelta
    dateCenter=dateCenter.replace('/','-')
    dateCenter=datetime.datetime.strptime(dateCenter,'%Y-%m-%d')
    dateStart=dateCenter+relativedelta(months=-monthInterval)
    dateEnd=dateCenter+relativedelta(months=monthInterval)

    dateStart=dateStart.strftime('%Y-%m-%d')
    dateEnd=dateEnd.strftime('%Y-%m-%d')

    return dateStart,dateEnd











##  ##  ##  ##









update=1

os.makedirs('Qian',exist_ok=True)

if update:
    quandl.save_key('w8WdHsCDd6zBPE-G2Pba')

    QuandlGet()
    QuandlProcess()


    YahooGet()
    YahooProcess()



DataMerge()
# MergeAll([])      # ['cpi','gold','misery','brent','wti','silver','spx','usd','unemployment','inflation']




# #  Standard Model for running
# PicSymbol(symbols=['cpi','gold','misery','brent','wti','silver','spx','usd','unemployment','inflation'],window=7,dateStart='2005-01-08',dateEnd='2011-01-08',monthDelta=2)
# PicSymbolCorr(symbols=['cpi','gold','misery','brent','wti','silver','spx','usd','unemployment','inflation'],window=7,dateStart='2005-01-08',dateEnd='2011-01-08',monthDelta=2,corrCut=0.006)





windows=[0,7,21]
symbols=['cpi','gold','misery','brent','wti','silver','spx','usd','unemployment','inflation']
dateCenter=['1921-01-30','1929-01-30','1973-01-30','1987-01-30','1997-01-30','2008-09-30','2020-01-01']
corrCut=0.6




dateStart=[]
dateEnd=[]
for iCenter in dateCenter:
    iStart,iEnd=DateCenter2DateBounday(dateCenter=iCenter,monthInterval=30)
    dateStart.append(iStart)
    dateEnd.append(iEnd)


for idxWindow in tqdm(range(len(windows))):
    for idxDate in tqdm(range(len(dateCenter))):


        iDateStart=dateStart[idxDate]
        iDateEnd=dateEnd[idxDate]
        iWindow=windows[idxWindow]


        PicSymbol(symbols=symbols,window=iWindow,dateStart=iDateStart,dateEnd=iDateEnd,monthDelta=12)

        PicSymbolCorr(symbols=symbols,window=iWindow,dateStart=iDateStart,dateEnd=iDateEnd,monthDelta=12,corrCut=corrCut)



    #
