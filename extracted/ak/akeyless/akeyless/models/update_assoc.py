# coding: utf-8

"""
    Akeyless API

    The purpose of this application is to provide access to Akeyless API.  # noqa: E501

    The version of the OpenAPI document: 3.0
    Contact: support@akeyless.io
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from akeyless.configuration import Configuration


class UpdateAssoc(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'assoc_id': 'str',
        'case_sensitive': 'str',
        'json': 'bool',
        'sub_claims': 'dict(str, str)',
        'token': 'str',
        'uid_token': 'str'
    }

    attribute_map = {
        'assoc_id': 'assoc-id',
        'case_sensitive': 'case-sensitive',
        'json': 'json',
        'sub_claims': 'sub-claims',
        'token': 'token',
        'uid_token': 'uid-token'
    }

    def __init__(self, assoc_id=None, case_sensitive='true', json=False, sub_claims=None, token=None, uid_token=None, local_vars_configuration=None):  # noqa: E501
        """UpdateAssoc - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._assoc_id = None
        self._case_sensitive = None
        self._json = None
        self._sub_claims = None
        self._token = None
        self._uid_token = None
        self.discriminator = None

        self.assoc_id = assoc_id
        if case_sensitive is not None:
            self.case_sensitive = case_sensitive
        if json is not None:
            self.json = json
        if sub_claims is not None:
            self.sub_claims = sub_claims
        if token is not None:
            self.token = token
        if uid_token is not None:
            self.uid_token = uid_token

    @property
    def assoc_id(self):
        """Gets the assoc_id of this UpdateAssoc.  # noqa: E501

        The association id to be updated  # noqa: E501

        :return: The assoc_id of this UpdateAssoc.  # noqa: E501
        :rtype: str
        """
        return self._assoc_id

    @assoc_id.setter
    def assoc_id(self, assoc_id):
        """Sets the assoc_id of this UpdateAssoc.

        The association id to be updated  # noqa: E501

        :param assoc_id: The assoc_id of this UpdateAssoc.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and assoc_id is None:  # noqa: E501
            raise ValueError("Invalid value for `assoc_id`, must not be `None`")  # noqa: E501

        self._assoc_id = assoc_id

    @property
    def case_sensitive(self):
        """Gets the case_sensitive of this UpdateAssoc.  # noqa: E501

        Treat sub claims as case-sensitive [true/false]  # noqa: E501

        :return: The case_sensitive of this UpdateAssoc.  # noqa: E501
        :rtype: str
        """
        return self._case_sensitive

    @case_sensitive.setter
    def case_sensitive(self, case_sensitive):
        """Sets the case_sensitive of this UpdateAssoc.

        Treat sub claims as case-sensitive [true/false]  # noqa: E501

        :param case_sensitive: The case_sensitive of this UpdateAssoc.  # noqa: E501
        :type: str
        """

        self._case_sensitive = case_sensitive

    @property
    def json(self):
        """Gets the json of this UpdateAssoc.  # noqa: E501

        Set output format to JSON  # noqa: E501

        :return: The json of this UpdateAssoc.  # noqa: E501
        :rtype: bool
        """
        return self._json

    @json.setter
    def json(self, json):
        """Sets the json of this UpdateAssoc.

        Set output format to JSON  # noqa: E501

        :param json: The json of this UpdateAssoc.  # noqa: E501
        :type: bool
        """

        self._json = json

    @property
    def sub_claims(self):
        """Gets the sub_claims of this UpdateAssoc.  # noqa: E501

        key/val of sub claims, e.g group=admins,developers  # noqa: E501

        :return: The sub_claims of this UpdateAssoc.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._sub_claims

    @sub_claims.setter
    def sub_claims(self, sub_claims):
        """Sets the sub_claims of this UpdateAssoc.

        key/val of sub claims, e.g group=admins,developers  # noqa: E501

        :param sub_claims: The sub_claims of this UpdateAssoc.  # noqa: E501
        :type: dict(str, str)
        """

        self._sub_claims = sub_claims

    @property
    def token(self):
        """Gets the token of this UpdateAssoc.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this UpdateAssoc.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this UpdateAssoc.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this UpdateAssoc.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def uid_token(self):
        """Gets the uid_token of this UpdateAssoc.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this UpdateAssoc.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this UpdateAssoc.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this UpdateAssoc.  # noqa: E501
        :type: str
        """

        self._uid_token = uid_token

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, UpdateAssoc):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpdateAssoc):
            return True

        return self.to_dict() != other.to_dict()
