import requests, json
import datetime as dt
import numpy as np
import pandas as pd



toDateTime = np.vectorize(dt.datetime.fromtimestamp)
toUnixTime = np.vectorize(dt.datetime.timestamp)




#Public API methods for Poloniex data
#TODO: implement Trading API methods

class Poloniex:


	def getTicker(self,currencyPair):
		r = requests.get("https://poloniex.com/public?command=returnTicker")
		ticker = json.loads(r.text)[currencyPair]
		
		return pd.DataFrame.from_dict(ticker,orient='index')

	def get24hVolume(self,currencyPair):
		r = requests.get("https://poloniex.com/public?command=return24hVolume")
		volumes = json.loads(r.text)[currencyPair]
		
		return pd.DataFrame.from_dict(volumes,orient='index')

	def getOrderBook(self,currencyPair,depth):


		r = requests.get("https://poloniex.com/public?command=returnOrderBook&currencyPair="
			+ currencyPair + "&depth=" + str(depth))
		orderBook = json.loads(r.text)

		return pd.DataFrame.from_dict(orderBook,orient='columns')

	#Start and End dates are tuples;(y,m,d)
	def getTradeHistory(self,currencyPair,start,end):
		start = int(toUnixTime(dt.datetime(start[0],start[1],start[2])))
		end = int(toUnixTime(dt.datetime(end[0],end[1],end[2])))
		tradeHistory = {}
		r = requests.get("https://poloniex.com/public?command=returnTradeHistory&currencyPair="
			+ currencyPair + "&start=" + str(start) + "&end=" + str(end))
		tradeHistory = json.loads(r.text)

		return pd.DataFrame.from_dict(tradeHistory,orient='columns')

	#valid period times: 300(5m), 900(15m), 1800(30m), 7200(2h), 14400(4h), 86400(1d)
	def getChartData(self,currencyPair,start,end,period):
		start = int(toUnixTime(dt.datetime(start[0],start[1],start[2])))
		end = int(toUnixTime(dt.datetime(end[0],end[1],end[2])))
		chartData = {}
		r = requests.get("https://poloniex.com/public?command=returnChartData&currencyPair=" 
			+ currencyPair + "&start=" + str(start) + "&end=" + str(end)
			+ "&period=" + str(period))
		chartData = pd.DataFrame.from_dict(json.loads(r.text),orient='columns')
		chartData['date'] = chartData['date'].apply(toDateTime)

		return chartData

	def getLoanOrders(self,currency):
		loanOrders = {}
		r = requests.get("https://poloniex.com/public?command=returnLoanOrders&currency=" +
			currency)
		loanOrders = json.loads(r.text)['offers']

		return pd.DataFrame.from_dict(loanOrders,orient='columns')







tester = Poloniex()
#print(tester.getTicker("BTC_XMR"))
#print(tester.get24hVolume("BTC_XMR"))
#print(tester.getOrderBook("BTC_XMR",5))
#print(tester.getTradeHistory("BTC_XMR",(2014,7,14),(2014,8,14)))
#print(tester.getLoanOrders("XMR"))
print(tester.getChartData("BTC_XMR",(2014,7,14),(2014,7,15),300))

