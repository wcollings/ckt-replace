
import string
from random import randint as rint
def rstr(size):
	return ''.join([string.ascii_lowercase[rint(0,25)] for i in range(size)])
class Node:
	_elems:list
	def __init__(self,inputs=[]):
		self.name=rstr(10)
		self._elems=inputs
	def merge(self,n):
		for elem in n._elems:
			if not elem in self._elems:
				self._elems.append(elem)
				elem.conn=self
	def __eq__(self,n):
		if isinstance(n,str):
			return self.name==n
		else:
			return self.name==n.name
	def __repr__(self):
		return self.name
