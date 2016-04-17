import inspect

import numpy as np

from account import Account
from data import Data



class Backtester(Account, Data):

	def __init__(self):
		Account.__init__(self,3)


	def backtest(self,func, *argv):

		argNum = func.__code__.co_argcount
		varNames = func.__code__.co_varnames

		for var in varNames:
			print(varNames)


		#return profit



