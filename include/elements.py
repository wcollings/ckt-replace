from .node import Node
import string
from random import randint as rint
def rstr(size):
	return ''.join([string.ascii_lowercase[rint(0,25)] for i in range(size)])
class Elem:
	'''
		Holds a single element (C,L,R,T,D,V,etc)
	'''
	polar:bool
	def __init__(self, *args, **kwargs):
		'''
		The first arg should be the name of the part, past that everything is ignored for now
		'''
		self.name=args[0]#+rstr(4)
		self.hash_name=args[0]+rstr(4)
		pass

	def get_legs(self):
		'''
		Returns all the legs this device has, as a list
		'''
		return [l for l in self.__dict__.values() if isinstance(l,Leg)]
	
	def get_connected(self, legs=None)->list:
		'''
		Get the list of elements connected to this element (on any leg)
		Return
		------
		list
			All elements that share a common node with any of the legs of this element
		'''
		if legs is None:
			legs=self.get_legs()
		elems=[]
		for leg in legs:
			elems.append([e for e in leg.conn._elems if e != leg])
		return sum(elems,[])


	def deg(self)->int:
		'''
		Get the degree of this element, in the Graph Theory understanding (treating this as a vertex of some graph)
		Return
		------
		int
			The number of connected elements to this device
		'''
		return len(self.get_connected())

	def add_leg(self,l):
		'''
			A shortcut to create a new leg on a part. Primarily for use in initialization of derived classes.

			Parameters
			----------
			l:str
				The name of the new leg
			Return
			------
			None
		'''
		temp_leg=Leg(self,l,Node([]))
		temp_leg.conn._elems.append(temp_leg)
		self.__dict__[l]=temp_leg

	def __eq__(self,e):
		if isinstance(e,Elem):
			return self.name==e.name
		if isinstance(e,str):
			return self.name==e
	def __repr__(self):
		return self.name[0]
	def __hash__(self):
		return sum([ord(x) for x in self.hash_name])

class Leg:
	'''
	A base class for each leg of a device.
	'''
	parent:Elem
	side:str
	conn:Node
	def __init__(self,p,s,c):
		self.parent=p
		self.side=s
		self.conn=c
	def connect(self,l):
		self.conn.merge(l.conn)
	def __repr__(self):
		if self.parent.polar:
			return f'{self.parent.name[0]}.{self.side}'
		else:
			return self.parent.name[0]+'.l'

class two_term(Elem):
	'''
	Generic type for two-terminal devices
	'''
	p:Leg
	n:Leg
	def __init__(self,*args, **kwargs):
		super().__init__(*args, **kwargs)
		self.add_leg('p')
		self.add_leg('n')
	def __repr__(self):
		return self.name[0]

class C(two_term):
	def __init__(self,val=0,*args):
		super().__init__('C',val)
		self.polar=False

class R(two_term):
	def __init__(self,val=0,*args):
		super().__init__('R',val)
		self.polar=False

class L(two_term):
	def __init__(self,val=0,*args):
		super().__init__('L',val)
		self.polar=False

class V(two_term):
	def __init__(self,val,*args):
		super().__init__('V',val)
		self.polar=True

class D(two_term):
	def __init__(self,*args):
		super().__init__('D')
		self.polar=True

class T(Elem):
	d:Leg
	g:Leg
	s:Leg
	def __init__(self, *args):
		super().__init__('T')
		self.polar=True
		for l in ['d','g','s']:
			self.add_leg(l)
	def __repr__(self):
		return 'T'

	
class Subcircuit(Elem):
	def __init__(self,legs, *args, **kwargs):
		super().__init__('X')
		self.polar=True
		for leg in legs:
			self.add_leg(leg)
	def __repr__(self):
		return self.name

