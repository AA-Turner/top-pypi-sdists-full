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


class RotateSecret(object):
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
        'rotate_all_services_boolean': 'bool',
        'json': 'bool',
        'name': 'str',
        'rotate_all_services': 'str',
        'token': 'str',
        'uid_token': 'str'
    }

    attribute_map = {
        'rotate_all_services_boolean': 'RotateAllServicesBoolean',
        'json': 'json',
        'name': 'name',
        'rotate_all_services': 'rotate-all-services',
        'token': 'token',
        'uid_token': 'uid-token'
    }

    def __init__(self, rotate_all_services_boolean=None, json=False, name=None, rotate_all_services='false', token=None, uid_token=None, local_vars_configuration=None):  # noqa: E501
        """RotateSecret - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._rotate_all_services_boolean = None
        self._json = None
        self._name = None
        self._rotate_all_services = None
        self._token = None
        self._uid_token = None
        self.discriminator = None

        if rotate_all_services_boolean is not None:
            self.rotate_all_services_boolean = rotate_all_services_boolean
        if json is not None:
            self.json = json
        self.name = name
        if rotate_all_services is not None:
            self.rotate_all_services = rotate_all_services
        if token is not None:
            self.token = token
        if uid_token is not None:
            self.uid_token = uid_token

    @property
    def rotate_all_services_boolean(self):
        """Gets the rotate_all_services_boolean of this RotateSecret.  # noqa: E501


        :return: The rotate_all_services_boolean of this RotateSecret.  # noqa: E501
        :rtype: bool
        """
        return self._rotate_all_services_boolean

    @rotate_all_services_boolean.setter
    def rotate_all_services_boolean(self, rotate_all_services_boolean):
        """Sets the rotate_all_services_boolean of this RotateSecret.


        :param rotate_all_services_boolean: The rotate_all_services_boolean of this RotateSecret.  # noqa: E501
        :type: bool
        """

        self._rotate_all_services_boolean = rotate_all_services_boolean

    @property
    def json(self):
        """Gets the json of this RotateSecret.  # noqa: E501

        Set output format to JSON  # noqa: E501

        :return: The json of this RotateSecret.  # noqa: E501
        :rtype: bool
        """
        return self._json

    @json.setter
    def json(self, json):
        """Sets the json of this RotateSecret.

        Set output format to JSON  # noqa: E501

        :param json: The json of this RotateSecret.  # noqa: E501
        :type: bool
        """

        self._json = json

    @property
    def name(self):
        """Gets the name of this RotateSecret.  # noqa: E501

        Secret name (Rotated Secret or Custom Dynamic Secret)  # noqa: E501

        :return: The name of this RotateSecret.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this RotateSecret.

        Secret name (Rotated Secret or Custom Dynamic Secret)  # noqa: E501

        :param name: The name of this RotateSecret.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def rotate_all_services(self):
        """Gets the rotate_all_services of this RotateSecret.  # noqa: E501

        Rotate all associated services  # noqa: E501

        :return: The rotate_all_services of this RotateSecret.  # noqa: E501
        :rtype: str
        """
        return self._rotate_all_services

    @rotate_all_services.setter
    def rotate_all_services(self, rotate_all_services):
        """Sets the rotate_all_services of this RotateSecret.

        Rotate all associated services  # noqa: E501

        :param rotate_all_services: The rotate_all_services of this RotateSecret.  # noqa: E501
        :type: str
        """

        self._rotate_all_services = rotate_all_services

    @property
    def token(self):
        """Gets the token of this RotateSecret.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this RotateSecret.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this RotateSecret.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this RotateSecret.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def uid_token(self):
        """Gets the uid_token of this RotateSecret.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this RotateSecret.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this RotateSecret.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this RotateSecret.  # noqa: E501
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
        if not isinstance(other, RotateSecret):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RotateSecret):
            return True

        return self.to_dict() != other.to_dict()
