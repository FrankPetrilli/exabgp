# encoding: utf-8
"""
clusterlist.py

Created by Thomas Mangin on 2012-07-07.
Copyright (c) 2009-2012 Exa Networks. All rights reserved.
"""

from exabgp.structure.address import AFI,SAFI
from exabgp.structure.ip.inet import Inet
from exabgp.message.update.attribute import AttributeID,Flag,Attribute

# =================================================================== 

class ClusterID (Inet):
	def __init__ (self,cluster_id):
		Inet.__init__(self,AFI.ipv4,SAFI.unicast_multicast,cluster_id)


class ClusterList (Attribute):
	ID = AttributeID.CLUSTER_LIST
	FLAG = Flag.OPTIONAL
	MULTIPLE = False

	def __init__ (self,cluster_ids):
		self.clusters = []
		while cluster_ids:
			self.clusters.append(ClusterID(cluster_ids[:4]))
			cluster_ids = cluster_ids[4:]
		self._len = len(self.clusters)*4
		# XXX: are we doing the work for nothing ?
		self.packed = self._attribute(''.join([_.pack() for _ in self.clusters]))

	def pack (self):
		return self.packed

	def __len__ (self):
		return self._len

	def __str__ (self):
		if self._len != 1:
			return '[ %s ]' % ' '.join([str(_) for _ in self.clusters])
		return '%s' % self.clusters[0]

	def __repr__ (self):
		return str(self)

