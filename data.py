from poloniex import Poloniex
from chartGen import Charter

import pandas as pd
import datetime as dt
import numpy as np
import os
import time
from threading import Thread


def getSeconds(timeUnit):
	seconds = unitSeconds[timeUnit]

	return seconds


class Data(Poloniex):

	def __init__(self,exchange='poloniex',updateFlag = True):

		self.chartData = None

		self.updateFlag = updateFlag
		self.exchange = exchange

		self.fileIO()

		

		if self.updateFlag == True:
			t = Thread(target=self.updateData)
			#t.start()


	def fileIO(self):

		if 'data' not in os.listdir():
			os.mkdir('data')
			print("Created new data folder")
		os.chdir('data')

		if self.exchange not in os.listdir():
			os.mkdir(self.exchange)
			print("Created new ", self.exchange, " folder")
		os.chdir(self.exchange)

		if self.pair not in os.listdir():
			os.mkdir(self.pair)
			print("Created new ", self.pair, " folder")
		os.chdir(self.pair)


		if "chartData" + self.pair + ".h5" not in os.listdir():
			self.saveChartData()

		self.chartData = pd.read_hdf("chartData" + self.pair + ".h5",'table')

		os.chdir('../../..')

	
	def saveChartData(self,start=dt.datetime(2008,1,1)):
		now = dt.datetime.utcnow()
		df = Poloniex.getChartData(self,self.pair,start,now,300)
		df.to_hdf("chartData" + self.pair + ".h5",'table')
		print("chartData" + self.pair + ".h5 saved at " + os.getcwd())


	def saveOrderBook(self):
		pass

	def saveTradeHistory(self):
		pass

	def resampleClose(self, frequency):
		closep = self.chartData['close']
		closep = closep.resample(frequency).last()
		closep.name = 'close'
		return closep

	def resampleOpen(self, frequency):
		openp = self.chartData['open']
		openp = openp.resample(frequency).first()
		openp.name = 'open'
		return openp

	def resampleHigh(self, frequency):
		highp = self.chartData['high']
		highp = highp.resample(frequency).max()
		highp.name = 'high'
		return highp

	def resampleLow(self,frequency):
		lowp = self.chartData['low']
		lowp = lowp.resample(frequency).min()
		lowp.name = 'low'
		return lowp

	def resampleVolume(self,frequency):
		volume = self.chartData['volume']
		volume = volume.resample(frequency).sum()
		volume.name = 'volume'
		return volume


	def resampleChartData(self,frequency):
		chartData = pd.DataFrame(self.resampleOpen(frequency))
		chartData['high'] = self.resampleHigh(frequency)
		chartData['low'] = self.resampleLow(frequency)
		chartData['close'] = self.resampleClose(frequency)
		chartData['volume'] = self.resampleVolume(frequency)
		
		
		return chartData

		

	def updateData(self):

		size = len(self.chartData.index)
		lastDate = self.chartData.index[size-1]

		while self.updateFlag == True:
			time.sleep(3)
			self.chartData = pd.concat([self.chartData,Poloniex.getChartData(self,self.pair,lastDate,dt.datetime.utcnow(),300)])

