import numpy as np

class Indicators():

	def sma(self,closingPrices,windowSize):
		window = np.ones(windowSize)/float(windowSize)
		return np.convolve(closingPrices, window, 'same')
		
	def ema(self,values,window):
		weights = np.exp(np.linspace(-1.,0.,window))
		weights = weights.sum()

		a = np.convolve(values,weights)[:len(values)]
		a[:window] = a[window]

		return a




