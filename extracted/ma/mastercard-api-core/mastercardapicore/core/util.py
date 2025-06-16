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
Utility file having common functions for MasterCard Core SDK
"""

from future import standard_library
standard_library.install_aliases()
from builtins import str
import re
import hashlib
import base64


try:
    from urllib.parse import urlparse, parse_qsl #Python 2.x
    from urllib.parse import quote, quote_plus
except ImportError: #Python 3
    from urllib.parse import urlparse, quote, quote_plus, parse_qsl
def validateURL(url):
    """
    Validates that the given string is a valid URL
    """
    urlRegex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if urlRegex.match(url):
        return True
    return False

def normalizeParams(url,params):
    """
    Combines the query parameters of url and extra params into a single queryString.
    All the query string parameters are lexicographically sorted
    """
    #parse the url
    parse = urlparse(url)

    #Get the query list
    qs_dict = parse_qsl(parse.query)
    #convert the list to dict
    qs_dict = dict(qs_dict)
    #Combine the two dictionaries
    if params is None:
        combined_dict = qs_dict
    else:
        combined_dict = qs_dict.copy()
        combined_dict.update(params)
    #,quote(value if isinstance(value,bytes) else str(value)) -- This part means that for bytes we pass as it is else we convert to string
    return "&".join(['%s=%s' % (uriRfc3986Encode(key),uriRfc3986Encode(value if isinstance(value,bytes) else str(value))) for (key,value) in sorted(combined_dict.items())])

def normalizeUrl(url):
    """
    Removes the query parameters from the URL
    """
    parse = urlparse(url)
    return "{}://{}{}".format(parse.scheme,parse.netloc,parse.path)

def uriRfc3986Encode(value):
    """
    RFC 3986 encodes the value
    """
    encoded = quote_plus(value)
    encoded = str.replace(encoded, '+', '%20')
    encoded = str.replace(encoded, '*', '%2A')
    encoded = str.replace(encoded, '~', '%7E')
    return encoded


def sha1Encode(text):
    """
    Returns the digest of SHA-1 of the text
    """
    return hashlib.sha1(str(text).encode('utf-8')).digest()

def sha256Encode(text):
    """
    Returns the digest of SHA-1 of the text
    """
    return hashlib.sha256(str(text).encode('utf-8')).digest()

def base64Encode(text):
    """
    Base64 encodes the given input
    """
    #text = text.encode('ascii')
    encode = base64.b64encode(text)
    if isinstance(encode, (bytearray, bytes)):
        return encode.decode('ascii')
    else:
        return encode

def subMap(inputMap,keyList):
    """
    Returns a dict containing key, value from inputMap for keys in keyList
    Matched keys are removed from inputMap
    """
    subMap = {}
    for key in keyList:
        if key in inputMap:
            subMap[key] = inputMap[key]
            del inputMap[key]
    return subMap

def getReplacedPath(path,inputMap):
    """
    Replaces the {var} variables in path with value from inputMap
    The replaced values are removed from inputPath

    >>> getReplacedPath("http://localhost:8080/{var1}/car",{"var1" => 1})
        "http://localhost:8080/1/car"

    """
    pathRegex = re.compile("{(.*?)}")
    matches = pathRegex.findall(path)

    for match in matches:
        try:
            path = path.replace("{"+match+"}",str(inputMap[match]))
            del inputMap[match]
        except KeyError as k:
            raise KeyError("path parameter: "+match+" expected but not found in input map")

    return path
