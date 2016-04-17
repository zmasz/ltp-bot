import numpy as np
import datetime as dt

from bokeh.plotting import figure, output_file, show
from bokeh.io import curdoc

from data import Data
from indicators import Indicators


toDateTime = np.vectorize(dt.datetime.fromtimestamp)

unitSeconds = {'m':60, 'h':3600, 'd':86400, 'w':604800, 'M':2678400, 'y':32140800}


class Charter(Data, Indicators):

	def __init__(self):

		self.interval = 1
		self.unit = 'd'


		self.TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
		self.p = figure(plot_height=1000, plot_width=1800,
						x_axis_type="datetime", tools=self.TOOLS)

		#self.p.xaxis[0].formatter = DatetimeTickFormatter('%b-%d')

		self.p.title = self.pair

		self.p.border_fill_color = "whitesmoke"
		self.p.background_fill_color = "#111111"
		#self.p.background_fill_alpha = 0.25


		output_file('test')


		
	def chartCandles(self,frequency,showVolume=True):

		chartData = self.resampleChartData(frequency)

		date = chartData.index
		openp = chartData['open']
		closep = chartData['close']
		highp = chartData['high']
		lowp = chartData['low']
		volume = chartData['volume']

		inc  = closep > openp
		dec = openp > closep

		mids = (openp + closep)/2
		spans = abs(closep - openp)

		width = (date[1] - date[0]) / np.timedelta64(1,'ms') * .75

		self.p.segment(date[inc],highp[inc],date[inc],lowp[inc],color='#00FF00')
		self.p.segment(date[dec],highp[dec],date[dec],lowp[dec],color='#CC0000')
		self.p.rect(date[inc], mids[inc], width, spans[inc],  color="#00FF00")
		self.p.rect(date[dec], mids[dec], width, spans[dec],  color="#CC0000")

		#self.p.extra_y_ranges = {'volume':volume.values}
		#p.circle(dates,volume)
		#p.add_layout(LinearAxis(y_range_name='volume'),'right')






	def chartSMA(self, n, color='blue'):

		
		date = toDateTime(Data.getDates(self,self.interval,self.unit))
		closep = Data.getCloses(self,self.interval,self.unit)
		sma = Indicators.sma(self,closep,n)



		self.p.line(date, sma, color=color)


	def chartEMA(self, n, color='red'):

		date = toDateTime(Data.getDates(self,self.interval,self.unit))
		closep = Data.getCloses(self,self.interval,self.unit)
		ema = Indicators.ema(self,closep,n)



		self.p.line(date, ema, color=color)

	def updateData(self):

		pass

	def showChart(self):
		#curdoc().add_peridoic_callback(update, 5)
		show(self.p)


	def clearChart(self):

		Charter.__init__(self)





