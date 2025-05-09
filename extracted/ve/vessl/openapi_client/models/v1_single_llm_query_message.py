# coding: utf-8

"""
    Aron API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from openapi_client.configuration import Configuration


class V1SingleLLMQueryMessage(object):
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
        'content': 'str',
        'content_for_view': 'str',
        'role': 'str'
    }

    attribute_map = {
        'content': 'content',
        'content_for_view': 'content_for_view',
        'role': 'role'
    }

    def __init__(self, content=None, content_for_view=None, role=None, local_vars_configuration=None):  # noqa: E501
        """V1SingleLLMQueryMessage - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._content = None
        self._content_for_view = None
        self._role = None
        self.discriminator = None

        self.content = content
        if content_for_view is not None:
            self.content_for_view = content_for_view
        self.role = role

    @property
    def content(self):
        """Gets the content of this V1SingleLLMQueryMessage.  # noqa: E501


        :return: The content of this V1SingleLLMQueryMessage.  # noqa: E501
        :rtype: str
        """
        return self._content

    @content.setter
    def content(self, content):
        """Sets the content of this V1SingleLLMQueryMessage.


        :param content: The content of this V1SingleLLMQueryMessage.  # noqa: E501
        :type content: str
        """
        if self.local_vars_configuration.client_side_validation and content is None:  # noqa: E501
            raise ValueError("Invalid value for `content`, must not be `None`")  # noqa: E501

        self._content = content

    @property
    def content_for_view(self):
        """Gets the content_for_view of this V1SingleLLMQueryMessage.  # noqa: E501


        :return: The content_for_view of this V1SingleLLMQueryMessage.  # noqa: E501
        :rtype: str
        """
        return self._content_for_view

    @content_for_view.setter
    def content_for_view(self, content_for_view):
        """Sets the content_for_view of this V1SingleLLMQueryMessage.


        :param content_for_view: The content_for_view of this V1SingleLLMQueryMessage.  # noqa: E501
        :type content_for_view: str
        """

        self._content_for_view = content_for_view

    @property
    def role(self):
        """Gets the role of this V1SingleLLMQueryMessage.  # noqa: E501


        :return: The role of this V1SingleLLMQueryMessage.  # noqa: E501
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role):
        """Sets the role of this V1SingleLLMQueryMessage.


        :param role: The role of this V1SingleLLMQueryMessage.  # noqa: E501
        :type role: str
        """
        if self.local_vars_configuration.client_side_validation and role is None:  # noqa: E501
            raise ValueError("Invalid value for `role`, must not be `None`")  # noqa: E501
        allowed_values = ["system", "user", "agent"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and role not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `role` ({0}), must be one of {1}"  # noqa: E501
                .format(role, allowed_values)
            )

        self._role = role

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, V1SingleLLMQueryMessage):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1SingleLLMQueryMessage):
            return True

        return self.to_dict() != other.to_dict()
