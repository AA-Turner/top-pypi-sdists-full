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
from builtins import str
from builtins import object
from mastercardapicore.core.config import Config
from .authentication import Authentication
from OpenSSL import crypto

from . import util as SecurityUtil
import mastercardapicore.core.util as util
import collections


class OAuthAuthentication(Authentication):
    """
    Implementation of OAuth Authentication to generate the OAuth Header
    """
    def __init__(self,clientId, privateKey, alias, password):

        self._clientId   = clientId
        self._privateKey = privateKey
        self._alias      = alias
        self._password   = password

    def getClientId(self):
        return self._clientId

    def getPrivateKey(self):
        return self._privateKey

    def signRequest(self,uri,request):
        """
        Generates the OAuth header for the request, adds the header to the request and returns the request object
        """
        oauth_key = self.getOAuthKey(uri,request.method,request.data,request.params)
        request.headers[OAuthParameters.AUTHORIZATION] = oauth_key
        return request

    def getOAuthBaseParameters(self,url, method, body):
        oAuthParameters = OAuthParameters()
        oAuthParameters.setOAuthConsumerKey(self._clientId)
        oAuthParameters.setOAuthNonce(SecurityUtil.getNonce())
        oAuthParameters.setOAuthTimestamp(SecurityUtil.getTimestamp())
        oAuthParameters.setOAuthSignatureMethod("RSA-SHA256")
        oAuthParameters.setOAuthVersion("1.0")
        if method != "GET" and method != "DELETE" and method != "HEAD"  :
            encodedHash = util.base64Encode(util.sha256Encode(body))
            oAuthParameters.setOAuthBodyHash(encodedHash)

        return oAuthParameters

    def getBaseString(self,url, method,params, oAuthParams):
        #Merge the query string parameters
        mergeParams = params.copy()
        mergeParams.update(oAuthParams)
        return "{}&{}&{}".format(util.uriRfc3986Encode(method.upper()),util.uriRfc3986Encode(util.normalizeUrl(url)),util.uriRfc3986Encode(util.normalizeParams(url, mergeParams)))

    def getOAuthKey(self,url,method,body,params):
        #Get all the base parameters such as nonce and timestamp
        oAuthBaseParameters = self.getOAuthBaseParameters(url,method,body)
        #Get the base string
        baseString = self.getBaseString(url, method, params,oAuthBaseParameters.getBaseParametersDict())
        #Sign the base string using the private key
        signature = self.signMessage(baseString)

        #Set the signature in the Base parameters
        oAuthBaseParameters.setOAuthSignature(signature)

        #Get the updated base parameteres dict
        oAuthBaseParametersDict = oAuthBaseParameters.getBaseParametersDict()

        #Generate the header value for OAuth Header
        oauth_key = OAuthParameters.OAUTH_KEY+" "+",".join([util.uriRfc3986Encode(str(key))+"=\""+util.uriRfc3986Encode(str(value))+"\"" for (key,value) in oAuthBaseParametersDict.items()])
        return oauth_key




    def signMessage(self,message):
        """
            Signs the message using the private key with sha1 as digest
        """
        privateKeyFile = open(self._privateKey, 'rb')
        try:
            p12 = crypto.load_pkcs12(privateKeyFile.read(), self._password.encode("utf-8"))
            privateKey = p12.get_privatekey()
            sign = crypto.sign(privateKey,message.encode("utf-8"),'SHA256')
            privateKeyFile.close()
            return util.base64Encode(sign)
        except:
            privateKeyFile.close()
            raise Exception("Error Reading the key file")


class OAuthParameters(object):
    """
    Stores the OAuth parameters required to generate the Base String and Headers constants
    """

    OAUTH_BODY_HASH_KEY = "oauth_body_hash"
    OAUTH_CALLBACK_KEY = "oauth_callback"
    OAUTH_CONSUMER_KEY = "oauth_consumer_key"
    OAUTH_CONSUMER_SECRET = "oauth_consumer_secret"
    OAUTH_NONCE_KEY = "oauth_nonce"
    OAUTH_KEY = "OAuth"
    AUTHORIZATION = "Authorization"
    OAUTH_SIGNATURE_KEY = "oauth_signature"
    OAUTH_SIGNATURE_METHOD_KEY = "oauth_signature_method"
    OAUTH_TIMESTAMP_KEY = "oauth_timestamp"
    OAUTH_TOKEN_KEY = "oauth_token"
    OAUTH_TOKEN_SECRET_KEY = "oauth_token_secret"
    OAUTH_VERIFIER_KEY = "oauth_verifier"
    REALM_KEY = "realm"
    XOAUTH_REQUESTOR_ID_KEY = "xoauth_requestor_id"
    OAUTH_VERSION = "oauth_version"

    def __init__(self):
        self.baseParameters = {}

    def put(self,key, value):
        self.baseParameters[key] = value

    def setOAuthConsumerKey(self,consumerKey):
        self.put(OAuthParameters.OAUTH_CONSUMER_KEY, consumerKey)

    def setOAuthNonce(self,oAuthNonce):
        self.put(OAuthParameters.OAUTH_NONCE_KEY, oAuthNonce)

    def setOAuthTimestamp(self,timestamp):
        self.put(OAuthParameters.OAUTH_TIMESTAMP_KEY, timestamp)

    def setOAuthSignatureMethod(self,signatureMethod):
        self.put(OAuthParameters.OAUTH_SIGNATURE_METHOD_KEY, signatureMethod)

    def setOAuthSignature(self,signature):
        self.put(OAuthParameters.OAUTH_SIGNATURE_KEY, signature)

    def setOAuthBodyHash(self,bodyHash):
        self.put(OAuthParameters.OAUTH_BODY_HASH_KEY, bodyHash)

    def setOAuthVersion(self,version):
        self.put(OAuthParameters.OAUTH_VERSION, version)

    def getBaseParametersDict(self):
        return self.baseParameters
