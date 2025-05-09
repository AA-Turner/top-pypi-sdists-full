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


class ModelServiceGatewayUpdateAPIInput(object):
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
        'annotations': 'dict[str, str]',
        'enabled': 'bool',
        'traffic_split': 'list[OrmModelServiceGatewayTrafficSplitEntry]'
    }

    attribute_map = {
        'annotations': 'annotations',
        'enabled': 'enabled',
        'traffic_split': 'traffic_split'
    }

    def __init__(self, annotations=None, enabled=None, traffic_split=None, local_vars_configuration=None):  # noqa: E501
        """ModelServiceGatewayUpdateAPIInput - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._annotations = None
        self._enabled = None
        self._traffic_split = None
        self.discriminator = None

        if annotations is not None:
            self.annotations = annotations
        if enabled is not None:
            self.enabled = enabled
        if traffic_split is not None:
            self.traffic_split = traffic_split

    @property
    def annotations(self):
        """Gets the annotations of this ModelServiceGatewayUpdateAPIInput.  # noqa: E501


        :return: The annotations of this ModelServiceGatewayUpdateAPIInput.  # noqa: E501
        :rtype: dict[str, str]
        """
        return self._annotations

    @annotations.setter
    def annotations(self, annotations):
        """Sets the annotations of this ModelServiceGatewayUpdateAPIInput.


        :param annotations: The annotations of this ModelServiceGatewayUpdateAPIInput.  # noqa: E501
        :type annotations: dict[str, str]
        """

        self._annotations = annotations

    @property
    def enabled(self):
        """Gets the enabled of this ModelServiceGatewayUpdateAPIInput.  # noqa: E501


        :return: The enabled of this ModelServiceGatewayUpdateAPIInput.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this ModelServiceGatewayUpdateAPIInput.


        :param enabled: The enabled of this ModelServiceGatewayUpdateAPIInput.  # noqa: E501
        :type enabled: bool
        """

        self._enabled = enabled

    @property
    def traffic_split(self):
        """Gets the traffic_split of this ModelServiceGatewayUpdateAPIInput.  # noqa: E501


        :return: The traffic_split of this ModelServiceGatewayUpdateAPIInput.  # noqa: E501
        :rtype: list[OrmModelServiceGatewayTrafficSplitEntry]
        """
        return self._traffic_split

    @traffic_split.setter
    def traffic_split(self, traffic_split):
        """Sets the traffic_split of this ModelServiceGatewayUpdateAPIInput.


        :param traffic_split: The traffic_split of this ModelServiceGatewayUpdateAPIInput.  # noqa: E501
        :type traffic_split: list[OrmModelServiceGatewayTrafficSplitEntry]
        """

        self._traffic_split = traffic_split

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
        if not isinstance(other, ModelServiceGatewayUpdateAPIInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ModelServiceGatewayUpdateAPIInput):
            return True

        return self.to_dict() != other.to_dict()
