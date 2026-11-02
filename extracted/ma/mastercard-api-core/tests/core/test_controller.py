
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

from __future__ import print_function
from __future__ import absolute_import
import unittest
from .test_resourceconfig import ResourceConfig
from mastercardapicore.core.controller import APIController
from mastercardapicore import OperationConfig
from mastercardapicore import OperationMetadata
from mastercardapicore import Config
from mastercardapicore import Environment
from mastercardapicore import Authentication
from mastercardapicore import OAuthAuthentication
from mastercardapicore import Constants
from mastercardapicore import APIException
import json
from os.path import dirname, realpath, join

try:
    from mock import Mock, patch
except ImportError:
    from unittest.mock import Mock, patch

class APIControllerBaseTest(unittest.TestCase):

    def setUp(self):
        keyFile = join(dirname(dirname(realpath(__file__))),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d",keyFile, "test", "password")
        Config.setAuthentication(auth)
        self.controller = APIController()


class APIControllerTests(APIControllerBaseTest):

    def test_config(self):
        self.assertEqual(Config.getEnvironment(), Environment.SANDBOX)

        Config.setSandbox(False)
        self.assertEqual(Config.getEnvironment(), Environment.PRODUCTION)
        
        Config.setSandbox(True)
        self.assertEqual(Config.getEnvironment(), Environment.SANDBOX)
        
        Config.setEnvironment(Environment.STAGE)
        self.assertEqual(Config.getEnvironment(), Environment.STAGE)
        
        Config.setEnvironment("")
        self.assertEqual(Config.getEnvironment(), Environment.STAGE)
        
        Config.setEnvironment(None)
        self.assertEqual(Config.getEnvironment(), Environment.STAGE)
        
    def test_ResourceConfig(self):
        
        ResourceConfig.getInstance().setEnvironment(Environment.SANDBOX)
        self.assertEqual(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getVersion())
        self.assertEqual(ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getHost())
        self.assertEqual(ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getContext())


    def test_removeForwareSlashFromTail(self):

        #Url with /
        self.assertEqual(self.controller.removeForwardSlashFromTail("http://localhost:8080/"),"http://localhost:8080")

        #Url with parameters and /
        self.assertEqual(self.controller.removeForwardSlashFromTail("http://localhost:8080/?nam=1&an=1/"),"http://localhost:8080/?nam=1&an=1")

        #Url without /
        self.assertEqual(self.controller.removeForwardSlashFromTail("http://localhost:8080"),"http://localhost:8080")


    def test_getURL(self):

        inputMap = {
            'api' : 'lostandstolen',
            'version' : 1,
            'three' : 3,
            'four': 4,
            'five':5
        }
        
        config = OperationConfig("/fraud/{api}/v{version}/account-inquiry", "create", [], [])
        metadata = OperationMetadata("0.0.1", "https://sandbox.api.mastercard.com")

        url = self.controller.getURL(config,metadata,inputMap)

        #Normal URL
        self.assertEqual(url,"https://sandbox.api.mastercard.com/fraud/lostandstolen/v1/account-inquiry")
        self.assertEqual(3,len(inputMap))

        inputMap = {
            'api' : 'lostandstolen',
            'version' : 1,
            'three' : 3,
            'four': 4,
            'five':5
        }

        #URL with trailing /
        config = OperationConfig("/fraud/{api}/v{version}/account-inquiry/", "create", [], [])
        
        
        url = self.controller.getURL(config,metadata,inputMap)
        self.assertEqual(url,"https://sandbox.api.mastercard.com/fraud/lostandstolen/v1/account-inquiry")
        self.assertEqual(3,len(inputMap))

        inputMap = {
            'api' : 'lostandstolen',
            'version' : 1,
            'three' : 3,
            'id':1
        }

        #URL with id and action delete
        config = OperationConfig("/fraud/{api}/v{version}/account-inquiry/{id}", "delete", [], [])
        
        url = self.controller.getURL(config,metadata,inputMap)
        self.assertEqual(url,"https://sandbox.api.mastercard.com/fraud/lostandstolen/v1/account-inquiry/1")
        self.assertEqual(1,len(inputMap))


        inputMap = {
            'api' : 'lostandstolen',
            'version' : 1,
            'three' : 3,
            'id':1
        }


        #URL with id in inputMap but not in url
        config = OperationConfig("/fraud/{api}/v{version}/account-inquiry", "delete", [], [])
        
        url = self.controller.getURL(config,metadata, inputMap)
        self.assertEqual(url,"https://sandbox.api.mastercard.com/fraud/lostandstolen/v1/account-inquiry")
        self.assertEqual(2,len(inputMap))

        inputMap = {
            'api' : 'lostandstolen',
            'version' : 1,
            'three' : 3,
            'id':1
        }

        #URL with id in inputMap but not in url and method create
        config = OperationConfig("/fraud/{api}/v{version}/account-inquiry", "create", [], [])
        
        url = self.controller.getURL(config, metadata, inputMap)
        self.assertEqual(url,"https://sandbox.api.mastercard.com/fraud/lostandstolen/v1/account-inquiry")
        self.assertEqual(2,len(inputMap))
        

        #Now that the key api and version are not there in map
        #This should raise a key error
        with self.assertRaises(KeyError):
            config = OperationConfig("/fraud/{api}/v{version}/account-inquiry", "create", [], [])
            
            url = self.controller.getURL(config,metadata,inputMap)
            print(url)


    def test_getMethod(self):

        self.assertEqual(self.controller.getMethod(APIController.ACTION_CREATE),APIController.HTTP_METHOD_POST)
        self.assertEqual(self.controller.getMethod(APIController.ACTION_DELETE),APIController.HTTP_METHOD_DELETE)
        self.assertEqual(self.controller.getMethod(APIController.ACTION_UPDATE),APIController.HTTP_METHOD_PUT)
        self.assertEqual(self.controller.getMethod(APIController.ACTION_READ),APIController.HTTP_METHOD_GET)
        self.assertEqual(self.controller.getMethod(APIController.ACTION_LIST),APIController.HTTP_METHOD_GET)
        self.assertEqual(self.controller.getMethod(APIController.ACTION_QUERY),APIController.HTTP_METHOD_GET)
        #Should work even if case does not match
        self.assertEqual(self.controller.getMethod(APIController.ACTION_UPDATE.lower()),APIController.HTTP_METHOD_PUT)
        #Returns none for not matching string
        self.assertEqual(self.controller.getMethod("SomeString"),None)


    def test_getRequestObject(self):

        #TEST POST with jsonNative and ContentTypeOverride
     
        inputMap = {
            "param1":1,
            "param2":2,
            "a":"1",
        }
        
        config = OperationConfig("/fraud/api/v1/account-inquiry", "create", [], ["a"])
        metadata = OperationMetadata("mock:0.0.1", "https://sandbox.api.mastercard.com", None, True, "text/json")

        url = "https://sandbox.api.mastercard.com/fraud/api/v1/account-inquiry"
        
        #Create Request with inputMap
        request = self.controller.getRequestObject(config,metadata,inputMap)

        self.assertEqual(request.url,url)
        self.assertEqual(request.params,{"a":"1"})
        self.assertEqual(json.loads(request.data),inputMap)
        
        self.assertEqual(request.headers[APIController.KEY_ACCEPT], "text/json; charset=UTF-8")
        self.assertEqual(request.headers[APIController.KEY_CONTENT_TYPE], "text/json; charset=UTF-8")
        self.assertEqual(request.headers[APIController.KEY_USER_AGENT], Constants.getCoreVersion()+"/mock:0.0.1")

        self.assertTrue("oauth_body_hash" in request.headers["Authorization"]);     


        #TEST POST
     
        inputMap = {
            "param1":1,
            "param2":2,
            "a":"1",
        }
        
        config = OperationConfig("/fraud/api/v1/account-inquiry", "create", [], ["a"])
        metadata = OperationMetadata("mock:0.0.1", "https://sandbox.api.mastercard.com", None, True)

        url = "https://sandbox.api.mastercard.com/fraud/api/v1/account-inquiry"
        
        #Create Request with inputMap
        request = self.controller.getRequestObject(config,metadata,inputMap)

        self.assertEqual(request.url,url)
        self.assertEqual(request.params,{"a":"1"})
        self.assertEqual(json.loads(request.data),inputMap)
        
        self.assertEqual(request.headers[APIController.KEY_ACCEPT], APIController.APPLICATION_JSON)
        self.assertEqual(request.headers[APIController.KEY_CONTENT_TYPE], APIController.APPLICATION_JSON)
        self.assertEqual(request.headers[APIController.KEY_USER_AGENT], Constants.getCoreVersion()+"/mock:0.0.1")

        self.assertTrue("oauth_body_hash" in request.headers["Authorization"]);


        #TEST GET

        inputMap = {
            "param1":1,
            "param2":2,
            "a":"1",
            "b":2
        }


        config = OperationConfig("/fraud/api/v1/account-inquiry", "list", [], ["a", "b"])

        #List Request with inputMap
        request = self.controller.getRequestObject(config,metadata,inputMap)

        self.assertEqual(request.params,{"param1":1,"param2":2,"a":"1","b":2})
        self.assertEqual(request.data,[])
        self.assertEqual(request.url,url)

        self.assertEqual(request.headers[APIController.KEY_ACCEPT], APIController.APPLICATION_JSON)
        self.assertFalse( APIController.KEY_CONTENT_TYPE in request.headers )
        self.assertEqual(request.headers[APIController.KEY_USER_AGENT], "mastercard-api-core(python):1.4.12/mock:0.0.1")
        self.assertTrue("oauth_body_hash" not in request.headers["Authorization"]);

        inputMap = {
            "a":"1",
            "b":2
        }

        #List Request with no inputMap
        request = self.controller.getRequestObject(config,metadata,inputMap)

        self.assertEqual(request.params,{"a":"1","b":2})
        self.assertEqual(request.data,[])
        self.assertEqual(request.url,url)

        self.assertEqual(request.headers[APIController.KEY_ACCEPT], APIController.APPLICATION_JSON)
        self.assertFalse( APIController.KEY_CONTENT_TYPE in request.headers )
        self.assertEqual(request.headers[APIController.KEY_USER_AGENT], "mastercard-api-core(python):1.4.12/mock:0.0.1")

       
    def test_environment(self):
        inputMap = []
        
        
        Config.setEnvironment(Environment.SANDBOX);
        
        config = OperationConfig("/fraud/#env/v1/account-inquiry", "create", [], [])
        metadata = OperationMetadata("0.0.1", ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext())

        #dafault
        metadata = OperationMetadata("0.0.1", ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext())
        url = self.controller.getURL(config,metadata,inputMap)
        self.assertEqual(url,"https://sandbox.api.mastercard.com/fraud/v1/account-inquiry")
        
        #dafault
        Config.setEnvironment(Environment.PRODUCTION_MTF)
        metadata = OperationMetadata("0.0.1", ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext())
        self.assertEqual(self.controller.getURL(config,metadata,inputMap),"https://api.mastercard.com/fraud/mtf/v1/account-inquiry")
        
        Config.setEnvironment(Environment.PRODUCTION_ITF)
        metadata = OperationMetadata("0.0.1", ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext())
        self.assertEqual(self.controller.getURL(config,metadata,inputMap),"https://api.mastercard.com/fraud/itf/v1/account-inquiry")
        
        Config.setEnvironment(Environment.STAGE)
        metadata = OperationMetadata("0.0.1", ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext())
        self.assertEqual(self.controller.getURL(config,metadata,inputMap),"https://stage.api.mastercard.com/fraud/v1/account-inquiry")
        
        Config.setEnvironment("")
        metadata = OperationMetadata("0.0.1", ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext())
        self.assertEqual(self.controller.getURL(config,metadata,inputMap),"https://stage.api.mastercard.com/fraud/v1/account-inquiry")
        
        Config.setEnvironment(None)
        metadata = OperationMetadata("0.0.1", ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext())
        self.assertEqual(self.controller.getURL(config,metadata,inputMap),"https://stage.api.mastercard.com/fraud/v1/account-inquiry")
        
        Config.setEnvironment(Environment.LOCALHOST)
        metadata = OperationMetadata("0.0.1", ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext())
        self.assertEqual(self.controller.getURL(config,metadata,inputMap),"http://localhost:8081/fraud/v1/account-inquiry")
        
        Config.clearResourceConfig()
        

    def test_execute(self):

        inputMap = {

            "Content-Type":"application/json",
            "a":1,
            "b":"naman aggarwal %20",
            "id":3
        }

        
        config = OperationConfig("/user/{a}", "list", ["Content-Type"], [])
        metadata = OperationMetadata("0.0.1", "https://sandbox.api.mastercard.com")

        with patch('mastercardapicore.core.controller.Config') as mock_config:
            #Set Authentication to None
            mock_config.getAuthentication.return_value = None
            
            

            with self.assertRaises(APIException):
                content = self.controller.execute(config,metadata,inputMap)

            #Set Authentication to some other object
            mock_config.getAuthentication.return_value = "stringobject"

            with self.assertRaises(APIException):
                content = self.controller.execute(config,metadata,inputMap)


        with patch('mastercardapicore.core.controller.Session') as mock_session:
            response = Mock()
            response.content = "Some Content"
            response.status_code = 200
            mock_session().send.return_value =response
            content = self.controller.execute(config,metadata,inputMap)


    def test_handleResponse(self):

        response = Mock()
        response.status_code = 200

        content = self.controller.handleResponse(response,None)
        self.assertEqual(content,"")

        content = self.controller.handleResponse(response,{"a" :1})
        self.assertEqual(content,{"a" :1})

        response.status_code = 301
        
        with self.assertRaises(APIException) as cm:
            content = self.controller.handleResponse(response,{"Errors" :{"Error":{"message":"Some error", "ReasonCode": "some code"}}})
            
        self.assertEqual(cm.exception.getHttpStatus(), 301)
        self.assertEqual(cm.exception.getMessage(), "Moved Permanently")
        self.assertEqual(cm.exception.getReasonCode(), "some code")
        self.assertEqual(cm.exception.getSource(), None)
        

        #test errors.error.reasoncode
        with self.assertRaises(APIException) as cm:
            content = self.controller.handleResponse(response,{"Errors" :{"Error":{"Source":"System", "ReasonCode":"SYSTEM_ERROR1", "Description":"Unknown Error1", "Recoverable":"false"}}})
            
        self.assertEqual(cm.exception.getHttpStatus(), 301)
        self.assertEqual(cm.exception.getMessage(), "Unknown Error1")
        self.assertEqual(cm.exception.getReasonCode(), "SYSTEM_ERROR1")
        self.assertEqual(cm.exception.getSource(), "System")
        self.assertEqual(cm.exception.getRawErrorData().get("errors.error.Source"), "System")
        
        #test errors.error.reasoncode case insentive
        with self.assertRaises(APIException) as cm:
            content = self.controller.handleResponse(response,{"errors" :{"error":{"source":"System", "reasoncode":"SYSTEM_ERROR1", "description":"Unknown Error1", "recoverable":"false"}}})
            
        self.assertEqual(cm.exception.getHttpStatus(), 301)
        self.assertEqual(cm.exception.getMessage(), "Unknown Error1")
        self.assertEqual(cm.exception.getReasonCode(), "SYSTEM_ERROR1")
        self.assertEqual(cm.exception.getSource(), "System")
        self.assertEqual(cm.exception.getRawErrorData().get("errors.error.Source"), "System")

        #test errors.error[0].reasoncode case insensitive
        with self.assertRaises(APIException) as cm:
            content = self.controller.handleResponse(response,{"errors" :{"error":[{"source":"System", "reasoncode":"SYSTEM_ERROR1", "description":"Unknown Error1", "recoverable":"false"}]}})
            
        self.assertEqual(cm.exception.getHttpStatus(), 301)
        self.assertEqual(cm.exception.getMessage(), "Unknown Error1")
        self.assertEqual(cm.exception.getReasonCode(), "SYSTEM_ERROR1")
        self.assertEqual(cm.exception.getSource(), "System")
        self.assertEqual(cm.exception.getRawErrorData().get("errors.error[0].Source"), "System")

        #test errors[0].reasoncode case insensitive
        with self.assertRaises(APIException) as cm:
            content = self.controller.handleResponse(response,{"errors" :[{"source":"System", "reasoncode":"SYSTEM_ERROR1", "description":"Unknown Error1", "recoverable":"false"}]})
            
        self.assertEqual(cm.exception.getHttpStatus(), 301)
        self.assertEqual(cm.exception.getMessage(), "Unknown Error1")
        self.assertEqual(cm.exception.getReasonCode(), "SYSTEM_ERROR1")
        self.assertEqual(cm.exception.getSource(), "System")
        self.assertEqual(cm.exception.getRawErrorData().get("errors[0].Source"), "System")

        #test [].readonCode 
        with self.assertRaises(APIException) as cm:
            content = self.controller.handleResponse(response,[ {"source":"System", "reasoncode":"SYSTEM_ERROR1", "description":"Unknown Error1", "recoverable":"false"}])
            
        self.assertEqual(cm.exception.getHttpStatus(), 301)
        self.assertEqual(cm.exception.getMessage(), "Unknown Error1")
        self.assertEqual(cm.exception.getReasonCode(), "SYSTEM_ERROR1")
        self.assertEqual(cm.exception.getSource(), "System")
        self.assertEqual(cm.exception.getRawErrorData().get("source"), "System")
        


        response.status_code = 400
        with self.assertRaises(APIException) as cm:
                content = self.controller.handleResponse(response,{"Errors" :{"Error":{"message":"Some error"}}})
                
        self.assertEqual(cm.exception.getHttpStatus(), 400)
        self.assertEqual(cm.exception.getMessage(), "Bad Request")
        self.assertEqual(cm.exception.getReasonCode(), None)
        self.assertEqual(cm.exception.getSource(), None)
        

        response.status_code = 401
        with self.assertRaises(APIException) as cm:
            content = self.controller.handleResponse(response,{"Errors" :{"Error":{"message":"Some error"}}})

        self.assertEqual(cm.exception.getHttpStatus(), 401)
        self.assertEqual(cm.exception.getMessage(), "Unauthorized")
        self.assertEqual(cm.exception.getReasonCode(), None)
        self.assertEqual(cm.exception.getSource(), None)

        response.status_code = 403
        with self.assertRaises(APIException) as cm:
            content = self.controller.handleResponse(response,{"Errors" :{"Error":{"message":"Some error"}}})
                
        self.assertEqual(cm.exception.getHttpStatus(), 403)
        self.assertEqual(cm.exception.getMessage(), "Forbidden")
        self.assertEqual(cm.exception.getReasonCode(), None)

        response.status_code = 404
        with self.assertRaises(APIException) as cm:
                content = self.controller.handleResponse(response,{"Errors" :{"Error":{"message":"Some error"}}})
                
        self.assertEqual(cm.exception.getHttpStatus(), 404)
        self.assertEqual(cm.exception.getMessage(), "Not Found")
        self.assertEqual(cm.exception.getReasonCode(), None)
        self.assertEqual(cm.exception.getSource(), None)

        response.status_code = 405
        with self.assertRaises(APIException) as cm:
                content = self.controller.handleResponse(response,{"Errors" :{"Error":{"message":"Some error"}}})

        self.assertEqual(cm.exception.getHttpStatus(), 405)
        self.assertEqual(cm.exception.getMessage(), "Method Not Allowed")
        self.assertEqual(cm.exception.getReasonCode(), None)
        self.assertEqual(cm.exception.getSource(), None)
        
        response.status_code = 500
        with self.assertRaises(APIException) as cm:
                content = self.controller.handleResponse(response,{"Errors" :{"Error":{"message":"Some error"}}})

        self.assertEqual(cm.exception.getHttpStatus(), 500)
        self.assertEqual(cm.exception.getMessage(), "Internal Server Error")
        self.assertEqual(cm.exception.getReasonCode(), None)
        self.assertEqual(cm.exception.getSource(), None)
        
        
        response.status_code = 500
        with self.assertRaises(APIException) as cm:
                content = self.controller.handleResponse(response, {"errors":[{"source":"OpenAPIClientId","reasonCode":"AUTHORIZATION_FAILED","key":"050007","description":"Unauthorized Access","recoverable":False,"requestId":None,"details":{"details":[{"name":"ErrorDetailCode","value":"050007"}]}}]})

        self.assertEqual(cm.exception.getHttpStatus(), 500)
        self.assertEqual(cm.exception.getMessage(), "Unauthorized Access")
        self.assertEqual(cm.exception.getReasonCode(), "AUTHORIZATION_FAILED")
        self.assertEqual(cm.exception.getSource(), "OpenAPIClientId")
        self.assertEqual(cm.exception.getRawErrorData().get("errors[0].source"), "OpenAPIClientId")
        self.assertEqual(cm.exception.getRawErrorData().get("Errors[0].Source"), "OpenAPIClientId")
        self.assertEqual(cm.exception.getError().get("details.details[0].name"), "ErrorDetailCode")



if __name__ == '__main__':
    unittest.main()