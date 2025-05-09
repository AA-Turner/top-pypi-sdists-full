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


class GetProducersListReplyObj(object):
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
        'producers': 'list[Producer]',
        'producers_errors': 'object'
    }

    attribute_map = {
        'producers': 'producers',
        'producers_errors': 'producers_errors'
    }

    def __init__(self, producers=None, producers_errors=None, local_vars_configuration=None):  # noqa: E501
        """GetProducersListReplyObj - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._producers = None
        self._producers_errors = None
        self.discriminator = None

        if producers is not None:
            self.producers = producers
        if producers_errors is not None:
            self.producers_errors = producers_errors

    @property
    def producers(self):
        """Gets the producers of this GetProducersListReplyObj.  # noqa: E501


        :return: The producers of this GetProducersListReplyObj.  # noqa: E501
        :rtype: list[Producer]
        """
        return self._producers

    @producers.setter
    def producers(self, producers):
        """Sets the producers of this GetProducersListReplyObj.


        :param producers: The producers of this GetProducersListReplyObj.  # noqa: E501
        :type: list[Producer]
        """

        self._producers = producers

    @property
    def producers_errors(self):
        """Gets the producers_errors of this GetProducersListReplyObj.  # noqa: E501


        :return: The producers_errors of this GetProducersListReplyObj.  # noqa: E501
        :rtype: object
        """
        return self._producers_errors

    @producers_errors.setter
    def producers_errors(self, producers_errors):
        """Sets the producers_errors of this GetProducersListReplyObj.


        :param producers_errors: The producers_errors of this GetProducersListReplyObj.  # noqa: E501
        :type: object
        """

        self._producers_errors = producers_errors

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
        if not isinstance(other, GetProducersListReplyObj):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GetProducersListReplyObj):
            return True

        return self.to_dict() != other.to_dict()
