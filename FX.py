from poloniex import Poloniex
from data import Data
from charter import Charter
from backtester import Backtester

import numpy as np

class FX(Charter,Backtester,Data):

	def __str__(self):
		return self.base + '_' + self.quote
	
	def __init__(self,base,quote):
		self.base = base
		self.quote = quote
		self.pair = self.base + '_' + self.quote
		self.price = Poloniex.getPrice(self,self.pair)

		Data.__init__(self)
		Charter.__init__(self)
		#Backtester.__init__(self)


#xmr = FX("BTC","XMR")
#xmr.saveChartData()


#xmr.chartCandles('7D')
#xmr.showChart()