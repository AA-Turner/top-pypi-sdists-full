#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from .combinationctrlsalertresource import Combinationctrlsalertresource
from mastercardapicore import APIException
from .accountinquiry import AccountInquiry
from .base_test import BaseTest
from mastercardapicore import OAuthAuthentication
from os.path import dirname, realpath, join



class AllTest(BaseTest):

            def setUp(self):
                keyFile = join(dirname(dirname(realpath(__file__))),"resources","sandbox9_sandbox.p12")
                auth = OAuthAuthentication("rJWlVy-B-8Tfa5k0raxXy_BgKIfUx41sYT9CMdBod8885a33!50383044ee074864822d99b0a0295aa30000000000000000", keyFile, "sandbox9", "keystorepassword")
                Config.setAuthentication(auth)
                Config.setDebug(False)
    
            def test_181_example_filter_controls_alert_get_request(self):
                # 
                true = True

                map = RequestMap()
                map.set("uuid", "5tcTMLIqEg88gN6ClBGqH2TYDQuBDLT4ey5zjQQ7alg")
                #map.set("uuid", BaseTest.resolveResponseValue("example_cardregister_postrequest.uuid"));
                map.set("filters[0].filterId", "5555");

                try:
                    response = Combinationctrlsalertresource.query(map)
                except APIException as e:
                    self.assertEqual(e.getHttpStatus(), 404)
                    self.assertEqual(e.getMessage(), "No cards provisioned for the UUID.")
                    self.assertEqual(e.getReasonCode(), "card.invalid")
                    self.assertEqual(e.getSource(), "Validation")

                #BaseTest.putResponse("example_filter_controls_alert_get_request", response)
                #self.resetAuthentication()