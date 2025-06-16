#!/usr/bin/env python
# -*- coding: utf-8 -*-#
#
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
import unittest
import mastercardapicore.core.util as util

class UtilTests(unittest.TestCase):

    def test_validateURL_correctURL(self):

        #Normal url
        self.assertTrue(util.validateURL("http://www.mastercard.com"))

        #Url ending with /
        self.assertTrue(util.validateURL("http://www.mastercard.com/"))

        #Url with query Params
        self.assertTrue(util.validateURL("http://www.developer.mastercard.com?q=some&e=other"))

        #localhost with port and query
        self.assertTrue(util.validateURL("http://localhost:8080?q=some&e=other"))

    def test_validateURL_wrongURL(self):

        #empty
        self.assertFalse(util.validateURL(""))

        #string
        self.assertFalse(util.validateURL("somestring"))

        #invalid
        self.assertFalse(util.validateURL("http://www.developer,com"))

    def test_base64encode(self):

        #string
        self.assertEqual(util.base64Encode(b"mastercard"),"bWFzdGVyY2FyZA==")

        #string
        self.assertEqual(util.base64Encode(b"naman"),"bmFtYW4=")

        #string with special characters
        self.assertEqual(util.base64Encode(b"naman@3476@$%%^*%&^#mastercard"),"bmFtYW5AMzQ3NkAkJSVeKiUmXiNtYXN0ZXJjYXJk")

        #blank
        self.assertEqual(util.base64Encode(b""),"")

    def test_sha1encode(self):

        #string
        self.assertEqual(util.sha1Encode("mastercard"),b"\xc1\x9e3\xe7\xa9\xf2iZ\xda_?3E\xab%\xb9\xb2%\xd6e")

        #string
        self.assertEqual(util.sha1Encode("naman"),b"\xac\x94|)\xa0.db\xda\x10\x91Z\xab\xa8k\xdds)`\x84")

        #string with special characters
        self.assertEqual(util.sha1Encode("naman@3476@$%%^*%&^#mastercard"),b"\xcf\xc4\x01\"\xd9\xea\x06\xf9\xd0\xe5\xf3$\xaaH\xd5A|\'r\xfe")

        #blank
        self.assertEqual(util.sha1Encode(""),b"\xda9\xa3\xee^kK\r2U\xbf\xef\x95`\x18\x90\xaf\xd8\x07\t")


    def test_getReplacedPath(self):

        inputMap = {
            "one":1,
            "two":2,
            "three":"3",
            "four":4,
            "five":5
        }

        path = "http://localhost:8080/{one}/{two}/{three}/car"

        res = util.getReplacedPath(path,inputMap)

        self.assertEqual(res,"http://localhost:8080/1/2/3/car")
        self.assertEqual(len(inputMap),2)

        #Since now map does not have Key one this should raise KeyError
        with self.assertRaises(KeyError):
            res = util.getReplacedPath(path,inputMap)


    def test_subMap(self):

        inputMap = {
            "one":1,
            "two":2,
            "three":"3",
            "four":4,
            "five":5
        }

        keyList = ['one','three','five']

        subMap = util.subMap(inputMap,keyList)

        self.assertEqual(len(subMap),3)
        self.assertEqual(subMap['one'],1)
        self.assertEqual(subMap['three'],"3")
        self.assertEqual(subMap['five'],5)

        self.assertEqual(len(inputMap),2)
        self.assertEqual(inputMap['two'],2)
        self.assertEqual(inputMap['four'],4)

    def test_getNormaliedParams(self):

        url = "http://www.naman.com/abc?c=1&d=2&a=3"
        params = {
            "m":2,
            "b":3,
            "k":"5+8",
            "n":"a b"
        }

        nurl = util.normalizeParams(url,params)

        self.assertEqual(nurl,"a=3&b=3&c=1&d=2&k=5%2B8&m=2&n=a%20b")


    def test_uriRfc3986Encode(self):

        encode = util.uriRfc3986Encode("Formal=XML")
        self.assertEqual("Formal%3DXML",encode)

        encode = util.uriRfc3986Encode("WhqqH+TU95VgZMItpdq78BWb4cE=")
        self.assertEqual("WhqqH%2BTU95VgZMItpdq78BWb4cE%3D",encode)

        encode = util.uriRfc3986Encode("WhqqH+TU95VgZMItpdq78BWb4cE=&o")
        self.assertEqual("WhqqH%2BTU95VgZMItpdq78BWb4cE%3D%26o",encode)


if __name__ == '__main__':
    unittest.main()
