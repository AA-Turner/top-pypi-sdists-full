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


class CreateGroup(object):
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
        'description': 'str',
        'group_alias': 'str',
        'json': 'bool',
        'name': 'str',
        'token': 'str',
        'uid_token': 'str',
        'user_assignment': 'str'
    }

    attribute_map = {
        'description': 'description',
        'group_alias': 'group-alias',
        'json': 'json',
        'name': 'name',
        'token': 'token',
        'uid_token': 'uid-token',
        'user_assignment': 'user-assignment'
    }

    def __init__(self, description=None, group_alias=None, json=False, name=None, token=None, uid_token=None, user_assignment=None, local_vars_configuration=None):  # noqa: E501
        """CreateGroup - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._description = None
        self._group_alias = None
        self._json = None
        self._name = None
        self._token = None
        self._uid_token = None
        self._user_assignment = None
        self.discriminator = None

        if description is not None:
            self.description = description
        self.group_alias = group_alias
        if json is not None:
            self.json = json
        self.name = name
        if token is not None:
            self.token = token
        if uid_token is not None:
            self.uid_token = uid_token
        if user_assignment is not None:
            self.user_assignment = user_assignment

    @property
    def description(self):
        """Gets the description of this CreateGroup.  # noqa: E501

        Description of the object  # noqa: E501

        :return: The description of this CreateGroup.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CreateGroup.

        Description of the object  # noqa: E501

        :param description: The description of this CreateGroup.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def group_alias(self):
        """Gets the group_alias of this CreateGroup.  # noqa: E501

        A short group alias  # noqa: E501

        :return: The group_alias of this CreateGroup.  # noqa: E501
        :rtype: str
        """
        return self._group_alias

    @group_alias.setter
    def group_alias(self, group_alias):
        """Sets the group_alias of this CreateGroup.

        A short group alias  # noqa: E501

        :param group_alias: The group_alias of this CreateGroup.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and group_alias is None:  # noqa: E501
            raise ValueError("Invalid value for `group_alias`, must not be `None`")  # noqa: E501

        self._group_alias = group_alias

    @property
    def json(self):
        """Gets the json of this CreateGroup.  # noqa: E501

        Set output format to JSON  # noqa: E501

        :return: The json of this CreateGroup.  # noqa: E501
        :rtype: bool
        """
        return self._json

    @json.setter
    def json(self, json):
        """Sets the json of this CreateGroup.

        Set output format to JSON  # noqa: E501

        :param json: The json of this CreateGroup.  # noqa: E501
        :type: bool
        """

        self._json = json

    @property
    def name(self):
        """Gets the name of this CreateGroup.  # noqa: E501

        Group name  # noqa: E501

        :return: The name of this CreateGroup.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateGroup.

        Group name  # noqa: E501

        :param name: The name of this CreateGroup.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def token(self):
        """Gets the token of this CreateGroup.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this CreateGroup.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this CreateGroup.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this CreateGroup.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def uid_token(self):
        """Gets the uid_token of this CreateGroup.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this CreateGroup.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this CreateGroup.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this CreateGroup.  # noqa: E501
        :type: str
        """

        self._uid_token = uid_token

    @property
    def user_assignment(self):
        """Gets the user_assignment of this CreateGroup.  # noqa: E501

        A json string defining the access permission assignment for this client  # noqa: E501

        :return: The user_assignment of this CreateGroup.  # noqa: E501
        :rtype: str
        """
        return self._user_assignment

    @user_assignment.setter
    def user_assignment(self, user_assignment):
        """Sets the user_assignment of this CreateGroup.

        A json string defining the access permission assignment for this client  # noqa: E501

        :param user_assignment: The user_assignment of this CreateGroup.  # noqa: E501
        :type: str
        """

        self._user_assignment = user_assignment

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
        if not isinstance(other, CreateGroup):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateGroup):
            return True

        return self.to_dict() != other.to_dict()
