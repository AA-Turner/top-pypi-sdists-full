# -*- coding: utf-8 -*-
"""Identity Services Engine patchAuthorizationprofileId data model.

Copyright (c) 2021 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from __future__ import absolute_import, division, print_function, unicode_literals

import json
from builtins import *

import fastjsonschema
from ciscoisesdk.exceptions import MalformedRequest


class JSONSchemaValidatorCf54BCfca54Ff8300D01Df5F56Daf(object):
    """patchAuthorizationprofileId request schema definition."""
    def __init__(self):
        super(JSONSchemaValidatorCf54BCfca54Ff8300D01Df5F56Daf, self).__init__()
        self._validator = fastjsonschema.compile(json.loads(
            '''{
                "$schema": "http://json-schema.org/draft-04/schema#",
                "properties": {
                "AuthorizationProfile": {
                "properties": {
                "accessType": {
                "type": "string"
                },
                "acl": {
                "type": "string"
                },
                "advancedAttributes": {
                "properties": {
                "leftHandSideDictionaryAttribue": {
                "properties": {
                "attributeName": {
                "type": "string"
                },
                "dictionaryName": {
                "type": "string"
                }
                }
                },
                "rightHandSideAttribueValue": {
                "type": "object"
                }
                }
                },
                "agentlessPosture": {
                "type": "object"
                },
                "airespaceACL": {
                "type": "string"
                },
                "airespaceIPv6ACL": {
                "type": "string"
                },
                "asaVpn": {
                "type": "string"
                },
                "authzProfileType": {
                "type": "string"
                },
                "autoSmartPort": {
                "type": "string"
                },
                "avcProfile": {
                "type": "string"
                },
                "daclName": {
                "type": "string"
                },
                "description":
                 {
                "type": "string"
                },
                "easywiredSessionCandidate": {
                "type": "object"
                },
                "id": {
                "type": "string"
                },
                "interfaceTemplate": {
                "type": "string"
                },
                "ipv6ACLFilter": {
                "type": "string"
                },
                "ipv6DaclName": {
                "type": "string"
                },
                "macSecPolicy": {
                "type": "string"
                },
                "name": {
                "type": "string"
                },
                "neat": {
                "type": "object"
                },
                "profileName": {
                "type": "string"
                },
                "reauth": {
                "properties": {
                "attributeName": {
                "type": "string"
                },
                "connectivity": {
                "type": "string"
                },
                "dictionaryName": {
                "type": "string"
                },
                "reauthType": {
                "type": "string"
                },
                "timer": {
                "type": "object"
                }
                }
                },
                "serviceTemplate": {
                "type": "object"
                },
                "trackMovement": {
                "type": "object"
                },
                "uniqueIdentifier": {
                "type": "string"
                },
                "vlan": {
                "properties": {
                "nameID": {
                "type": "string"
                },
                "tagID": {
                "type": "number"
                }
                }
                },
                "voiceDomainPermission": {
                "type": "object"
                },
                "webAuth": {
                "type": "object"
                },
                "webRedirection": {
                "properties": {
                "ACL": {
                "type": "string"
                },
                "WebRedirectionType": {
                "type": "string"
                },
                "displayCertificatesRenewalMessages": {
                "type": "boolean"
                },
                "portalName": {
                "type": "string"
                },
                "staticIPHostNameFQDN": {
                "type": "string"
                }
                }
                }
                }
                }
                },
                "required": [
                "AuthorizationProfile"
                ],
                "type": "object"
                }'''.replace("\n" + ' ' * 16, '')
        ))

    def validate(self, request):
        try:
            self._validator(request)
        except fastjsonschema.exceptions.JsonSchemaException as e:
            raise MalformedRequest(
                '{} is invalid. Reason: {}'.format(request, e.message)
            )
