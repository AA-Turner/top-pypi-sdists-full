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


from mastercardapicore import RequestMap
from mastercardapicore import BaseObject
from mastercardapicore import OperationConfig
from mastercardapicore import OperationMetadata


class MultiplePathUserPost(BaseObject):
    """
    
    """

    __config = {
        "96c94c4d-fe46-4a70-96d2-ee0227a4690f" : OperationConfig("/mock_crud_server/users/{user_id}/post/{post_id}", "list", [], []),
        "1f153175-4a49-4cd2-bfb2-a949351dab10" : OperationConfig("/mock_crud_server/users/{user_id}/post/{post_id}", "update", [], ["testQuery"]),
        "7d0317ff-5d7d-427b-abd2-9df62d5becb7" : OperationConfig("/mock_crud_server/users/{user_id}/post/{post_id}", "delete", [], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata("0.0.1", "http://localhost:8081")




    @classmethod
    def listByCriteria(cls,criteria=None):
        """
        List objects of type MultiplePathUserPost

        @param Dict criteria
        @return Array of MultiplePathUserPost object matching the criteria.
        """

        if not criteria :
            return BaseObject.execute("96c94c4d-fe46-4a70-96d2-ee0227a4690f", MultiplePathUserPost())
        else:
            return BaseObject.execute("96c94c4d-fe46-4a70-96d2-ee0227a4690f", MultiplePathUserPost(criteria))





    def update(self):
        """
        Updates an object of type MultiplePathUserPost

        @return MultiplePathUserPost object representing the response.
        """
        return BaseObject.execute("1f153175-4a49-4cd2-bfb2-a949351dab10", self)








    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type MultiplePathUserPost by id

        @param str id
        @return MultiplePathUserPost of the response of the deleted instance.
        """

        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if map:
            if (isinstance(map,RequestMap)):
                mapObj.setAll(map.getObject())
            else:
                mapObj.setAll(map)

        return BaseObject.execute("7d0317ff-5d7d-427b-abd2-9df62d5becb7", MultiplePathUserPost(mapObj))


    def delete(self):
        """
        Delete object of type MultiplePathUserPost

        @return MultiplePathUserPost of the response of the deleted instance.
        """
        return BaseObject.execute("7d0317ff-5d7d-427b-abd2-9df62d5becb7", self)




