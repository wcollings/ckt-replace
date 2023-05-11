import numpy as np
from itertools import permutations
from .elements import *
import re

def defined_classes():
	g=globals().copy()
	names=[]
	for name, obj in g.items():
		if isinstance(obj, type):
			names.append(name)
	return names
def _type(t):
	pat=re.compile("(.\w+).(\w+)'")
	res=pat.search(str(type(t)))
	return res.groups()[-1]
def get_nodes(l):
	'''
	Returns all the nodes in the circuit, as a list
	'''
	nodes=[]
	for elem in l:
		for leg in elem.get_legs():
			if leg.conn not in nodes:
				nodes.append(leg.conn)
	return nodes

class Circuit:
	elems:list
	items_added:bool
	def __init__(self):
		self.G=None
		self.items_added=True
		self.elems=[]

	def add_elem(self,e):
		'''
			Add an element to the given circuit. All the connections, if already specified, remain
		'''
		self.elems.append(e)
		self.item_added=True

	def __getattr__(self,name):
		'''
			Three shortcuts exist:
			1. If you want the graph, call *obj*.G or *obj*.H (case insensitive)
			2. If you want a specific element, call *obj*.*elem_name*, for example *ckt.L2*
			3. If you want all the elements of a specific type, call *obj*.*elem_type*, for example *ckt.R* for all the resistors
		'''
		if name in self.__dict__:
			return self.__dict__[name]
		#if name=='elems':
			#return self.elems
		#if name in ['G','g','H','h']:
			#return self.G
		if name in defined_classes():
			return [elem for elem in self.elems if _type(elem)==name]
		index=self.elems.index(name)
		return self.elems[index]
	
	def make_graph(self):
		'''
			Take the current circuit, and create an adjacency matrix for it
		'''
		if self.items_added:
			self.G=np.chararray((len(self.elems),len(self.elems)),itemsize=10)
			self.H=np.zeros((len(self.elems),len(self.elems)))
			self.G[:]=' '*5
			for node in get_nodes(self.elems):
				lut=[self.elems.index(c.parent) for c in node._elems]
				for ind in permutations(lut,2):
					self.G[ind[0],ind[1]]=node.name
					self.H[ind[0],ind[1]]+=1
		self.items_added=False

	def get_legs_btw(self,e1,e2):
		'''
			Given two elements (assumed to be within the circuit defined here), back-trace what legs
			are attached to what nodes, or rather which legs of which components are attached
		'''
		ind1=self.elems.index(e1)
		ind2=self.elems.index(e2)
		node_name=self.G[ind1,ind2].decode()
		if node_name=='':
			return [] #Unless I want to try a traversal algo and return the entire path??
		nodes=get_nodes(self.elems)
		node_index=nodes.index(node_name)
		node=nodes[node_index]
		elems=node._elems
		# Sort elems with e1 first
		return node._elems

	def elems_and_numbers(self):
		'''
			Returns a dict of types of elements in the circuit, and counts of each element.
			example: {'T':2,'L':5,'R':15,...}
		'''
		elem_count={}
		for elem in self.elems:
			elem_t=_type(elem)
			if elem_t in elem_count:
				elem_count[elem_t]=elem_count[elem_t]+1
			else:
				elem_count[elem_t]=1
		return elem_count

	def __str__(self):
		if self.G is None:
			self.make_graph()
		s='  ' + ' '.join([str(e) for e in self.elems]) + '\n'
		temp= '-'*(len(s))+'\n'
		s+=temp
		for i,row in enumerate(self.H):
			s += str(self.elems[i]) + '|'
			for elem in row:
				if elem == 0:
					s+='  '
				else:
					s+= str(int(elem))+' '
			s+='\n'
		return s

class Boost(Circuit):
	def __init__(self,*args):
		super().__init__()
		self.subckt=Subcircuit(['p_in','p_out','n_in','n_out'])
		self.subckt.name='Boost'
		v=V(1)
		d=D()
		t=T()
		t.d.connect(d.n)
		t.g.connect(v.p)
		t.s.connect(v.n)
		self.elems=[t,d,v]
		self.subckt.p_in.conn=t.d.conn
		self.subckt.p_out.conn=d.p.conn
		self.subckt.n_in.conn=t.s.conn
		self.subckt.n_out.conn=t.s.conn
		self.make_graph()
