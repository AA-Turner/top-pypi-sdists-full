#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2016 MasterCard International Incorporated
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# Neither the name of the MasterCard International Incorporated nor the names of its
# contributors may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#


from mastercardapicore import BaseObject
from mastercardapicore import RequestMap
from mastercardapicore import OperationConfig
from mastercardapicore import OperationMetadata


class Combinationctrlsalertresource(BaseObject):
	"""
	
	"""

	__config = {
		
		"24888407-1ef9-4397-a2a4-1e1cf2d49b93" : OperationConfig("/issuer/spendcontrols/v1/card/{uuid}/controls/alerts/filters", "query", [], []),
		
		"c22923eb-383c-43e6-957c-1f9fcc33a46c" : OperationConfig("/issuer/spendcontrols/v1/card/{uuid}/controls/alerts/filters", "create", [], []),
		
	}

	def getOperationConfig(self,operationUUID):
		if operationUUID not in self.__config:
			raise Exception("Invalid operationUUID: "+operationUUID)

		return self.__config[operationUUID]

	def getOperationMetadata(self):
		return OperationMetadata("0.0.1", "https://sandbox.api.mastercard.com")







	@classmethod
	def query(cls,criteria):
		"""
		Query objects of type Combinationctrlsalertresource by id and optional criteria
		@param type criteria
		@return Combinationctrlsalertresource object representing the response.
		@raise ApiException: raised an exception from the response status
		"""

		return BaseObject.execute("24888407-1ef9-4397-a2a4-1e1cf2d49b93", Combinationctrlsalertresource(criteria))

	@classmethod
	def create(cls,mapObj):
		"""
		Creates object of type Combinationctrlsalertresource

		@param Dict mapObj, containing the required parameters to create a new object
		@return Combinationctrlsalertresource of the response of created instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("c22923eb-383c-43e6-957c-1f9fcc33a46c", Combinationctrlsalertresource(mapObj))







