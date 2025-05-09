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


class ScheduledNotebookListOutputV1(object):
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
        'scheduled_notebooks': 'list[ScheduledNotebookOutputV1]',
        'status_message': 'str'
    }

    attribute_map = {
        'scheduled_notebooks': 'scheduledNotebooks',
        'status_message': 'statusMessage'
    }

    def __init__(self, scheduled_notebooks=None, status_message=None):
        """
        ScheduledNotebookListOutputV1 - a model defined in Swagger
        """

        self._scheduled_notebooks = None
        self._status_message = None

        if scheduled_notebooks is not None:
          self.scheduled_notebooks = scheduled_notebooks
        if status_message is not None:
          self.status_message = status_message

    @property
    def scheduled_notebooks(self):
        """
        Gets the scheduled_notebooks of this ScheduledNotebookListOutputV1.
        The scheduled notebooks within this Project

        :return: The scheduled_notebooks of this ScheduledNotebookListOutputV1.
        :rtype: list[ScheduledNotebookOutputV1]
        """
        return self._scheduled_notebooks

    @scheduled_notebooks.setter
    def scheduled_notebooks(self, scheduled_notebooks):
        """
        Sets the scheduled_notebooks of this ScheduledNotebookListOutputV1.
        The scheduled notebooks within this Project

        :param scheduled_notebooks: The scheduled_notebooks of this ScheduledNotebookListOutputV1.
        :type: list[ScheduledNotebookOutputV1]
        """

        self._scheduled_notebooks = scheduled_notebooks

    @property
    def status_message(self):
        """
        Gets the status_message of this ScheduledNotebookListOutputV1.
        A plain language status message with information about any issues that may have been encountered during an operation

        :return: The status_message of this ScheduledNotebookListOutputV1.
        :rtype: str
        """
        return self._status_message

    @status_message.setter
    def status_message(self, status_message):
        """
        Sets the status_message of this ScheduledNotebookListOutputV1.
        A plain language status message with information about any issues that may have been encountered during an operation

        :param status_message: The status_message of this ScheduledNotebookListOutputV1.
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
        if not isinstance(other, ScheduledNotebookListOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
