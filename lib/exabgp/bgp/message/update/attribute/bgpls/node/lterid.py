# encoding: utf-8
"""
nodename.py

Created by Evelio Vila on 2016-12-01.
Copyright (c) 2014-2016 Exa Networks. All rights reserved.
"""

from exabgp.protocol.ip import IP
from exabgp.bgp.message.notification import Notify

from exabgp.bgp.message.update.attribute.bgpls.linkstate import LINKSTATE


#   |     1028    | IPv4 Router-ID of    |        4 | [RFC5305]/4.3     |
#   |             | Local Node           |          |                   |
#   |     1029    | IPv6 Router-ID of    |       16 | [RFC6119]/4.1     |
#   |             | Local Node           |          |                   |
#   +-------------+----------------------+----------+-------------------+
#	https://tools.ietf.org/html/rfc7752 sec 3.3.1.4  - Traffic Engineering RouterID

@LINKSTATE.register(lsid=1028)
@LINKSTATE.register(lsid=1029)
class LocalTeRid(object):

	def __init__ (self, terid):
		self.terid = terid

	def __repr__ (self):
		return "Local TE Router ID: %s" % (self.terid)

	@classmethod
	def unpack (cls,data,length):
		if len(data) == 4:
    		# IPv4 address
			terid = IP.unpack(data[:4])
		elif len(data) == 16:
    		# IPv6
			terid = IP.unpack(data[:16])
		return cls(terid=terid)

	def json (self,compact=None):
		return '"local-te-router-id": "%s"' % str(self.terid)
