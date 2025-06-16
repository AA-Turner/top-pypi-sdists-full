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

"""
Config File for MasterCard APIs Core SDK
"""

from builtins import object
from mastercardapicore.core.constants import Environment

class Config(object):
    """
    Configurable options for MasterCard APIs Core SDK
    """

    environment     = Environment.SANDBOX
    debug           = False
    authentication  = None
    registeredInstances = {}
    proxy           = {}
    connection_timeout   = 5
    read_timeout         = 30

    def __init__(self):
        pass

    @classmethod
    def setDebug(cls,debug):
        cls.debug = debug

    @classmethod
    def isDebug(cls):
        return cls.debug

    @classmethod
    def setSandbox(cls, sandbox):
        if sandbox :
            cls.setEnvironment(Environment.SANDBOX)
        else:
            cls.setEnvironment(Environment.PRODUCTION)

    @classmethod
    def setProxy(cls, proxy):
        cls.proxy = proxy

    @classmethod
    def getProxy(cls):
        return cls.proxy

    @classmethod
    def getReadTimeout(cls):
        return cls.read_timeout

    @classmethod
    def setReadTimeout(cls, timeout):
        if timeout :
            cls.read_timeout = timeout
        else:
            cls.read_timeout = 30

    @classmethod
    def getConnectionTimeout(cls):
        return cls.connection_timeout

    @classmethod
    def setConnectionTimeout(cls, timeout):
        if timeout :
            cls.connection_timeout = timeout
        else:
            cls.connection_timeout = 5

    @classmethod
    def isSandbox(cls):
        return cls.environment == Environment.SANDBOX

    @classmethod
    def setAuthentication(cls,authentication):
        cls.authentication = authentication

    @classmethod
    def getAuthentication(cls):
        return cls.authentication

    @classmethod
    def setEnvironment(cls,environment):
        if environment:
            cls.environment = environment
            for registeredInstance in list(cls.registeredInstances.values()):
                registeredInstance.setEnvironment(environment)
            
            
    @classmethod
    def getEnvironment(cls):
        return cls.environment    
    
    @classmethod
    def registerResourceConfig(cls,resourceConfig):
        className = resourceConfig.getName()
        if not className in list(cls.registeredInstances.keys()):
            cls.registeredInstances[className] = resourceConfig

    @classmethod
    def clearResourceConfig(cls):
        cls.registeredInstances = {}
