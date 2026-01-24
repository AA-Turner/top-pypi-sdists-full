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
authres extension module for the RFC 5617 DKIM/ADSP authentication method.
"""

#MODULE = 'authres'

__author__  = 'Scott Kitterman, Julian Mehnle'
__email__   = 'scott@kitterman.com'

import authres.core
from authres.core import make_result_class_properties

class DKIMADSPAuthenticationResult(authres.core.AuthenticationResult):
    "DKIM ADSP (RFC 5617) result clause of an ``Authentication-Results`` header"

    METHOD = 'dkim-adsp'

    def __init__(self, version = None,
        result               = None,  result_comment               = None,
        reason               = None,  reason_comment               = None,
        properties = None,
        header_from          = None,  header_from_comment          = None
    ):
        authres.core.AuthenticationResult.__init__(self, self.METHOD, version,
            result, result_comment, reason, reason_comment, properties)
        if header_from:                  self.header_from                  = header_from
        if header_from_comment:          self.header_from_comment          = header_from_comment

    header_from,          header_from_comment          = make_result_class_properties('header', 'from')

RESULT_CLASSES = [
    DKIMADSPAuthenticationResult
]

# vim:sw=4 sts=4
