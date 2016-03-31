from poloniex import Poloniex
from data import Data

class FX(Data):

	def __str__(self):
		return self.base + '_' + self.quote
	
	def __init__(self,base,quote):
		self.base = base
		self.quote = quote
		self.pair = self.base + '_' + self.quote
		self.price = Poloniex.getPrice(self,self.pair)



	



xmr = FX('BTC','XMR')
print(xmr.price)

