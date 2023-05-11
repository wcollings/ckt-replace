from include import circuit as c
import unittest
class circuit_test(unittest.TestCase):
	def setUp(self) -> None:
		self.ckt=c.Boost()
	def test_get_legs_btw(self):
		V=self.ckt.elems[2]
		T=self.ckt.elems[0]
		l=self.ckt.get_legs_btw(V,T)

