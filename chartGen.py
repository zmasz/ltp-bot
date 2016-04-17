import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.ticker import ScalarFormatter
from matplotlib.finance import candlestick_ohlc
from matplotlib.finance import volume_overlay
from matplotlib import style
import pandas as pd
import numpy as np
import datetime as dt
#from scipy.interpolate import UnivariateSpline

from poloniex import Poloniex
from indicators import Indicators




class Charter(Indicators):

	def __init__(self):
		self.fig = plt.figure(facecolor='#07000d')
		self.ax = plt.subplot(111, axisbg='#07000d')
		self.ax.grid(True,color='w')
		self.ax.yaxis.label.set_color("w")
		self.ax.spines['bottom'].set_color("#5998ff")
		self.ax.spines['top'].set_color("#5998ff")
		self.ax.spines['left'].set_color("#5998ff")
		self.ax.spines['right'].set_color("#5998ff")
		self.ax.tick_params(axis='y',colors='w')
		self.ax.tick_params(axis='x',colors='w')

	#The SMA argument should contain a list of SMA to be displayed
	def chartOHLC(self,interval,unit):

		
		chartData = self.readChartData(interval,unit)
		
		#ax = plt.subplot(111)

		dateconv = np.vectorize(dt.datetime.fromtimestamp)

		date = mdates.date2num(dateconv(chartData['date']))
		closep = chartData['close']
		volume = chartData['volume']
		highp = chartData['high']
		lowp = chartData['low']
		openp = chartData['open']


		x=0
		y=len(date)
		OHLC = []

		while x<y:
			applendLine = date[x],openp[x], highp[x], lowp[x],closep[x]
			OHLC.append(applendLine)
			x+=1

 

		candlestick_ohlc(self.ax, OHLC, width=.65, colorup='#00D000', colordown='#FA0000')

		for label in self.ax.xaxis.get_ticklabels():
			label.set_rotation(45)

		
		self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y\n%H:%M'))

		self.ax.set_yscale('log')
		self.ax.yaxis.set_major_formatter(ScalarFormatter())
		self.ax.yaxis.set_major_locator(mticker.MaxNLocator(10))


		plt.xlabel('Date')
		plt.ylabel('Price (BTC)')

		self.ax.autoscale_view()

		plt.show()

	def chartSMA(self,bars):

		chartData = self.readChartData(3,'d')

		dateconv = np.vectorize(dt.datetime.fromtimestamp)

		closep = chartData['close']
		sma = Indicators.sma(self,closep,bars)
		date = mdates.date2num(dateconv(chartData['date']))


		self.ax.plot(date,sma)

		plt.show()

	def chartPrice(self,interval, unit, data='close'):

		chartData = self.readChartData(interval,unit)
		x = chartData['date']
		y = chartData[data]

		self.ax.plot(x,y)

		#self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y\n%H:%M'))

		plt.show()
