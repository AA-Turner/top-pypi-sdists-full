# coding: utf-8

"""
    Seeq REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 66.18.1-v202505080754-CD
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from pprint import pformat
from six import iteritems
import re


class ScreenshotOutputV1(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
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
        'screenshot': 'str',
        'status_message': 'str'
    }

    attribute_map = {
        'screenshot': 'screenshot',
        'status_message': 'statusMessage'
    }

    def __init__(self, screenshot=None, status_message=None):
        """
        ScreenshotOutputV1 - a model defined in Swagger
        """

        self._screenshot = None
        self._status_message = None

        if screenshot is not None:
          self.screenshot = screenshot
        if status_message is not None:
          self.status_message = status_message

    @property
    def screenshot(self):
        """
        Gets the screenshot of this ScreenshotOutputV1.
        The URL of the generated and cached screenshot

        :return: The screenshot of this ScreenshotOutputV1.
        :rtype: str
        """
        return self._screenshot

    @screenshot.setter
    def screenshot(self, screenshot):
        """
        Sets the screenshot of this ScreenshotOutputV1.
        The URL of the generated and cached screenshot

        :param screenshot: The screenshot of this ScreenshotOutputV1.
        :type: str
        """

        self._screenshot = screenshot

    @property
    def status_message(self):
        """
        Gets the status_message of this ScreenshotOutputV1.
        A plain language status message with information about any issues that may have been encountered during an operation. Null if the status message has not been set.

        :return: The status_message of this ScreenshotOutputV1.
        :rtype: str
        """
        return self._status_message

    @status_message.setter
    def status_message(self, status_message):
        """
        Sets the status_message of this ScreenshotOutputV1.
        A plain language status message with information about any issues that may have been encountered during an operation. Null if the status message has not been set.

        :param status_message: The status_message of this ScreenshotOutputV1.
        :type: str
        """

        self._status_message = status_message

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
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
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, ScreenshotOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
