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


class V1Toleration(object):
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
        'effect': 'str',
        'key': 'str',
        'operator': 'str',
        'toleration_seconds': 'int',
        'value': 'str'
    }

    attribute_map = {
        'effect': 'effect',
        'key': 'key',
        'operator': 'operator',
        'toleration_seconds': 'tolerationSeconds',
        'value': 'value'
    }

    def __init__(self, effect=None, key=None, operator=None, toleration_seconds=None, value=None, local_vars_configuration=None):  # noqa: E501
        """V1Toleration - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._effect = None
        self._key = None
        self._operator = None
        self._toleration_seconds = None
        self._value = None
        self.discriminator = None

        if effect is not None:
            self.effect = effect
        if key is not None:
            self.key = key
        if operator is not None:
            self.operator = operator
        self.toleration_seconds = toleration_seconds
        if value is not None:
            self.value = value

    @property
    def effect(self):
        """Gets the effect of this V1Toleration.  # noqa: E501


        :return: The effect of this V1Toleration.  # noqa: E501
        :rtype: str
        """
        return self._effect

    @effect.setter
    def effect(self, effect):
        """Sets the effect of this V1Toleration.


        :param effect: The effect of this V1Toleration.  # noqa: E501
        :type effect: str
        """

        self._effect = effect

    @property
    def key(self):
        """Gets the key of this V1Toleration.  # noqa: E501


        :return: The key of this V1Toleration.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this V1Toleration.


        :param key: The key of this V1Toleration.  # noqa: E501
        :type key: str
        """

        self._key = key

    @property
    def operator(self):
        """Gets the operator of this V1Toleration.  # noqa: E501


        :return: The operator of this V1Toleration.  # noqa: E501
        :rtype: str
        """
        return self._operator

    @operator.setter
    def operator(self, operator):
        """Sets the operator of this V1Toleration.


        :param operator: The operator of this V1Toleration.  # noqa: E501
        :type operator: str
        """

        self._operator = operator

    @property
    def toleration_seconds(self):
        """Gets the toleration_seconds of this V1Toleration.  # noqa: E501


        :return: The toleration_seconds of this V1Toleration.  # noqa: E501
        :rtype: int
        """
        return self._toleration_seconds

    @toleration_seconds.setter
    def toleration_seconds(self, toleration_seconds):
        """Sets the toleration_seconds of this V1Toleration.


        :param toleration_seconds: The toleration_seconds of this V1Toleration.  # noqa: E501
        :type toleration_seconds: int
        """

        self._toleration_seconds = toleration_seconds

    @property
    def value(self):
        """Gets the value of this V1Toleration.  # noqa: E501


        :return: The value of this V1Toleration.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this V1Toleration.


        :param value: The value of this V1Toleration.  # noqa: E501
        :type value: str
        """

        self._value = value

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
        if not isinstance(other, V1Toleration):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1Toleration):
            return True

        return self.to_dict() != other.to_dict()
