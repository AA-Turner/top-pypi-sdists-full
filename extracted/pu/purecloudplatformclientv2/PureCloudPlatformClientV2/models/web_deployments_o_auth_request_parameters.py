# coding: utf-8

"""
Copyright 2016 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from datetime import datetime
from datetime import date
from pprint import pformat
import re
import json

from ..utils import sanitize_for_serialization

# type hinting support
from typing import TYPE_CHECKING
from typing import List
from typing import Dict


class WebDeploymentsOAuthRequestParameters(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self) -> None:
        """
        WebDeploymentsOAuthRequestParameters - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'code': 'str',
            'redirect_uri': 'str',
            'nonce': 'str',
            'max_age': 'int',
            'code_verifier': 'str',
            'iss': 'str'
        }

        self.attribute_map = {
            'code': 'code',
            'redirect_uri': 'redirectUri',
            'nonce': 'nonce',
            'max_age': 'maxAge',
            'code_verifier': 'codeVerifier',
            'iss': 'iss'
        }

        self._code = None
        self._redirect_uri = None
        self._nonce = None
        self._max_age = None
        self._code_verifier = None
        self._iss = None

    @property
    def code(self) -> str:
        """
        Gets the code of this WebDeploymentsOAuthRequestParameters.
        The authorization code to be sent to the authentication server during the token request.  Refer to https://openid.net/specs/openid-connect-core-1_0.html#AuthRequest

        :return: The code of this WebDeploymentsOAuthRequestParameters.
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code: str) -> None:
        """
        Sets the code of this WebDeploymentsOAuthRequestParameters.
        The authorization code to be sent to the authentication server during the token request.  Refer to https://openid.net/specs/openid-connect-core-1_0.html#AuthRequest

        :param code: The code of this WebDeploymentsOAuthRequestParameters.
        :type: str
        """
        

        self._code = code

    @property
    def redirect_uri(self) -> str:
        """
        Gets the redirect_uri of this WebDeploymentsOAuthRequestParameters.
        Redirect URI sent in the \"Authentication Request\"Refer to https://openid.net/specs/openid-connect-core-1_0.html#AuthRequest

        :return: The redirect_uri of this WebDeploymentsOAuthRequestParameters.
        :rtype: str
        """
        return self._redirect_uri

    @redirect_uri.setter
    def redirect_uri(self, redirect_uri: str) -> None:
        """
        Sets the redirect_uri of this WebDeploymentsOAuthRequestParameters.
        Redirect URI sent in the \"Authentication Request\"Refer to https://openid.net/specs/openid-connect-core-1_0.html#AuthRequest

        :param redirect_uri: The redirect_uri of this WebDeploymentsOAuthRequestParameters.
        :type: str
        """
        

        self._redirect_uri = redirect_uri

    @property
    def nonce(self) -> str:
        """
        Gets the nonce of this WebDeploymentsOAuthRequestParameters.
        Required if provided in the \"Authentication Request\". Otherwise should be empty.String value used to associate a Client session with an ID Token, and to mitigate replay attacks. The value is passed through unmodified from the Authentication Request to the ID Token. Refer to https://openid.net/specs/openid-connect-core-1_0.html#AuthRequest

        :return: The nonce of this WebDeploymentsOAuthRequestParameters.
        :rtype: str
        """
        return self._nonce

    @nonce.setter
    def nonce(self, nonce: str) -> None:
        """
        Sets the nonce of this WebDeploymentsOAuthRequestParameters.
        Required if provided in the \"Authentication Request\". Otherwise should be empty.String value used to associate a Client session with an ID Token, and to mitigate replay attacks. The value is passed through unmodified from the Authentication Request to the ID Token. Refer to https://openid.net/specs/openid-connect-core-1_0.html#AuthRequest

        :param nonce: The nonce of this WebDeploymentsOAuthRequestParameters.
        :type: str
        """
        

        self._nonce = nonce

    @property
    def max_age(self) -> int:
        """
        Gets the max_age of this WebDeploymentsOAuthRequestParameters.
        Required if provided in the  \"Authentication Request\". Otherwise should be empty.Specifies the allowable elapsed time in seconds since the last time the End-User was actively authenticated.Refer to https://openid.net/specs/openid-connect-core-1_0.html#AuthRequest

        :return: The max_age of this WebDeploymentsOAuthRequestParameters.
        :rtype: int
        """
        return self._max_age

    @max_age.setter
    def max_age(self, max_age: int) -> None:
        """
        Sets the max_age of this WebDeploymentsOAuthRequestParameters.
        Required if provided in the  \"Authentication Request\". Otherwise should be empty.Specifies the allowable elapsed time in seconds since the last time the End-User was actively authenticated.Refer to https://openid.net/specs/openid-connect-core-1_0.html#AuthRequest

        :param max_age: The max_age of this WebDeploymentsOAuthRequestParameters.
        :type: int
        """
        

        self._max_age = max_age

    @property
    def code_verifier(self) -> str:
        """
        Gets the code_verifier of this WebDeploymentsOAuthRequestParameters.
        Required if authorizing using Proof Key for Code Exchange (PKCE). Otherwise should be empty.Random URL-safe string with a minimum length of 43 characters generated at start of authorization flow to mitigate the threat of having the authorization code intercepted. Refer to https://datatracker.ietf.org/doc/html/rfc7636

        :return: The code_verifier of this WebDeploymentsOAuthRequestParameters.
        :rtype: str
        """
        return self._code_verifier

    @code_verifier.setter
    def code_verifier(self, code_verifier: str) -> None:
        """
        Sets the code_verifier of this WebDeploymentsOAuthRequestParameters.
        Required if authorizing using Proof Key for Code Exchange (PKCE). Otherwise should be empty.Random URL-safe string with a minimum length of 43 characters generated at start of authorization flow to mitigate the threat of having the authorization code intercepted. Refer to https://datatracker.ietf.org/doc/html/rfc7636

        :param code_verifier: The code_verifier of this WebDeploymentsOAuthRequestParameters.
        :type: str
        """
        

        self._code_verifier = code_verifier

    @property
    def iss(self) -> str:
        """
        Gets the iss of this WebDeploymentsOAuthRequestParameters.
        Optional parameter. Set it if authorization server discovery metadata authorization_response_iss_parameter_supported is enabled. Refer to https://datatracker.ietf.org/doc/html/rfc9207

        :return: The iss of this WebDeploymentsOAuthRequestParameters.
        :rtype: str
        """
        return self._iss

    @iss.setter
    def iss(self, iss: str) -> None:
        """
        Sets the iss of this WebDeploymentsOAuthRequestParameters.
        Optional parameter. Set it if authorization server discovery metadata authorization_response_iss_parameter_supported is enabled. Refer to https://datatracker.ietf.org/doc/html/rfc9207

        :param iss: The iss of this WebDeploymentsOAuthRequestParameters.
        :type: str
        """
        

        self._iss = iss

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in self.swagger_types.items():
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_json(self):
        """
        Returns the model as raw JSON
        """
        return json.dumps(sanitize_for_serialization(self.to_dict()))

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

