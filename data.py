from poloniex import Poloniex
import pandas as pd
import datetime as dt


class Data(Poloniex):
	
	
	def saveChartData(self,pair):
		start = dt.datetime(2008,1,1)
		end = dt.datetime.utcnow()
		Poloniex.getChartData(self,pair,start,end,300).to_csv('chartData'+pair+".csv")


#tester = Data()
#tester.saveChartData("BTC_XMR")