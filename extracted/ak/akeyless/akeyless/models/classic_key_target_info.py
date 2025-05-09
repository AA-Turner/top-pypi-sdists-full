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


class ClassicKeyTargetInfo(object):
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
        'external_kms_id': 'ExternalKMSKeyId',
        'key_purpose': 'list[str]',
        'key_status': 'ClassicKeyStatusInfo',
        'target_assoc_id': 'str',
        'target_type': 'str'
    }

    attribute_map = {
        'external_kms_id': 'external_kms_id',
        'key_purpose': 'key_purpose',
        'key_status': 'key_status',
        'target_assoc_id': 'target_assoc_id',
        'target_type': 'target_type'
    }

    def __init__(self, external_kms_id=None, key_purpose=None, key_status=None, target_assoc_id=None, target_type=None, local_vars_configuration=None):  # noqa: E501
        """ClassicKeyTargetInfo - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._external_kms_id = None
        self._key_purpose = None
        self._key_status = None
        self._target_assoc_id = None
        self._target_type = None
        self.discriminator = None

        if external_kms_id is not None:
            self.external_kms_id = external_kms_id
        if key_purpose is not None:
            self.key_purpose = key_purpose
        if key_status is not None:
            self.key_status = key_status
        if target_assoc_id is not None:
            self.target_assoc_id = target_assoc_id
        if target_type is not None:
            self.target_type = target_type

    @property
    def external_kms_id(self):
        """Gets the external_kms_id of this ClassicKeyTargetInfo.  # noqa: E501


        :return: The external_kms_id of this ClassicKeyTargetInfo.  # noqa: E501
        :rtype: ExternalKMSKeyId
        """
        return self._external_kms_id

    @external_kms_id.setter
    def external_kms_id(self, external_kms_id):
        """Sets the external_kms_id of this ClassicKeyTargetInfo.


        :param external_kms_id: The external_kms_id of this ClassicKeyTargetInfo.  # noqa: E501
        :type: ExternalKMSKeyId
        """

        self._external_kms_id = external_kms_id

    @property
    def key_purpose(self):
        """Gets the key_purpose of this ClassicKeyTargetInfo.  # noqa: E501


        :return: The key_purpose of this ClassicKeyTargetInfo.  # noqa: E501
        :rtype: list[str]
        """
        return self._key_purpose

    @key_purpose.setter
    def key_purpose(self, key_purpose):
        """Sets the key_purpose of this ClassicKeyTargetInfo.


        :param key_purpose: The key_purpose of this ClassicKeyTargetInfo.  # noqa: E501
        :type: list[str]
        """

        self._key_purpose = key_purpose

    @property
    def key_status(self):
        """Gets the key_status of this ClassicKeyTargetInfo.  # noqa: E501


        :return: The key_status of this ClassicKeyTargetInfo.  # noqa: E501
        :rtype: ClassicKeyStatusInfo
        """
        return self._key_status

    @key_status.setter
    def key_status(self, key_status):
        """Sets the key_status of this ClassicKeyTargetInfo.


        :param key_status: The key_status of this ClassicKeyTargetInfo.  # noqa: E501
        :type: ClassicKeyStatusInfo
        """

        self._key_status = key_status

    @property
    def target_assoc_id(self):
        """Gets the target_assoc_id of this ClassicKeyTargetInfo.  # noqa: E501


        :return: The target_assoc_id of this ClassicKeyTargetInfo.  # noqa: E501
        :rtype: str
        """
        return self._target_assoc_id

    @target_assoc_id.setter
    def target_assoc_id(self, target_assoc_id):
        """Sets the target_assoc_id of this ClassicKeyTargetInfo.


        :param target_assoc_id: The target_assoc_id of this ClassicKeyTargetInfo.  # noqa: E501
        :type: str
        """

        self._target_assoc_id = target_assoc_id

    @property
    def target_type(self):
        """Gets the target_type of this ClassicKeyTargetInfo.  # noqa: E501


        :return: The target_type of this ClassicKeyTargetInfo.  # noqa: E501
        :rtype: str
        """
        return self._target_type

    @target_type.setter
    def target_type(self, target_type):
        """Sets the target_type of this ClassicKeyTargetInfo.


        :param target_type: The target_type of this ClassicKeyTargetInfo.  # noqa: E501
        :type: str
        """

        self._target_type = target_type

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
        if not isinstance(other, ClassicKeyTargetInfo):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ClassicKeyTargetInfo):
            return True

        return self.to_dict() != other.to_dict()
