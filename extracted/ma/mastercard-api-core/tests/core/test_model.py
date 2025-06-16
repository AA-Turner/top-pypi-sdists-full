#!/usr/bin/env python
# -*- coding: utf-8 -*-#
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
from mastercardapicore import RequestMap

class RequestMapTest(unittest.TestCase):

    def test_constructor(self):

        requestMapObj = RequestMap()
        self.assertEqual(requestMapObj.getObject(),{})

    def test_simpleSet(self):

        requestMapObj = RequestMap()
        requestMapObj.set("user",122132)

        self.assertEqual(requestMapObj.getObject(),{'user':122132})

        requestMapObj.set("name","naman")
        self.assertEqual(requestMapObj.getObject(),{'user':122132,'name':'naman'})

        #Override the value
        requestMapObj.set("name","atul")
        self.assertEqual(requestMapObj.getObject(),{'user':122132,'name':'atul'})

    def test_nestedSet(self):

        requestMapObj = RequestMap()

        requestMapObj.set("user.name.first","Naman")
        self.assertEqual(requestMapObj.getObject(),{'user':{'name':{'first':'Naman'}}})

        requestMapObj.set("user.name.last.middle","Kumar")
        self.assertEqual(requestMapObj.getObject(),{'user':{'name':{'first':'Naman','last':{'middle':'Kumar'}}}})

        requestMapObj.set("user.name.last.last","Aggarwal")
        self.assertEqual(requestMapObj.getObject(),{'user':{'name':{'first':'Naman','last':{'middle':'Kumar','last':'Aggarwal'}}}})



    def test_nestedSetWithList(self):

        requestMapObj = RequestMap()

        requestMapObj.set("user.name[0]","Naman")
        self.assertEqual(requestMapObj.getObject(),{'user':{'name':['Naman']}})

        requestMapObj.set("user.name[1]","Kumar")
        self.assertEqual(requestMapObj.getObject(),{'user':{'name':['Naman','Kumar']}})

        requestMapObj.set("user.name[2]","Aggarwal")
        self.assertEqual(requestMapObj.getObject(),{'user':{'name':['Naman','Kumar','Aggarwal']}})

        requestMapObj.set("user.name[3].class.id",1233)
        self.assertEqual(requestMapObj.getObject(),{'user':{'name':['Naman','Kumar','Aggarwal',{'class':{'id':1233}}]}})


    def test_setInvalidAction(self):

        requestMapObj = RequestMap()

        requestMapObj.set("user.name[0]","Naman")
        requestMapObj.set("user.name[1]","Kumar")
        requestMapObj.set("user.name[2]","Aggarwal")

        with self.assertRaises(TypeError):
            requestMapObj.set("user.name.class.id",1233)

        self.assertEqual(requestMapObj.getObject(),{'user':{'name':['Naman','Kumar','Aggarwal']}})



    def test_get(self):

        requestMapObj = RequestMap()

        requestMapObj.set("user.name[0]","Naman")
        requestMapObj.set("user.name[1]","Kumar")
        requestMapObj.set("user.name[2]","Aggarwal")
        requestMapObj.set("user.name[3].class.id",1233)
        requestMapObj.set("employee[0].name","atul")
        requestMapObj.set("employee[1].name","sumit")

        self.assertEqual(requestMapObj.get("user"),{'name':['Naman','Kumar','Aggarwal',{'class':{'id':1233}}]})
        self.assertEqual(requestMapObj.get("user.name"),['Naman','Kumar','Aggarwal',{'class':{'id':1233}}])
        self.assertEqual(requestMapObj.get("user.name[3]"),{'class':{'id':1233}})
        self.assertEqual(requestMapObj.get("user.name[3].class"),{'id':1233})
        self.assertEqual(requestMapObj.get("user.name[3].class.id"),1233)

        self.assertEqual(requestMapObj.get("user.name[3].class.id.value"),None)

        self.assertEqual(requestMapObj.get("user.name[4].class.id.value"),None)

        self.assertEqual(requestMapObj.get("employee"),[{'name':'atul'},{'name':'sumit'}])

        self.assertEqual(requestMapObj.get("employee[3]"),None)

        self.assertEqual(requestMapObj.get("user.name[4].class"),None)

        #check object is still the same
        self.assertEqual(requestMapObj.getObject(),{"user":{'name':['Naman','Kumar','Aggarwal',{'class':{'id':1233}}]},"employee":[{'name':'atul'},{'name':'sumit'}]})




    def test_setAll(self):

        requestMapObj = RequestMap()

        requestMapObj.setAll({'user.name':['Naman','Kumar','Aggarwal',{'class':{'id':1233}}]})
        self.assertEqual(requestMapObj.getObject(),{"user":{'name':['Naman','Kumar','Aggarwal',{'class':{'id':1233}}]}})

        requestMapObj.setAll({'employee.name':'atul'})
        self.assertDictEqual(requestMapObj.getObject(),{"user":{'name':['Naman','Kumar','Aggarwal',{'class':{'id':1233}}]},"employee":{"name":"atul"}})


        requestMapObj = RequestMap()
        requestMapObj.setAll([{"user.name":"Naman","user.lastname":"Aggarwal"}])
        self.assertEqual(requestMapObj.getObject(),{"list":[{"user":{"name":"Naman","lastname":"Aggarwal"}}]})


        #ARIZZINI: check list bug
        requestMapObj = RequestMap()
        requestMapObj.setAll([ { "id": 1, "title": "My Title", "body": "some body text", "userId": 1 } ])
        self.assertEqual(requestMapObj.getObject(),{"list":[{ "id": 1, "title": "My Title", "body": "some body text", "userId": 1 }]})
        self.assertEqual(requestMapObj.get("list[0].id"), 1)






if __name__ == '__main__':
    unittest.main()
