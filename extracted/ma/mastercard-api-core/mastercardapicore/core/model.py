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
from builtins import str
from past.builtins import basestring
from builtins import object
import re
from collections import OrderedDict
import json

################################################################################
# SmartMap
################################################################################

class SmartMap(object):

    KEY_LIST = "list"

    def __init__(self):

        self.__properties = OrderedDict()
        self.parentWithSquareBracket = re.compile("\[(.*)\]")

    def _moveInList(self,key,match):
        """
        Moves in the subMap, if key is of type for eg key[1] and match matches [1]
        Raises exception if either key is not in map or map.key is not a list or map.key[1] does not exist
        """

        arr_key = match.group(0)[1:-1]
        txt_key = key[0:match.start(0)]
        #If text part of the key is not part of map
        if txt_key not in self.__subProperty:
            raise Exception("Invalid Key "+txt_key)

        #Else Move inside
        self.__subProperty = self.__subProperty[txt_key]

        #Check if arr_key is an integer
        try:
            arr_key = int(arr_key)
        except ValueError:
            #If not integer then raise exception
            raise Exception("Invalid key index "+arr_key)

        #Check if subProperty is a list and index exists in that list
        if isinstance(self.__subProperty,list) and arr_key < len(self.__subProperty):
            #If list and list index exists then move to the index
            self.__subProperty = self.__subProperty[arr_key]
        else:
            #Else raise an exception
            raise Exception("Invalid key index "+str(arr_key))


    def _handleListTypeKeys(self,key,match,value):
        """
        Handles the keys of type key[0]
        """
        #Creates a new list if key does not exist else moves to keys
        #Adds the value at the poistion index for key[index]
        #if index == len of list then appends
        #if index > len then throw exception

        #Get the array index
        arr_key = match.group(0)[1:-1]

        #Get the text key
        txt_key = key[0:match.start(0)]

        try:
            arr_key = int(arr_key)
        except ValueError:
            raise KeyError("Key "+arr_key+" is not an integer")



        #If key does not exist
        if txt_key not in self.__subProperty:
            #If the arr_key is not integer or not zero
            if arr_key != 0 :
                #Raise Exception
                raise TypeError("Invalid Key error")

            #Else add key as a list
            self.__subProperty[txt_key] = []

            #Move the sub_property in it
            self.__subProperty = self.__subProperty[txt_key]
            #Append the value
            self.__subProperty.append(value)
            #Move ine the array
            self.__subProperty = self.__subProperty[arr_key]
        else:#If the txt_key exists in map
            #move in the map
            self.__subProperty = self.__subProperty[txt_key]

            try:
                if value == OrderedDict(): #If value is OrderedDict() then we just want to move in the dict
                    self.__subProperty = self.__subProperty[arr_key]
                else: # This means that this is the last key and value need to be set
                    self.__subProperty[int(arr_key)] = value
            #This means that index arr_key does not exist in the list
            except IndexError as ie:
                #if index is same as length then append
                if len(self.__subProperty) == arr_key:
                    self.__subProperty.append(value)
                    self.__subProperty = self.__subProperty[arr_key]
                else:
                    raise IndexError("List only has "+len(self.__subProperty)+" elements. Cannot add at position "+arr_key)

    def _createMap(self,key):

        match = self.parentWithSquareBracket.search(key)
        #If it is a type of key[0]
        if match is not None:
            self._handleListTypeKeys(key,match,OrderedDict())
        else: #if it does not have [] like key1
            if key not in self.__subProperty:
                if isinstance(self.__subProperty,OrderedDict):
                    self.__subProperty[key] = OrderedDict()
                else:
                    raise TypeError("Invalid Key String : Cannot override value "+str(self.__subProperty))

            self.__subProperty = self.__subProperty[key]



    def set(self,key,value):
        """
        Sets the value of the key as value
        """
        #Get the list of keys
        keys = key.split(".")
        #Number of Keys
        keys_len = len(keys)
        #Copy the __properties in __subProperty so we can walk over it
        self.__subProperty = self.__properties
        count = 0
        for part_key in keys:
            count +=1
            #If we are at the final key, then we need to set this key for __subProperty
            if count == keys_len:
                match = self.parentWithSquareBracket.search(part_key)
                if match is not None:
                    self._handleListTypeKeys(part_key,match,value)

                else:#Set the value
                    self.__subProperty[part_key] = value
            else:
                #Else walk inside the __subProperty[part_key]
                self._createMap(part_key)

        return self.__properties

    def getObject(self):
        """
        Returns the requestMap internal object
        """
        return self.__properties

    def get(self,key):
        """
        Gets the value from the map associated with the key
        """

        #Get the list of keys
        keys = key.split(".")
        #Number of Keys
        keys_len = len(keys)

        #Copy the __properties in __subProperty so we can walk over it
        self.__subProperty = self.__properties

        count = 0

        #Iterate over the keys
        for part_key in keys:

            count +=1

            #check if the key is of form key[0]
            match = self.parentWithSquareBracket.search(part_key)
            #if the final key is of form key[0]
            if match is not None:
                try:
                    self._moveInList(part_key,match)
                except Exception:
                    return None
                #If this is the last key
                if count == keys_len:
                    return self.__subProperty
            else: # Move in the map
                if isinstance(self.__subProperty,dict) and part_key in self.__subProperty:
                    if count == keys_len:
                        if isinstance(self.__subProperty[part_key], basestring) :
                            return self.__subProperty[part_key]
                        else: 
                            return self.__subProperty[part_key]
                    else:
                        self.__subProperty = self.__subProperty[part_key]
                else:
                    return None


    def __iterateItemsAndAdd(self,map,combKey):
        """
        Iterate over the items in the map object and adds them to basemap object
        """
        #The implementation is more of a depth first search
        #For a given object for eg {"user":"name":{"first":"naman","last":"aggarwal",roll:[4,3,6]}}
        #It reaches to a lowest level and keeps track of the key, in this case user.name.first and then
        #uses set function to set the value self.set("user.name.first","naman")
        #For list it uses index as keys, for eg user.name.roll[0] = 4

        #Check if it object is  a dict
        if isinstance(map,dict):
            for (key,value) in map.items():
                #if last combined is not empty then append current key to it else use current key
                tempKey = combKey +"."+key if combKey != "" else key
                #call the function again with one level down and combined key
                self.__iterateItemsAndAdd(map[key],tempKey)
        #If the object is a list , for eg roll:[1,2,3] (combKey will be user.name for this case)
        elif isinstance(map,list):
            count = 0
            # Iterate over each value
            for value in map:
                #create the temp key with the current index
                tempKey = combKey+"["+str(count)+"]"
                #call the function again with one level lower and combined key
                self.__iterateItemsAndAdd(value,tempKey)
                count+=1
        #If its any other object then set the key to that value
        else:
            self.set(combKey,map)

    def size(self):
        """
        Returns the number of keys at the first level of the object
        """
        return len(self.__properties)

    def parseJson(self,jsonString):
        """
        Uses the Json String to create the base map object
        """
        map = json.loads(jsonString, encoding='utf-8')
        self.setAll(map)



    def setAll(self,map):
        """
        Uses the map object to create the base map object
        """

        initialKey = ""

        #If given object is a list then the created map should have a key called list first
        if isinstance(map,list):
            initialKey = RequestMap.KEY_LIST

        #Iterate over the object and keeps on adding the items to the properties object
        self.__iterateItemsAndAdd(map,initialKey)

        return self.__properties


    def containsKey(self,key):
        """
        Check if map contains the key
        """
        if self.get(key) is not None:
            return True
        return False

################################################################################
# CaseInsensitiveSmartMap
################################################################################

class CaseInsensitiveSmartMap(SmartMap):

    def containsKey(self,key):
        return super(CaseInsensitiveSmartMap, self).containsKey(key.lower())

    def get(self,key):
        return super(CaseInsensitiveSmartMap, self).get(key.lower())

    def setAll(self,map):
        properties = self._parseMap(map)
        super(CaseInsensitiveSmartMap, self).setAll(properties)

    def set(self,key,value):
        super(CaseInsensitiveSmartMap, self).set(key.lower(),value)

    def _parseMap(self,aMap):
        result = {}
        for (key, value) in aMap.items(): 
            if (isinstance(value, dict)):
                result[key.lower()] = self._parseMap(value)
            elif (isinstance(value, list)):
                result[key.lower()] = self._parseList(value)
            else:
                result[key.lower()] = value
        return result
    
    def _parseList(self,aList):
        result = []
        for value in aList:
            if (isinstance(value, dict)):
                result.append(self._parseMap(value))
            elif (isinstance(value, list)):
                result.append(self._parseList(value))
            else:
                result.append(value)
        return result

    

################################################################################
# RequestMap (Alias to SmartMap)
################################################################################

RequestMap = SmartMap


################################################################################
# OperationConfig
################################################################################

class OperationConfig(object):
    def __init__(self,resourcePath,action,headerParams,queryParams):
        self.resourcePath = resourcePath
        self.action = action
        self.headerParams = headerParams
        self.queryParams = queryParams
        
    def getResourcePath(self):
        return self.resourcePath
    
    def getAction(self):
        return self.action

    def getHeaderParams(self):
        return self.headerParams
    
    def getQueryParams(self):
        return self.queryParams

################################################################################
# OperationMetadata
################################################################################

class OperationMetadata(object):
    def __init__(self,version,host,environment=None,jsonNative=False,contentTypeOverride=False):
        self.version = version
        self.host = host
        self.environment = environment
        self.jsonNative = jsonNative
        self.contentTypeOverride = contentTypeOverride
        
    def getVersion(self):
        return self.version
    
    def getHost(self):
        return self.host
    
    def getEnvironment(self):
        return self.environment
    
    def isJsonNative(self):
        return self.jsonNative

    def getContentTypeOverride(self):
        return self.contentTypeOverride


