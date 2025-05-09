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


class BatchTokenizationRequestLine(object):
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
        'data': 'str',
        'item_id': 'int',
        'tweak': 'str'
    }

    attribute_map = {
        'data': 'data',
        'item_id': 'item_id',
        'tweak': 'tweak'
    }

    def __init__(self, data=None, item_id=None, tweak=None, local_vars_configuration=None):  # noqa: E501
        """BatchTokenizationRequestLine - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._data = None
        self._item_id = None
        self._tweak = None
        self.discriminator = None

        if data is not None:
            self.data = data
        if item_id is not None:
            self.item_id = item_id
        if tweak is not None:
            self.tweak = tweak

    @property
    def data(self):
        """Gets the data of this BatchTokenizationRequestLine.  # noqa: E501


        :return: The data of this BatchTokenizationRequestLine.  # noqa: E501
        :rtype: str
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this BatchTokenizationRequestLine.


        :param data: The data of this BatchTokenizationRequestLine.  # noqa: E501
        :type: str
        """

        self._data = data

    @property
    def item_id(self):
        """Gets the item_id of this BatchTokenizationRequestLine.  # noqa: E501


        :return: The item_id of this BatchTokenizationRequestLine.  # noqa: E501
        :rtype: int
        """
        return self._item_id

    @item_id.setter
    def item_id(self, item_id):
        """Sets the item_id of this BatchTokenizationRequestLine.


        :param item_id: The item_id of this BatchTokenizationRequestLine.  # noqa: E501
        :type: int
        """

        self._item_id = item_id

    @property
    def tweak(self):
        """Gets the tweak of this BatchTokenizationRequestLine.  # noqa: E501


        :return: The tweak of this BatchTokenizationRequestLine.  # noqa: E501
        :rtype: str
        """
        return self._tweak

    @tweak.setter
    def tweak(self, tweak):
        """Sets the tweak of this BatchTokenizationRequestLine.


        :param tweak: The tweak of this BatchTokenizationRequestLine.  # noqa: E501
        :type: str
        """

        self._tweak = tweak

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
        if not isinstance(other, BatchTokenizationRequestLine):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BatchTokenizationRequestLine):
            return True

        return self.to_dict() != other.to_dict()
