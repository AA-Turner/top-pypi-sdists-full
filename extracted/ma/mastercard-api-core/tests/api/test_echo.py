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
from mastercardapicore import RequestMap
from mastercardapicore import Config
from mastercardapicore import OAuthAuthentication
from os.path import dirname, realpath, join
import time
from .base_test import BaseTest
from .echo import Echo
import json



class EchoTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()


    def test_utf_8(self):
        
        utf8String = u"мảŝťễřÇāŕď Ľẵвš ạאָđ мãśţēяĈẫřđ ĀקÏ ŕồçҝş..."
        

        mapObj = RequestMap()
        mapObj.set("Name",utf8String)
        
        
        response = Echo.create(mapObj)#

        responseMap = RequestMap()
        responseMap.parseJson(response.get("body"))  

        self.assertEqual(utf8String, responseMap.get("Name"))

        #self.assertEqual(response2.get("Name"), utf8String)
        
    

if __name__ == '__main__':
    unittest.main()

