# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkalidns.endpoint import endpoint_data

class UpdateCustomLineRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Alidns', '2015-01-09', 'UpdateCustomLine','alidns')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_LineId(self): # Long
		return self.get_query_params().get('LineId')

	def set_LineId(self, LineId):  # Long
		self.add_query_param('LineId', LineId)
	def get_IpSegments(self): # RepeatList
		return self.get_query_params().get('IpSegment')

	def set_IpSegments(self, IpSegment):  # RepeatList
		for depth1 in range(len(IpSegment)):
			if IpSegment[depth1].get('EndIp') is not None:
				self.add_query_param('IpSegment.' + str(depth1 + 1) + '.EndIp', IpSegment[depth1].get('EndIp'))
			if IpSegment[depth1].get('StartIp') is not None:
				self.add_query_param('IpSegment.' + str(depth1 + 1) + '.StartIp', IpSegment[depth1].get('StartIp'))
	def get_LineName(self): # String
		return self.get_query_params().get('LineName')

	def set_LineName(self, LineName):  # String
		self.add_query_param('LineName', LineName)
	def get_Lang(self): # String
		return self.get_query_params().get('Lang')

	def set_Lang(self, Lang):  # String
		self.add_query_param('Lang', Lang)
