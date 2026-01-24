# coding: utf-8

# Copyright © 2012-2013 Julian Mehnle <julian@mehnle.net>,
# Copyright © 2012-2013 Scott Kitterman <scott@kitterman.com>
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
authres extension module for RFC 6008 DKIM signature identification (header.b).
"""

#MODULE = 'authres'

__author__  = 'Scott Kitterman, Julian Mehnle'
__email__   = 'scott@kitterman.com'

import authres.core
from authres.core import make_result_class_properties

class DKIMAuthenticationResult(authres.core.DKIMAuthenticationResult):
    "DKIM result clause of an ``Authentication-Results`` header"

    def __init__(self, version = None,
        result               = None,  result_comment               = None,
        reason               = None,  reason_comment               = None,
        properties = None,
        header_d             = None,  header_d_comment             = None,
        header_i             = None,  header_i_comment             = None,
        header_b             = None,  header_b_comment             = None
    ):
        authres.core.DKIMAuthenticationResult.__init__(self, version,
            result, result_comment, reason, reason_comment, properties,
            header_d, header_d_comment, header_i, header_i_comment)
        if header_b:                     self.header_b                     = header_b
        if header_b_comment:             self.header_b_comment             = header_b_comment

    header_b,             header_b_comment             = make_result_class_properties('header', 'b')

    def match_signature(self, signature_d, signature_b = None, strict = False):
        """Match authentication result against a DKIM signature by ``header.d``
        and, if available, ``header.b``, per RFC 6008, section 4
        <https://tools.ietf.org/html/rfc6008#section-4>.  If ``header.b`` is
        absent from the authentication result, a non-strict match succeeds,
        whereas a strict match fails."""

        if self.header_d != signature_d:
            return False
        if self.header_b is None:
            return not strict
        if len(self.header_b) >= 8:
            # Require prefix match:
            return signature_b.startswith(self.header_b)
        else:
            # Require exact match:
            return self.header_b == signature_b

RESULT_CLASSES = [
    DKIMAuthenticationResult
]

# vim:sw=4 sts=4
