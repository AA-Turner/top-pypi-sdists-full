# coding: utf-8

# Copyright © 2012-2013 Julian Mehnle <julian@mehnle.net>,
# Copyright © 2012-2014 Scott Kitterman <scott@kitterman.com>
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
authres extension module for the RFC 7281, Authentication-Results Registration
for S/MIME Signature Verification authentication method.
"""

#MODULE = 'authres'

__author__  = 'Scott Kitterman, Julian Mehnle'
__email__   = 'scott@kitterman.com'

import authres.core
from authres.core import make_result_class_properties

class SMIMEAuthenticationResult(authres.core.AuthenticationResult):
    """
    S/MIME (RFC 7281, Authentication-Results Registration
    for S/MIME Signature Verification) result clause of an
    ``Authentication-Results`` header"""

    METHOD = 'smime'

    def __init__(self, version = None,
        result                = None,  result_comment                 = None,
        reason                = None,  reason_comment                 = None,
        properties = None,
        body_smime_identifier = None,  body_smime_identifier_comment  = None,
        body_smime_part       = None,  body_smime_part_comment        = None,
        body_smime_serial     = None,  body_smime_serial_comment      = None,
        body_smime_issuer     = None,  body_smime_issuer_comment      = None
        
    ):
        authres.core.AuthenticationResult.__init__(self, self.METHOD, version,
            result, result_comment, reason, reason_comment, properties)

        if body_smime_identifier:            self.body_smime_identifier            = body_smime_identifier
        if body_smime_identifier_comment:    self.body_smime_identifier_comment    = body_smime_identifier_comment
        if body_smime_part:                  self.body_smime_part                  = body_smime_part
        if body_smime_part_comment:          self.body_smime_part_comment          = body_smime_part_comment
        if body_smime_serial:                self.body_smime_serial                = body_smime_serial
        if body_smime_serial_comment:        self.body_smime_serial_comment        = body_smime_serial_comment
        if body_smime_issuer:                self.body_smime_issuer                = body_smime_issuer
        if body_smime_issuer_comment:        self.body_smime_issuer_comment        = body_smime_issuer_comment

        # RFC 7281 Section 3.2.3
        if body_smime_serial and not body_smime_issuer:
            raise AuthResError('body.smime-serial present, but body.smime-issuer missing.')
        if  not body_smime_serial and body_smime_issuer:
            raise AuthResError('body.smime-issuer present, but body.smime-serial missing.')

    body_smime_identifier,      body_smime_identifier_comment      = make_result_class_properties('body', 'smime-identifier')
    body_smime_part,            body_smime_part_comment            = make_result_class_properties('body', 'smime-part')
    body_smime_serial,          body_smime_serial_comment          = make_result_class_properties('body', 'smime-serial')
    body_smime_issuer,          body_smime_issuer_comment          = make_result_class_properties('body', 'smime-issuer')


RESULT_CLASSES = [
    SMIMEAuthenticationResult
]

# vim:sw=4 sts=4
