#!/usr/bin/env python
# -*- coding: utf-8 -*-#

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


class User(BaseObject):
    """
    
    """

    __config = {
        "3d1d0857-7e73-4534-99be-52134515f40a" : OperationConfig("/mock_crud_server/users", "list", [], []),
        "25cf4d3e-3606-433c-8fcc-1df3813d28d5" : OperationConfig("/mock_crud_server/users", "create", [], []),
        "7bd54cb3-740a-46a8-ba73-a7116d7fbfa5" : OperationConfig("/mock_crud_server/users/{id}", "read", [], []),
        "fe79f3e0-b05d-44e9-a8e4-6f08dbb99964" : OperationConfig("/mock_crud_server/users/{id}", "update", [], []),
        "32f3baaa-9757-4f56-9ed1-241756206274" : OperationConfig("/mock_crud_server/users/{id}", "delete", [], []),
        "ff6f7de7-08fe-4dc2-8185-1f838dc96197" : OperationConfig("/mock_crud_server/users200/{id}", "delete", [], []),
        "7223cecd-203a-47b7-85cb-3ddbf9027f33" : OperationConfig("/mock_crud_server/users204/{id}", "delete", [], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUI)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata("0.0.1", "http://localhost:8081")



    @classmethod
    def listByCriteria(cls,criteria=None):
        """
        List objects of type User

        @param Dict criteria
        @return Array of User object matching the criteria.
        """

        if not criteria :
            return BaseObject.execute("3d1d0857-7e73-4534-99be-52134515f40a", User())
        else:
            return BaseObject.execute("3d1d0857-7e73-4534-99be-52134515f40a", User(criteria))



    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type User

        @param Dict mapObj, containing the required parameters to create a new object
        @return User of the response of created instance.
        """
        return BaseObject.execute("25cf4d3e-3606-433c-8fcc-1df3813d28d5", User(mapObj))











    @classmethod
    def read(cls,id,criteria=None):
        """
        Returns objects of type User by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of User
        """
        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if criteria:
            if (isinstance(criteria,RequestMap)):
                mapObj.setAll(criteria.getObject())
            else:
                mapObj.setAll(criteria)

        return BaseObject.execute("7bd54cb3-740a-46a8-ba73-a7116d7fbfa5", User(mapObj))



    def update(self):
        """
        Updates an object of type User

        @return User object representing the response.
        """
        return BaseObject.execute("fe79f3e0-b05d-44e9-a8e4-6f08dbb99964", self)








    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type User by id

        @param str id
        @return User of the response of the deleted instance.
        """

        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if map:
            if (isinstance(map,RequestMap)):
                mapObj.setAll(map.getObject())
            else:
                mapObj.setAll(map)

        return BaseObject.execute("32f3baaa-9757-4f56-9ed1-241756206274", User(mapObj))


    def delete(self):
        """
        Delete object of type User

        @return User of the response of the deleted instance.
        """
        return BaseObject.execute("32f3baaa-9757-4f56-9ed1-241756206274", self)






    @classmethod
    def delete200ById(cls,id,map=None):
        """
        Delete object of type User by id

        @param str id
        @return User of the response of the deleted instance.
        """

        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if map:
            if (isinstance(map,RequestMap)):
                mapObj.setAll(map.getObject())
            else:
                mapObj.setAll(map)

        return BaseObject.execute("ff6f7de7-08fe-4dc2-8185-1f838dc96197", User(mapObj))


    def delete200(self):
        """
        Delete object of type User

        @return User of the response of the deleted instance.
        """
        return BaseObject.execute("ff6f7de7-08fe-4dc2-8185-1f838dc96197", self)






    @classmethod
    def delete204ById(cls,id,map=None):
        """
        Delete object of type User by id

        @param str id
        @return User of the response of the deleted instance.
        """

        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if map:
            if (isinstance(map,RequestMap)):
                mapObj.setAll(map.getObject())
            else:
                mapObj.setAll(map)

        return BaseObject.execute("7223cecd-203a-47b7-85cb-3ddbf9027f33", User(mapObj))


    def delete204(self):
        """
        Delete object of type User

        @return User of the response of the deleted instance.
        """
        return BaseObject.execute("7223cecd-203a-47b7-85cb-3ddbf9027f33", self)




