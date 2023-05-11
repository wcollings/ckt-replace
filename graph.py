import string
import numpy as np
from random import randint as rint
from dataclasses import dataclass
from itertools import permutations
import re
from include import *

elem_classes=list(string.ascii_uppercase)
for e in ['A','N','O','Y','Z']:
	elem_classes.remove(e)
def add(d,k,v):
	if k in d:
		d[k].append(v)
	else:
		d[k]=[v]
	return d

def create_Ullman(s:Circuit,k:Circuit):
		c={}
		for i in s.elems:
			for j in k.elems:
				degs_match=(i.deg() >=j.deg())
				types_match=(_type(i) == _type(j))
				if degs_match and types_match:
					c=add(c,j,i)
		
		all_in = lambda l1,l2: all([e in l2 for e in l1])
		valid=[]
		for elem in c:
			nref=[[str(e) for e in leg.conn._elems] for leg in elem.get_legs()]
			ntest=[[[str(e) for e in leg.conn._elems] for leg in _e.get_legs()] for _e in c[elem]]
			for i,test in enumerate(ntest):
				if all([all_in(l1,l2) for l1,l2 in zip(nref,test)]):
					valid.append(c[elem][i])
			c[elem]=valid
			valid=[]
		return c

def print_Ullman(s:Circuit,k:Circuit,c:dict):
		G=np.zeros((len(s.elems),len(k.elems)))
		for key in c:
			j=k.elems.index(key)
			for value in c[key]:
				i=s.elems.index(value)
				G[i,j]=1
		_s='  ' + ' '.join([str(e) for e in s.elems])
		print(_s)
		print('-'*len(_s))
		for i,row in enumerate(G.T):
			print(str(k.elems[i])+'|',end='')
			for j in row:
				if j==0:
					print('  ',end='')
				else:
					print('1 ',end='')
			print()

def replace(s:Circuit,k:Circuit,c:dict):
	counted_legs=[]
	temp_ckt=Circuit()
	# Find the element with the least number of candidates, then expand from there
	lengths=[len(c[l]) for l in c]
	Kn=list(c.keys())[lengths.index(min(lengths))]
	Sn=c[e][0]
	temp_ckt.add_elem(Sn)
	for leg in Kn.get_legs():
		counted_legs.append(leg)
		l=[l for l in leg.parent.get_connected() if not l in counted_legs]
		for elem in l:
				conn=k.get_legs_between(Kn,elem.parent)
				# TODO: Finish this train of thought










key_ckt=Boost()


# Boiler plate, ckt to search
V1=V(1,'1')
D1=D('1')
D2=D('2')
D3=D('3')
D4=D('4')
L1=L(1,'1')
V2=V(1,'2')
T1=T('1')
D5=D('5')
C1=C(1,'1')
R1=R(1,'1')
elems=[V1,D1,D2,D3,D4,L1,T1,D5,C1,R1,V2]
D1.p.connect(V1.p)
D1.p.connect(D2.n)
D1.n.connect(D3.p)
D4.p.connect(D3.n)
D4.n.connect(D2.p)
D1.n.connect(L1.p)
L1.n.connect(T1.d)
L1.n.connect(D5.n)
T1.g.connect(V2.p)
D5.p.connect(C1.n)
D5.p.connect(R1.n)
C1.p.connect(R1.p)
C1.p.connect(T1.s)
C1.p.connect(D2.p)
V1.n.connect(D4.p)
V2.n.connect(D4.n)
search_ckt=Circuit()
search_ckt.elems=elems

#print(str(search_ckt))
print(key_ckt.elems[0].get_connected())
#print(str(key_ckt))
#print(T1.deg())
#print(T1.deg())
c=create_Ullman(search_ckt,key_ckt)
#print_Ullman(search_ckt,key_ckt,c)
