# encoding: utf-8
"""
aggregator.py

Created by Thomas Mangin on 2012-07-14.
Copyright (c) 2012 Exa Networks. All rights reserved.
"""

from exabgp.structure.address import AFI,SAFI
from exabgp.structure.asn import ASN
from exabgp.structure.ip.inet import Inet

from exabgp.message.update.attribute import AttributeID,Flag,Attribute

# =================================================================== AGGREGATOR (7)

class Aggregator (Attribute):
	ID = AttributeID.AGGREGATOR
	FLAG = Flag.TRANSITIVE|Flag.OPTIONAL
	MULTIPLE = False

	def __init__ (self,aggregator):
		asn = 0
		for value in (ord(_) for _ in aggregator[:-4]):
			asn = (asn << 8) + value
		self.asn=ASN(asn)
		self.speaker=Inet(AFI.ipv4,SAFI.unicast,aggregator[-4:])
		self._str = '%s:%s' % (self.asn,self.speaker)

	def pack (self,asn4,as4agg=False):
		if as4agg:
			self.ID = AttributeID.AS4_AGGREGATOR
			packed = self._attribute(self.asn.pack(True)+self.speaker.pack())
			self.ID = AttributeID.AGGREGATOR
			return packed
		elif asn4:
			return self._attribute(self.asn.pack(True)+self.speaker.pack())
		elif not self.asn.asn4():
			return self._attribute(self.asn.pack(False)+self.speaker.pack())
		else:
			return self._attribute(self.asn.trans()+self.speaker.pack()) + self.pack(True,True)


	def __len__ (self):
		raise RuntimeError('size can be 6 or 8 - we can not say')

	def __str__ (self):
		return self._str

	def __repr__ (self):
		return str(self)
