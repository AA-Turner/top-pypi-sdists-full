# coding: utf-8

"""
    external/v1/auth_service.proto

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: version not set
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    NOTE
    ----
    standard swagger-codegen-cli for this python client has been modified
    by custom templates. The purpose of these templates is to include
    typing information in the API and Model code. Please refer to the
    main grid repository for more info
"""

import pprint
import re  # noqa: F401

from typing import TYPE_CHECKING

import six

if TYPE_CHECKING:
    from datetime import datetime
    from lightning_cloud.openapi.models import *

class V1StorageSystemMetrics(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'percentage': 'int',
        'total': 'int',
        'used': 'int'
    }

    attribute_map = {
        'percentage': 'percentage',
        'total': 'total',
        'used': 'used'
    }

    def __init__(self, percentage: 'int' =None, total: 'int' =None, used: 'int' =None):  # noqa: E501
        """V1StorageSystemMetrics - a model defined in Swagger"""  # noqa: E501
        self._percentage = None
        self._total = None
        self._used = None
        self.discriminator = None
        if percentage is not None:
            self.percentage = percentage
        if total is not None:
            self.total = total
        if used is not None:
            self.used = used

    @property
    def percentage(self) -> 'int':
        """Gets the percentage of this V1StorageSystemMetrics.  # noqa: E501


        :return: The percentage of this V1StorageSystemMetrics.  # noqa: E501
        :rtype: int
        """
        return self._percentage

    @percentage.setter
    def percentage(self, percentage: 'int'):
        """Sets the percentage of this V1StorageSystemMetrics.


        :param percentage: The percentage of this V1StorageSystemMetrics.  # noqa: E501
        :type: int
        """

        self._percentage = percentage

    @property
    def total(self) -> 'int':
        """Gets the total of this V1StorageSystemMetrics.  # noqa: E501


        :return: The total of this V1StorageSystemMetrics.  # noqa: E501
        :rtype: int
        """
        return self._total

    @total.setter
    def total(self, total: 'int'):
        """Sets the total of this V1StorageSystemMetrics.


        :param total: The total of this V1StorageSystemMetrics.  # noqa: E501
        :type: int
        """

        self._total = total

    @property
    def used(self) -> 'int':
        """Gets the used of this V1StorageSystemMetrics.  # noqa: E501


        :return: The used of this V1StorageSystemMetrics.  # noqa: E501
        :rtype: int
        """
        return self._used

    @used.setter
    def used(self, used: 'int'):
        """Sets the used of this V1StorageSystemMetrics.


        :param used: The used of this V1StorageSystemMetrics.  # noqa: E501
        :type: int
        """

        self._used = used

    def to_dict(self) -> dict:
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(V1StorageSystemMetrics, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1StorageSystemMetrics') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1StorageSystemMetrics):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1StorageSystemMetrics') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
