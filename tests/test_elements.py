from include import elements
import unittest
class elements_test(unittest.TestCase):
	def setUp(self):
		self.ckt=elements.Subcircuit(['p_in','p_out','n_in','n_out'])
		R=elements.R(1)
		L=elements.L(1)
		C=elements.C(1)
		R.p.connect(L.p)
		R.p.connect(C.p)
		self.R=R
		self.L=L
		self.C=C

	def test_get_legs(self):
		legs=self.ckt.get_legs()
		all_in = lambda l1, l2: all([e in l2 for e in l1])
		self.assertTrue(all_in(legs,[self.ckt.p_in,self.ckt.p_out,self.ckt.n_in,self.ckt.n_out]))

	def test_deg(self):
		deg=self.L.deg()
		self.assertEqual(deg,2)


