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
from aliyunsdkdcdn.endpoint import endpoint_data

class DescribeDcdnUserSecDropRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'dcdn', '2018-01-15', 'DescribeDcdnUserSecDrop')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_Data(self): # String
		return self.get_query_params().get('Data')

	def set_Data(self, Data):  # String
		self.add_query_param('Data', Data)
	def get_Metric(self): # String
		return self.get_query_params().get('Metric')

	def set_Metric(self, Metric):  # String
		self.add_query_param('Metric', Metric)
	def get_SecFunc(self): # String
		return self.get_query_params().get('SecFunc')

	def set_SecFunc(self, SecFunc):  # String
		self.add_query_param('SecFunc', SecFunc)
