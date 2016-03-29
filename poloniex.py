import requests, json
import datetime
import pandas as pd

#argument type must be tuple; (m,d,y)
def toUnixTime(date):
	epoch = datetime.date(1970,1,1)
	date = datetime.date(date[2],date[0],date[1])

	return int((date-epoch).total_seconds())


#Public API methods for Poloniex data
	#All methods use the list type arguments for currencies(pairs)
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

	#Start and End dates are tuples;(m,d,y)
	def getTradeHistory(self,currencyPair,start,end):
		tradeHistory = {}
		r = requests.get("https://poloniex.com/public?command=returnTradeHistory&currencyPair="
			+ currencyPair + "&start=" + str(toUnixTime(start)) + "&end=" + str(toUnixTime(end)))
		tradeHistory = json.loads(r.text)

		return pd.DataFrame.from_dict(tradeHistory,orient='columns')

	#valid period times: 300(5m), 900(15m), 1800(30m), 7200(2h), 14400(4h), 86400(1d)
	def getChartData(self,currencyPair,start,end,period):
		chartData = {}
		r = requests.get("https://poloniex.com/public?command=returnChartData&currencyPair=" 
			+ currencyPair + "&start=" + str(toUnixTime(start)) + "&end=" + str(toUnixTime(end))
			+ "&period=" + str(period))
		chartData = json.loads(r.text)

		return pd.DataFrame.from_dict(chartData,orient='columns')

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
#print(tester.getTradeHistory("BTC_XMR",(7,14,2013),(7,14,2014)))
#print(tester.getLoanOrders("XMR"))
#print(tester.getChartData("BTC_XMR",(7,14,2014),(7,15,2014),300))

