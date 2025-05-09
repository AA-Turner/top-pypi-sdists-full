# coding: utf-8

"""
    smc

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class DiskConfigForCreateMigrationJobInput(object):
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
        'disk_index': 'int',
        'disk_size': 'int'
    }

    attribute_map = {
        'disk_index': 'DiskIndex',
        'disk_size': 'DiskSize'
    }

    def __init__(self, disk_index=None, disk_size=None, _configuration=None):  # noqa: E501
        """DiskConfigForCreateMigrationJobInput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._disk_index = None
        self._disk_size = None
        self.discriminator = None

        self.disk_index = disk_index
        if disk_size is not None:
            self.disk_size = disk_size

    @property
    def disk_index(self):
        """Gets the disk_index of this DiskConfigForCreateMigrationJobInput.  # noqa: E501


        :return: The disk_index of this DiskConfigForCreateMigrationJobInput.  # noqa: E501
        :rtype: int
        """
        return self._disk_index

    @disk_index.setter
    def disk_index(self, disk_index):
        """Sets the disk_index of this DiskConfigForCreateMigrationJobInput.


        :param disk_index: The disk_index of this DiskConfigForCreateMigrationJobInput.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and disk_index is None:
            raise ValueError("Invalid value for `disk_index`, must not be `None`")  # noqa: E501

        self._disk_index = disk_index

    @property
    def disk_size(self):
        """Gets the disk_size of this DiskConfigForCreateMigrationJobInput.  # noqa: E501


        :return: The disk_size of this DiskConfigForCreateMigrationJobInput.  # noqa: E501
        :rtype: int
        """
        return self._disk_size

    @disk_size.setter
    def disk_size(self, disk_size):
        """Sets the disk_size of this DiskConfigForCreateMigrationJobInput.


        :param disk_size: The disk_size of this DiskConfigForCreateMigrationJobInput.  # noqa: E501
        :type: int
        """

        self._disk_size = disk_size

    def to_dict(self):
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
        if issubclass(DiskConfigForCreateMigrationJobInput, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, DiskConfigForCreateMigrationJobInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DiskConfigForCreateMigrationJobInput):
            return True

        return self.to_dict() != other.to_dict()
