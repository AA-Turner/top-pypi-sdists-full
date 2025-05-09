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


class SshBastionSessionTermination(object):
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
        'api_password': 'str',
        'api_token': 'str',
        'api_url': 'str',
        'api_username': 'str',
        'enabled': 'bool'
    }

    attribute_map = {
        'api_password': 'api_password',
        'api_token': 'api_token',
        'api_url': 'api_url',
        'api_username': 'api_username',
        'enabled': 'enabled'
    }

    def __init__(self, api_password=None, api_token=None, api_url=None, api_username=None, enabled=None, local_vars_configuration=None):  # noqa: E501
        """SshBastionSessionTermination - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._api_password = None
        self._api_token = None
        self._api_url = None
        self._api_username = None
        self._enabled = None
        self.discriminator = None

        if api_password is not None:
            self.api_password = api_password
        if api_token is not None:
            self.api_token = api_token
        if api_url is not None:
            self.api_url = api_url
        if api_username is not None:
            self.api_username = api_username
        if enabled is not None:
            self.enabled = enabled

    @property
    def api_password(self):
        """Gets the api_password of this SshBastionSessionTermination.  # noqa: E501


        :return: The api_password of this SshBastionSessionTermination.  # noqa: E501
        :rtype: str
        """
        return self._api_password

    @api_password.setter
    def api_password(self, api_password):
        """Sets the api_password of this SshBastionSessionTermination.


        :param api_password: The api_password of this SshBastionSessionTermination.  # noqa: E501
        :type: str
        """

        self._api_password = api_password

    @property
    def api_token(self):
        """Gets the api_token of this SshBastionSessionTermination.  # noqa: E501


        :return: The api_token of this SshBastionSessionTermination.  # noqa: E501
        :rtype: str
        """
        return self._api_token

    @api_token.setter
    def api_token(self, api_token):
        """Sets the api_token of this SshBastionSessionTermination.


        :param api_token: The api_token of this SshBastionSessionTermination.  # noqa: E501
        :type: str
        """

        self._api_token = api_token

    @property
    def api_url(self):
        """Gets the api_url of this SshBastionSessionTermination.  # noqa: E501


        :return: The api_url of this SshBastionSessionTermination.  # noqa: E501
        :rtype: str
        """
        return self._api_url

    @api_url.setter
    def api_url(self, api_url):
        """Sets the api_url of this SshBastionSessionTermination.


        :param api_url: The api_url of this SshBastionSessionTermination.  # noqa: E501
        :type: str
        """

        self._api_url = api_url

    @property
    def api_username(self):
        """Gets the api_username of this SshBastionSessionTermination.  # noqa: E501


        :return: The api_username of this SshBastionSessionTermination.  # noqa: E501
        :rtype: str
        """
        return self._api_username

    @api_username.setter
    def api_username(self, api_username):
        """Sets the api_username of this SshBastionSessionTermination.


        :param api_username: The api_username of this SshBastionSessionTermination.  # noqa: E501
        :type: str
        """

        self._api_username = api_username

    @property
    def enabled(self):
        """Gets the enabled of this SshBastionSessionTermination.  # noqa: E501


        :return: The enabled of this SshBastionSessionTermination.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this SshBastionSessionTermination.


        :param enabled: The enabled of this SshBastionSessionTermination.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

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
        if not isinstance(other, SshBastionSessionTermination):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SshBastionSessionTermination):
            return True

        return self.to_dict() != other.to_dict()
