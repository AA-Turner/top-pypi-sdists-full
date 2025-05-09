# coding: utf-8

"""
    AssistedInstall

    Assisted installation  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class NtpSynchronizationResponse(object):
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
        'ntp_sources': 'list[NtpSource]'
    }

    attribute_map = {
        'ntp_sources': 'ntp_sources'
    }

    def __init__(self, ntp_sources=None):  # noqa: E501
        """NtpSynchronizationResponse - a model defined in Swagger"""  # noqa: E501

        self._ntp_sources = None
        self.discriminator = None

        if ntp_sources is not None:
            self.ntp_sources = ntp_sources

    @property
    def ntp_sources(self):
        """Gets the ntp_sources of this NtpSynchronizationResponse.  # noqa: E501


        :return: The ntp_sources of this NtpSynchronizationResponse.  # noqa: E501
        :rtype: list[NtpSource]
        """
        return self._ntp_sources

    @ntp_sources.setter
    def ntp_sources(self, ntp_sources):
        """Sets the ntp_sources of this NtpSynchronizationResponse.


        :param ntp_sources: The ntp_sources of this NtpSynchronizationResponse.  # noqa: E501
        :type: list[NtpSource]
        """

        self._ntp_sources = ntp_sources

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
        if issubclass(NtpSynchronizationResponse, dict):
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
        if not isinstance(other, NtpSynchronizationResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
