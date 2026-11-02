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

from __future__ import absolute_import
import unittest
from mastercardapicore import Config
from mastercardapicore import RequestMap
from .accountinquiry import AccountInquiry
from .base_test import BaseTest
from mastercardapicore import OAuthAuthentication
from os.path import dirname, realpath, join
from nose.tools import nottest

class AccountInquiryTest(BaseTest):


    def setUp(self):
        keyFile = join(dirname(dirname(realpath(__file__))),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d", keyFile, "test", "password")
        Config.setAuthentication(auth)
        Config.setDebug(False)


    def tearDown(self):
        Config.setProxy(None)

    def test_account_inquiry(self):

        mapObj = RequestMap()
        mapObj.set("AccountInquiry.AccountNumber","5343434343434343")

        response = AccountInquiry.update(mapObj)
        
        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "Listed", response.get("Account.Listed"),"True")
        self.customAssertEqual(ignoreAsserts, "Listed", response.get("Account.ReasonCode"),"S")
        self.customAssertEqual(ignoreAsserts, "Listed", response.get("Account.Reason"),"STOLEN")

    # def test_account_inquiry_with_proxy(self):

    #     Config.setProxy({'http': 'http://127.0.0.1:9999', 'https': 'http://127.0.0.1:9999'})

    #     mapObj = RequestMap()
    #     mapObj.set("AccountInquiry.AccountNumber","5343434343434343")

    #     response = AccountInquiry.update(mapObj)
        
    #     ignoreAsserts = []
        
    #     self.customAssertEqual(ignoreAsserts, "Listed", response.get("Account.Listed"),"True")
    #     self.customAssertEqual(ignoreAsserts, "Listed", response.get("Account.ReasonCode"),"S")
    #     self.customAssertEqual(ignoreAsserts, "Listed", response.get("Account.Reason"),"STOLEN")
        


if __name__ == '__main__':
    unittest.main()
