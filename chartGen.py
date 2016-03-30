import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
from matplotlib import style
import pandas as pd
import numpy as np
from poloniex import Poloniex

style.use('ggplot')


def graph_chart(currencyPair):


	grapher = Poloniex()
	chartData = grapher.getChartData(currencyPair,(2015,1,1),(2016,3,29),86400)

	fig = plt.figure()
	ax = plt.subplot(111)

	date = chartData['date'].apply(mdates.date2num)
	closep = chartData['close']
	volume = chartData['volume']
	highp = chartData['high']
	lowp = chartData['low']
	openp = chartData['open']

	x = 0
	y = len(date)
	ohlc = []

	while x < y:
		append_me = date[x],openp[x],highp[x],lowp[x],closep[x],volume[x]
		ohlc.append(append_me)
		x+=1

	candlestick_ohlc(ax,ohlc, width=.6,colorup='g',colordown='r')

	for label in ax.xaxis.get_ticklabels():
		label.set_rotation(45)

	ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

	plt.xlabel('Date')
	plt.ylabel('Price (BTC)')
	plt.title(currencyPair)

	#plt.legend()
	plt.show()


graph_chart("BTC_XMR")