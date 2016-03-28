import collections

def mean(data):
	sum = 0
	for item in data:
		sum += item

	return sum/len(data)

def median(data):
	n = len(data)
	sorted_data = sorted(data)
	midpoint = n//2
	
	if n % 2 == 1:
		return sorted_data[midpoint]
	else:
		lo = midpoint-1
		hi = midpoint
		return (sorted_data[lo]+sorted_data[hi])/2

#return the pth-percentile value in data
def quantile(data,p):
	p_index = int(p*len(x))
	return sorted(data)[p_index]

#returns list
def mode(data):
	counts = collections.Counter(data)
	max_count = max(counts.values())

	return [xi for xi, count in counts.items() if count == max_count]

def data_range(data):

	return max(data) - min(data)

def variance(data):
	xbar = mean(data)
	n = len(data)
	numerator = sum([(x-xbar)**2 for x in data ])

	return numerator/n





print(variance([1,1,2,3,4,5,6]))