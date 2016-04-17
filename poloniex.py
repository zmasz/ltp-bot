import requests, json
import datetime as dt
import numpy as np
import pandas as pd



toDateTime = np.vectorize(dt.datetime.fromtimestamp)
toUnixTime = np.vectorize(dt.datetime.timestamp)




#TODO: implement Trading API methods

class Poloniex:

	#Public API methods for Poloniex data

	def getTicker(self,currencyPair):
		r = requests.get("https://poloniex.com/public?command=returnTicker")
		ticker = json.loads(r.text)[currencyPair]



		return pd.Series(list(ticker.values()),index=ticker.keys(),dtype=float)

	def get24hVolume(self,currencyPair):
		r = requests.get("https://poloniex.com/public?command=return24hVolume")
		volumes = json.loads(r.text)[currencyPair]

		return volumes
		#return pd.Series(list(volumes.values()),index=volumes.keys(),dtype=float)

	def getOrderBook(self,currencyPair,depth):

		r = requests.get("https://poloniex.com/public?command=returnOrderBook&currencyPair="
			+ currencyPair + "&depth=" + str(depth))
		orderBook = json.loads(r.text)

		return pd.DataFrame.from_dict(orderBook,orient='columns')

	#Start and End dates are datetime objects
	def getTradeHistory(self,currencyPair,start,end):
		start = dt.datetime(start[0],start[1],start[2])
		end = dt.datetime(end[0],end[1],end[2])
		start = int(toUnixTime(start))
		end = int(toUnixTime(end))
		tradeHistory = {}
		r = requests.get("https://poloniex.com/public?command=returnTradeHistory&currencyPair="
			+ currencyPair + "&start=" + str(start) + "&end=" + str(end))
		tradeHistory = json.loads(r.text)

		return pd.DataFrame.from_dict(tradeHistory,orient='columns')

	#valid period times: 300(5m), 900(15m), 1800(30m), 7200(2h), 14400(4h), 86400(1d)
	def getChartData(self,currencyPair,start,end,period):
		start = int(toUnixTime(start))
		end = int(toUnixTime(end))
		r = requests.get("https://poloniex.com/public?command=returnChartData&currencyPair=" 
			+ currencyPair + "&start=" + str(start) + "&end=" + str(end)
			+ "&period=" + str(period))

		chartData = json.loads(r.text)
	
		chartData = pd.DataFrame.from_dict(chartData,orient='columns',dtype=np.float64)
		chartData['date'] = pd.to_datetime(chartData['date'],unit='s')
		chartData = chartData.set_index('date')
		chartData = chartData.drop('weightedAverage',1)
		chartData = chartData.drop('quoteVolume',1)


		return chartData


	def getLoanOrders(self,currency):
		loanOrders = {}
		r = requests.get("https://poloniex.com/public?command=returnLoanOrders&currency=" +
			currency)
		loanOrders = json.loads(r.text)['offers']

		return pd.DataFrame.from_dict(loanOrders,orient='columns')

	#Custom Poloniex API methods

	def getPrice(self,currencyPair):
		tickerData = Poloniex.getTicker(self,currencyPair)
	
		return tickerData['last']


