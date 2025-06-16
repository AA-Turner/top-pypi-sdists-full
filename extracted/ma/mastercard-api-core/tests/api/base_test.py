#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function
from builtins import str
import unittest
from mastercardapicore import RequestMap
from mastercardapicore import Config
from mastercardapicore import OAuthAuthentication
from os.path import dirname, realpath, join

class BaseTest(unittest.TestCase):
	responses = {}
	authentications = {
		"default": OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d", join(dirname(dirname(realpath(__file__))),"resources", "mcapi_sandbox_key.p12"), "test", "password"),
		"send_1": OAuthAuthentication("-mzBAF1UFssV7H1VDrJuXQ45AZlkmfNEoMUxocsGae1f9f59!cba9cef300b64e3e812698fd7a8b6bff0000000000000000", join(dirname(dirname(realpath(__file__))),"resources", "send_sdk_ci_1_sandbox.p12"), "keyalias", "keystorepassword"),
		"send_2": OAuthAuthentication("3nSpMB_IjYzyLhUbK37cHsYHVy7b3goCk1Q1DEinb60951d6!1b1af7c5aa1a4d5792ee9e707f9b87d60000000000000000", join(dirname(dirname(realpath(__file__))),"resources", "send_sdk_ci_2_sandbox.p12"), "keyalias", "keystorepassword"),
		"send_3": OAuthAuthentication("qPG4eNdxSW2pT1M5YdsyBoQs1CeyYmQ2JvYL2qq_a2b027f3!c6350fb087cc4df58700e117636e16c90000000000000000", join(dirname(dirname(realpath(__file__))),"resources", "send_sdk_ci_3_sandbox.p12"), "keyalias", "keystorepassword"),
		
	}

	@staticmethod
	def putResponse(name,response):
		BaseTest.responses[name] = response

	@staticmethod
	def resolveResponseValue(overrideValue):

            #arizzini: if plan value, return it
            if overrideValue.startswith("val:"):
                    return overrideValue[4:]
            else:
                    pos = overrideValue.find('.')
                    name = overrideValue[:pos]
                    #print "Example Name: %s" % name
                    key = overrideValue[pos+1:]
                    #print "Key Name: %s" % key

                    if name in BaseTest.responses:
                            response = BaseTest.responses[name]
                            if response.containsKey(key) == True:
                                    return str(response.get(key))
                            else:
                                    print("Key:'%s' is not found in the response" % key)
                    else:
                            print("Example:'%s' is not found in the response" % name)

                    return None

	def customAssertEqual(self,ignoreAsserts,key, actualValue, expectedValue):
		if (key not in ignoreAsserts):
			self.customAssertValue(expectedValue,actualValue)

	def customAssertValue(self,expected,actual):
		if isinstance(actual,float):
			self.assertEqual(float(expected), actual)
		elif isinstance(actual,bool):
			self.assertEqual(bool(expected), actual)
		elif isinstance(actual,int):
			self.assertEqual(int(expected), actual)
		elif isinstance(actual,bytes):
			self.assertEqual(bytes(expected), actual)
		else:
			self.assertEqual(str(expected).lower(), str(actual).lower())

	def setAuthentication(self, keyId):
		authentication = self.authentications[keyId]

		if authentication is None:
			raise Exception("No authentication found for keyId: " + keyId)

		Config.setAuthentication(authentication)

	def resetAuthentication(self):
		self.setAuthentication("default")