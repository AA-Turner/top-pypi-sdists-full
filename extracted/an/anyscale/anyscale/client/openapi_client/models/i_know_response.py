# coding: utf-8

"""
    Managed Ray API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from openapi_client.configuration import Configuration


class IKnowResponse(object):
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
        'error': 'str',
        'time_series_events': 'list[IKnowTimeSeriesEvent]',
        'rootcause': 'str'
    }

    attribute_map = {
        'error': 'error',
        'time_series_events': 'time_series_events',
        'rootcause': 'rootcause'
    }

    def __init__(self, error=None, time_series_events=None, rootcause=None, local_vars_configuration=None):  # noqa: E501
        """IKnowResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._error = None
        self._time_series_events = None
        self._rootcause = None
        self.discriminator = None

        if error is not None:
            self.error = error
        self.time_series_events = time_series_events
        self.rootcause = rootcause

    @property
    def error(self):
        """Gets the error of this IKnowResponse.  # noqa: E501


        :return: The error of this IKnowResponse.  # noqa: E501
        :rtype: str
        """
        return self._error

    @error.setter
    def error(self, error):
        """Sets the error of this IKnowResponse.


        :param error: The error of this IKnowResponse.  # noqa: E501
        :type: str
        """

        self._error = error

    @property
    def time_series_events(self):
        """Gets the time_series_events of this IKnowResponse.  # noqa: E501


        :return: The time_series_events of this IKnowResponse.  # noqa: E501
        :rtype: list[IKnowTimeSeriesEvent]
        """
        return self._time_series_events

    @time_series_events.setter
    def time_series_events(self, time_series_events):
        """Sets the time_series_events of this IKnowResponse.


        :param time_series_events: The time_series_events of this IKnowResponse.  # noqa: E501
        :type: list[IKnowTimeSeriesEvent]
        """
        if self.local_vars_configuration.client_side_validation and time_series_events is None:  # noqa: E501
            raise ValueError("Invalid value for `time_series_events`, must not be `None`")  # noqa: E501

        self._time_series_events = time_series_events

    @property
    def rootcause(self):
        """Gets the rootcause of this IKnowResponse.  # noqa: E501


        :return: The rootcause of this IKnowResponse.  # noqa: E501
        :rtype: str
        """
        return self._rootcause

    @rootcause.setter
    def rootcause(self, rootcause):
        """Sets the rootcause of this IKnowResponse.


        :param rootcause: The rootcause of this IKnowResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and rootcause is None:  # noqa: E501
            raise ValueError("Invalid value for `rootcause`, must not be `None`")  # noqa: E501

        self._rootcause = rootcause

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
        if not isinstance(other, IKnowResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, IKnowResponse):
            return True

        return self.to_dict() != other.to_dict()
