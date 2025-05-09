# coding: utf-8

"""
    vod20250101

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class OperationForStartExecutionInput(object):
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
        'task': 'TaskForStartExecutionInput',
        'template': 'TemplateForStartExecutionInput',
        'type': 'str'
    }

    attribute_map = {
        'task': 'Task',
        'template': 'Template',
        'type': 'Type'
    }

    def __init__(self, task=None, template=None, type=None, _configuration=None):  # noqa: E501
        """OperationForStartExecutionInput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._task = None
        self._template = None
        self._type = None
        self.discriminator = None

        if task is not None:
            self.task = task
        if template is not None:
            self.template = template
        if type is not None:
            self.type = type

    @property
    def task(self):
        """Gets the task of this OperationForStartExecutionInput.  # noqa: E501


        :return: The task of this OperationForStartExecutionInput.  # noqa: E501
        :rtype: TaskForStartExecutionInput
        """
        return self._task

    @task.setter
    def task(self, task):
        """Sets the task of this OperationForStartExecutionInput.


        :param task: The task of this OperationForStartExecutionInput.  # noqa: E501
        :type: TaskForStartExecutionInput
        """

        self._task = task

    @property
    def template(self):
        """Gets the template of this OperationForStartExecutionInput.  # noqa: E501


        :return: The template of this OperationForStartExecutionInput.  # noqa: E501
        :rtype: TemplateForStartExecutionInput
        """
        return self._template

    @template.setter
    def template(self, template):
        """Sets the template of this OperationForStartExecutionInput.


        :param template: The template of this OperationForStartExecutionInput.  # noqa: E501
        :type: TemplateForStartExecutionInput
        """

        self._template = template

    @property
    def type(self):
        """Gets the type of this OperationForStartExecutionInput.  # noqa: E501


        :return: The type of this OperationForStartExecutionInput.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this OperationForStartExecutionInput.


        :param type: The type of this OperationForStartExecutionInput.  # noqa: E501
        :type: str
        """

        self._type = type

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
        if issubclass(OperationForStartExecutionInput, dict):
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
        if not isinstance(other, OperationForStartExecutionInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OperationForStartExecutionInput):
            return True

        return self.to_dict() != other.to_dict()
