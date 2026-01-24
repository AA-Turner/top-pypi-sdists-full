# coding: utf-8

# Copyright © 2012-2013 Julian Mehnle <julian@mehnle.net>,
# Copyright © 2012-2015 Scott Kitterman <scott@kitterman.com>
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
authres extension module for RFC 7293, The Require-Recipient-Valid-Since
    Header Field and SMTP Service Extension, header field type.
"""

#MODULE = 'authres'

__author__  = 'Scott Kitterman, Julian Mehnle'
__email__   = 'scott@kitterman.com'

import authres.core
from authres.core import make_result_class_properties

class RRVSAuthenticationResult(authres.core.AuthenticationResult):
    "RRVS (RFC 7293) result clause of an ``Authentication-Results`` header"

    METHOD = 'rrvs'

    def __init__(self, version = None,
        result               = None,  result_comment               = None,
        reason               = None,  reason_comment               = None,
        properties = None,
        smtp_rrvs            = None,  smtp_rrvs_comment            = None
    ):
        authres.core.AuthenticationResult.__init__(self, self.METHOD, version,
            result, result_comment, reason, reason_comment, properties)
        if smtp_rrvs:                    self.smtp_rrvs                    = smtp_rrvs
        if smtp_rrvs_comment:            self.smtp_rrvs_comment            = smtp_rrvs_comment

    smtp_rrvs,            smtp_rrvs_comment            = make_result_class_properties('smtp', 'rrvs')

RESULT_CLASSES = [
    RRVSAuthenticationResult
]

# vim:sw=4 sts=4
