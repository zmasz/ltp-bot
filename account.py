
class Account:

	def __init__(self, equity):
		self.equity = equity
		self.units = 0

	def buy(self,amount, price):
		if self.equity < amount * price:
			return -1
		self.units += amount;
		self.equity -= amount * price

	def sell(self, amount, price):
		if self.units < amount:
			return -1

		self.units -= amount;
		self.equity += amount * price;

