from poloniex import Poloniex
import pandas as pd
import datetime as dt
import numpy as np

toDateTime = np.vectorize(dt.datetime.fromtimestamp)

unitSeconds = {'m':60, 'h':3600, 'd':86400, 'w':604800, 'M':2678400, 'y':32140800}

def getSeconds(timeUnit):
	seconds = unitSeconds[timeUnit]

	return seconds


class Data(Poloniex):
	
	
	def saveChartData(self,pair):
		start = dt.datetime(2008,1,1)
		end = dt.datetime.utcnow()
		Poloniex.getChartData(self,pair,start,end,300).to_csv('chartData'+pair+".csv")

	#Valid Arguments ('XXX/OOO',int,['m','h','d','w','M','y'])
	def readChartData(self,pair,interval,unit):

		chartDataOrig = pd.read_csv('chartData'+pair+".csv")

		chartDataNew = {'date':[], 'open':[], 'close':[], 'high':[], 'low':[]}

		datelist = []
		openp = []
		closep = []
		highp = []
		lowp = []


		first = [0,chartDataOrig['date'][0]]
		for i,date in enumerate(chartDataOrig['date']):

			if date >= first[1] + (interval*getSeconds(unit)):

				chartDataNew['date'].append(toDateTime(first[1]))
				chartDataNew['open'].append(chartDataOrig['open'][first[0]])
				chartDataNew['close'].append(chartDataOrig['close'][i])
				chartDataNew['high'].append(chartDataOrig['high'][first[0]:i].max())
				chartDataNew['low'].append(chartDataOrig['low'][first[0]:i].min())

				first = [i,chartDataOrig['date'][i]]

		return pd.DataFrame.from_dict(chartDataNew,orient='columns')



