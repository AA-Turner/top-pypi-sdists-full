# coding: utf-8

# Copyright © 2011-2013 Julian Mehnle <julian@mehnle.net>,
# Copyright © 2011-2013 Scott Kitterman <scott@kitterman.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Package for parsing ``Authentication-Results`` headers as defined in RFC
5451/7001/7601/8601.  Optional support for authentication methods defined in
RFCs 5617, 6008, 6212, 7281, and 8617.

Examples:
RFC 5451 B.2
>>> str(AuthenticationResultsHeader('test.example.org'))
'Authentication-Results: test.example.org; none'

RFC 5451 B.3
>>> str(AuthenticationResultsHeader(authserv_id = 'example.com',
... results = [SPFAuthenticationResult(result = 'pass',
... smtp_mailfrom = 'example.net')]))
'Authentication-Results: example.com; spf=pass smtp.mailfrom=example.net'

RFC 5451 B.4(1)
>>> str(AuthenticationResultsHeader(authserv_id = 'example.com',
... results = [SMTPAUTHAuthenticationResult(result = 'pass', result_comment = 'cram-md5',
... smtp_auth = 'sender@example.net'), SPFAuthenticationResult(result = 'pass',
... smtp_mailfrom = 'example.net')]))
'Authentication-Results: example.com; auth=pass (cram-md5) smtp.auth=sender@example.net; spf=pass smtp.mailfrom=example.net'

RFC 5451 B.4(2)
>>> str(AuthenticationResultsHeader(authserv_id = 'example.com',
... results = [SenderIDAuthenticationResult(result = 'pass',
... header_from = 'example.com')]))
'Authentication-Results: example.com; sender-id=pass header.from=example.com'

RFC 5451 B.5(1) # Note: RFC 5451 uses 'hardfail' instead of 'fail' for
SPF failures. Hardfail is deprecated.  See RFC 6577.
Examples here use the correct 'fail'. The authres module does not
validate result codes, so either will be processed.

>>> str(AuthenticationResultsHeader(authserv_id = 'example.com',
... results = [SenderIDAuthenticationResult(result = 'fail',
... header_from = 'example.com'), DKIMAuthenticationResult(result = 'pass',
... header_i = 'sender@example.com', result_comment = 'good signature')]))
'Authentication-Results: example.com; sender-id=fail header.from=example.com; dkim=pass (good signature) header.i=sender@example.com'

# Missing parsing header comment.
#FIXME
>>> arobj = AuthenticationResultsHeader.parse('Authentication-Results: example.com; sender-id=fail header.from=example.com; dkim=pass (good signature) header.i=sender@example.com')
>>> str(arobj.authserv_id)
'example.com'
>>> str(arobj.results[0])
'sender-id=fail header.from=example.com'
>>> str(arobj.results[0].method)
'sender-id'
>>> str(arobj.results[0].result)
'fail'
>>> str(arobj.results[0].header_from)
'example.com'
>>> str(arobj.results[0].properties[0].type)
'header'
>>> str(arobj.results[0].properties[0].name)
'from'
>>> str(arobj.results[0].properties[0].value)
'example.com'
>>> str(arobj.results[1])
'dkim=pass header.i=sender@example.com'
>>> str(arobj.results[1].method)
'dkim'
>>> str(arobj.results[1].result)
'pass'
>>> str(arobj.results[1].header_i)
'sender@example.com'
>>> str(arobj.results[1].properties[0].type)
'header'
>>> str(arobj.results[1].properties[0].name)
'i'
>>> str(arobj.results[1].properties[0].value)
'sender@example.com'
"""

MODULE = 'authres'

__author__  = 'Julian Mehnle, Scott Kitterman'
__email__   = 'julian@mehnle.net'
__version__ = '1.2.0'

import authres.core

# Backward compatibility: For the benefit of user modules referring to authres.…:
from authres.core import *

# FeatureContext class & convenience methods
###############################################################################

class FeatureContext(object):
    """
    Class representing a "feature context" for the ``authres`` package.
    A feature context is a collection of extension modules that may override
    the core AuthenticationResultsHeader class or result classes, or provide
    additional result classes for new authentication methods.

    To instantiate a feature context, import the desired ``authres.…`` extension
    modules and pass them to ``FeatureContext()``.

    A ``FeatureContext`` object provides ``parse``, ``parse_value``, ``header``,
    and ``result`` methods specific to the context's feature set.
    """

    def __init__(self, *modules):
        self.header_class                = authres.core.AuthenticationResultsHeader
        self.result_class_by_auth_method = {}

        modules = [authres.core] + list(modules)
        for module in modules:
            try:
                self.header_class = module.AuthenticationResultsHeader
            except AttributeError:
                # Module does not provide new AuthenticationResultsHeader class.
                pass

            try:
                for result_class in module.RESULT_CLASSES:
                    self.result_class_by_auth_method[result_class.METHOD] = result_class
            except AttributeError:
                # Module does not provide AuthenticationResult subclasses.
                pass

    def parse(self, string):
        return self.header_class.parse(self, string)

    def parse_value(self, string):
        return self.header_class.parse_value(self, string)

    def header(self,
        authserv_id = None,  authserv_id_comment = None,
        version     = None,  version_comment     = None,
        results     = None
    ):
        return self.header_class(
            self, authserv_id, authserv_id_comment, version, version_comment, results)

    def result(self, method, version = None,
        result = None, result_comment = None,
        reason = None, reason_comment = None,
        properties = None
    ):
        try:
            return self.result_class_by_auth_method[method](version,
                result, result_comment, reason, reason_comment, properties)
        except KeyError:
            return authres.core.AuthenticationResult(method, version,
                result, result_comment, reason, reason_comment, properties)

_core_features = None
def core_features():
    "Returns default feature context providing only RFC 5451 core features."
    global _core_features
    if not _core_features:
        _core_features = FeatureContext()
    return _core_features

_all_features = None
def all_features():
    """
    Returns default feature context providing all features shipped with the
    ``authres`` package.
    """
    global _all_features
    if not _all_features:
        import authres.dkim_b
        import authres.dkim_adsp
        import authres.vbr
        import authres.dmarc
        import authres.smime
        import authres.rrvs
        import authres.arc        
        _all_features = FeatureContext(
            authres.dkim_b,
            authres.dkim_adsp,
            authres.vbr,
            authres.dmarc,
            authres.smime,
            authres.rrvs,
            authres.arc
        )
    return _all_features

# Simple API with implicit core-features-only context
###############################################################################

class AuthenticationResultsHeader(authres.core.AuthenticationResultsHeader):
    @classmethod
    def parse(self, string):
        return authres.core.AuthenticationResultsHeader.parse(core_features(), string)

    @classmethod
    def parse_value(self, string):
        return authres.core.AuthenticationResultsHeader.parse_value(core_features(), string)

    def __init__(self,
        authserv_id = None,  authserv_id_comment = None,
        version     = None,  version_comment     = None,
        results     = None
    ):
        authres.core.AuthenticationResultsHeader.__init__(self,
            core_features(), authserv_id, authserv_id_comment, version, version_comment, results)

def result(method, version = None,
    result = None, result_comment = None,
    reason = None, reason_comment = None,
    properties = None
):
    return core_features().result(method, version,
        result, result_comment, reason, reason_comment, properties)

def header(
    authserv_id = None,  authserv_id_comment = None,
    version     = None,  version_comment     = None,
    results     = None
):
    return core_features().header(
        authserv_id, authserv_id_comment, version, version_comment, results)

def parse(string):
    return core_features().parse(string)

def parse_value(string):
    return core_features().parse_value(string)

# vim:sw=4 sts=4
