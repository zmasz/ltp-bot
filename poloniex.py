import requests, json
import datetime

#argument type must be tuple; (m,d,y)
def toUnixTime(date):
	epoch = datetime.date(1970,1,1)
	date = datetime.date(date[2],date[0],date[1])

	return int((date-epoch).total_seconds())


#Public API methods for Poloniex data
	#All methods use the list type arguments for currencies(pairs)
#TODO: implement Trading API methods

class Poloniex:


	def getTicker(self,currencyPairs):
		r = requests.get("https://poloniex.com/public?command=returnTicker")
		ticker = json.loads(r.text)

		return {pair: ticker[pair] for pair in ticker if pair in currencyPairs}

	def get24hVolume(self,currencyPairs):
		r = requests.get("https://poloniex.com/public?command=return24hVolume")
		volumes = json.loads(r.text)

		return {pair: volumes[pair] for pair in volumes if pair in currencyPairs}

	def getOrderBook(self,currencyPairs,depth):
		orderBook = {}
		for pair in currencyPairs:
			r = requests.get("https://poloniex.com/public?command=returnOrderBook&currencyPair="
				+ pair + "&depth=" + str(depth))
			orderBook[pair] = json.loads(r.text)

		return orderBook

	#Start and End dates are tuples;(m,d,y)
	def getTradeHistory(self,currencyPairs,start,end):
		tradeHistory = {}
		for pair in currencyPairs:
			r = requests.get("https://poloniex.com/public?command=returnTradeHistory&currencyPair="
				+ pair + "&start=" + str(toUnixTime(start)) + "&end=" + str(toUnixTime(end)))
			tradeHistory[pair] = json.loads(r.text)

		return tradeHistory

	def getLoanOrders(self,currencies):
		loanOrders = {}
		for currency in currencies:
			r = requests.get("https://poloniex.com/public?command=returnLoanOrders&currency=" +
				currency)
			loanOrders[currency] = json.loads(r.text)

		return loanOrders







bot = Poloniex()
#print(bot.getTicker(["BTC_XMR","BTC_ETH"]))
#print(bot.getOrderBook(["BTC_XMR","BTC_ETH","BTC_LTC"],5))
#bot.getTradeHistory(["BTC_XMR"],(7,14,2013),(7,14,2014))
print(bot.getLoanOrders(["XMR"]))

