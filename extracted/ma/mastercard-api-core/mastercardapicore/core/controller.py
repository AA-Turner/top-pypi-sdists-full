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
from __future__ import print_function
from builtins import object
from requests import Request, Session
from mastercardapicore.core.config import Config
from mastercardapicore.core.constants import Constants
from mastercardapicore.security import Authentication
from mastercardapicore.core.exceptions import APIException
from mastercardapicore.core import util
import json

class APIController(object):


    ACTION_CREATE = "CREATE"
    ACTION_DELETE = "DELETE"
    ACTION_UPDATE = "UPDATE"
    ACTION_READ   = "READ"
    ACTION_LIST   = "LIST"
    ACTION_QUERY  = "QUERY"

    HTTP_METHOD_GET    = "GET"
    HTTP_METHOD_POST   = "POST"
    HTTP_METHOD_PUT    = "PUT"
    HTTP_METHOD_DELETE = "DELETE"

    KEY_ID     = "id"
    KEY_FORMAT = "Format"
    KEY_ACCEPT = "Accept"
    KEY_USER_AGENT = "User-Agent"
    KEY_CONTENT_TYPE = "Content-Type"
    APPLICATION_JSON = "application/json; charset=UTF-8"
    JSON             = "JSON"





    def __check(self):
        """
        Check the pre-conditions before execute can be called
        """

        if Config.getAuthentication() is None or not isinstance(Config.getAuthentication(),Authentication):
            raise  APIException("No or incorrect authentication has been configured")
        

    def removeForwardSlashFromTail(self,text):
        """
        Removes the trailing / from url if any and returns the url
        """
        return text[:-1] if text.endswith("/") else text

    def getURL(self,config,metadata,inputMap):
        """
        Forms the complete URL by combining baseURL and replaced path variables in resourcePath from inputMap
        """

        resourcePath = config.getResourcePath()
        action= config.getAction()
        baseURL = metadata.getHost()
      
        if baseURL: 
            if not util.validateURL(baseURL):
                raise APIException("URL: '" + baseURL + "' is not a valid url")
        else:
            raise APIException("URL: '' is not a valid url")
        
        #Remove the Trailing slash from base URL
        baseURL = self.removeForwardSlashFromTail(baseURL)

        #Remove the Trailing slash from the resource path
        resourcePath = self.removeForwardSlashFromTail(resourcePath)
        
        #arizzini: we need to set the environment variable in the resourcepath
        if "#env" in resourcePath:
            environment = ""
            if metadata.getEnvironment():
                environment = metadata.getEnvironment()
            resourcePath = resourcePath.replace("#env", environment)
            resourcePath = resourcePath.replace("//", "/")
            
        #Combine the  base URL and the path
        fullURL = baseURL + resourcePath

        #Replace the path variables
        fullURL = util.getReplacedPath(fullURL,inputMap)

        #This step is if id is in inputMap but was not specified in URL as /{id}
        #If the action is read,update or delete we add this id
        #if APIController.KEY_ID in inputMap:
            #if action.upper() in [APIController.ACTION_READ,APIController.ACTION_UPDATE,APIController.ACTION_DELETE]:
                #fullURL += "/"+str(inputMap[APIController.KEY_ID])
                #del inputMap[APIController.KEY_ID] #Remove from input path otherwise this would get add in query params as well

        return fullURL

    def addQueryParamter(self, inputDic, outputDic):

        for (key, value) in inputDic.items():
            if (isinstance(value, list) or isinstance(value, dict)): 
                #value = json.dumps(value, encoding='utf-8')
                value = json.dumps(value)
            outputDic[key] = value;  



    def getRequestObject(self,config,metadata,inputMap):
        """
        Gets the Request Object with URL and
        """
        
        #Separate the headers from the inputMap
        headerMap = util.subMap(inputMap,config.getHeaderParams())

        #Separate the query from the inputMap
        queryMap  = util.subMap(inputMap,config.getQueryParams())
        
        #Extract the action
        action = config.getAction()
        
        #getting the url
        fullURL = self.getURL(config,metadata,inputMap)

        #get method from action
        method  = self.getMethod(action)        

        if method is None:
            raise APIException("Invalid action supplied: " + action);

        #Create the request object
        request = Request()

        #calculate the contentTypeOverride
        contentType = APIController.APPLICATION_JSON
        if (metadata.getContentTypeOverride()):
            contentType = metadata.getContentTypeOverride() + "; charset=UTF-8"


        #set the Method and URL
        request.method = method
        request.url    = fullURL

        #Add inputMap to params if action in read,delete,list,query
        if action.upper() in [APIController.ACTION_READ,APIController.ACTION_DELETE,APIController.ACTION_LIST,APIController.ACTION_QUERY]:
            self.addQueryParamter(inputMap, queryMap)
            
        # else is is a body if not null
        elif action.upper() in [APIController.ACTION_CREATE,APIController.ACTION_UPDATE]:
            if inputMap:
                #request.data = json.dumps(inputMap, encoding='utf-8')
                request.data = json.dumps(inputMap)
            else: 
                request.data = ""

        request.headers[APIController.KEY_ACCEPT]       = contentType
        if request.data: 
            request.headers[APIController.KEY_CONTENT_TYPE] = contentType
        request.headers[APIController.KEY_USER_AGENT]   = Constants.getCoreVersion()+"/"+metadata.getVersion()

        #Set the query parameter Format as JSON
        if metadata.isJsonNative() is False :
            request.params[APIController.KEY_FORMAT] = APIController.JSON

        #Add the query in queryMap
        request.params.update(queryMap)
        
        #Add headers
        for (key, value) in headerMap.items():
            request.headers[key] = value

        #Sign the request
        #This should add the authorization header in the request
        if (Config.getAuthentication()):
            Config.getAuthentication().signRequest(fullURL,request)

        return request
    
    def getMethod(self,action):

        actions = {
            APIController.ACTION_CREATE:APIController.HTTP_METHOD_POST,
            APIController.ACTION_DELETE:APIController.HTTP_METHOD_DELETE,
            APIController.ACTION_UPDATE:APIController.HTTP_METHOD_PUT,
            APIController.ACTION_READ:APIController.HTTP_METHOD_GET,
            APIController.ACTION_LIST:APIController.HTTP_METHOD_GET,
            APIController.ACTION_QUERY:APIController.HTTP_METHOD_GET
        }

        return actions.get(action.upper(),None)

    def execute(self,config,metadata,inputMap):

        #Check preconditions for execute
        self.__check()

        request = self.getRequestObject(config,metadata,inputMap)
        prepreq = request.prepare()

        ##Log the request parameters if Debug is on
        if Config.isDebug():
            print("------ Request ----")
            print("")
            print("URL")
            print(prepreq.url)
            print("")
            print("Headers")
            print(prepreq.headers)
            print("")
            print("Body")
            print(prepreq.body)
            print(" ")


        #Make the request
        sess = Session()
        response = sess.send(prepreq, proxies=Config.getProxy(), timeout=(Config.getConnectionTimeout(), Config.getReadTimeout()))
        sess.close()

        ##Log the response parameters if Debug is on
        if Config.isDebug():
            print("------ Response ----")
            print("")
            print("Status Code")
            print(response.status_code)
            print("")
            print("Headers")
            print(response.headers)
            print("")
            print("Body")
            print(response.content)
            print(" ")

        content = response.content

        return self.handleResponse(response,content)


    def handleResponse(self,response,content):
        """
        Handles the exception and response
        """
        status = response.status_code
        if content:
            try:
                if isinstance(content,bytes):
                    content = content.decode("utf-8")
                content= json.loads(content, encoding='utf-8')
            except (ValueError, TypeError):
                pass

        else:
             content= ""

        if 200 <= status <= 299:
            return content
        else:
            raise APIException("Internal Server Error",status,content)
