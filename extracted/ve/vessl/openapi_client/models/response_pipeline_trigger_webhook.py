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


class ResponsePipelineTriggerWebhook(object):
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
        'endpoint_url': 'str',
        'prepared_argument_set': 'dict[str, V1VariableValue]',
        'webhook_type': 'str'
    }

    attribute_map = {
        'endpoint_url': 'endpoint_url',
        'prepared_argument_set': 'prepared_argument_set',
        'webhook_type': 'webhook_type'
    }

    def __init__(self, endpoint_url=None, prepared_argument_set=None, webhook_type=None, local_vars_configuration=None):  # noqa: E501
        """ResponsePipelineTriggerWebhook - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._endpoint_url = None
        self._prepared_argument_set = None
        self._webhook_type = None
        self.discriminator = None

        if endpoint_url is not None:
            self.endpoint_url = endpoint_url
        if prepared_argument_set is not None:
            self.prepared_argument_set = prepared_argument_set
        if webhook_type is not None:
            self.webhook_type = webhook_type

    @property
    def endpoint_url(self):
        """Gets the endpoint_url of this ResponsePipelineTriggerWebhook.  # noqa: E501


        :return: The endpoint_url of this ResponsePipelineTriggerWebhook.  # noqa: E501
        :rtype: str
        """
        return self._endpoint_url

    @endpoint_url.setter
    def endpoint_url(self, endpoint_url):
        """Sets the endpoint_url of this ResponsePipelineTriggerWebhook.


        :param endpoint_url: The endpoint_url of this ResponsePipelineTriggerWebhook.  # noqa: E501
        :type endpoint_url: str
        """

        self._endpoint_url = endpoint_url

    @property
    def prepared_argument_set(self):
        """Gets the prepared_argument_set of this ResponsePipelineTriggerWebhook.  # noqa: E501


        :return: The prepared_argument_set of this ResponsePipelineTriggerWebhook.  # noqa: E501
        :rtype: dict[str, V1VariableValue]
        """
        return self._prepared_argument_set

    @prepared_argument_set.setter
    def prepared_argument_set(self, prepared_argument_set):
        """Sets the prepared_argument_set of this ResponsePipelineTriggerWebhook.


        :param prepared_argument_set: The prepared_argument_set of this ResponsePipelineTriggerWebhook.  # noqa: E501
        :type prepared_argument_set: dict[str, V1VariableValue]
        """

        self._prepared_argument_set = prepared_argument_set

    @property
    def webhook_type(self):
        """Gets the webhook_type of this ResponsePipelineTriggerWebhook.  # noqa: E501


        :return: The webhook_type of this ResponsePipelineTriggerWebhook.  # noqa: E501
        :rtype: str
        """
        return self._webhook_type

    @webhook_type.setter
    def webhook_type(self, webhook_type):
        """Sets the webhook_type of this ResponsePipelineTriggerWebhook.


        :param webhook_type: The webhook_type of this ResponsePipelineTriggerWebhook.  # noqa: E501
        :type webhook_type: str
        """

        self._webhook_type = webhook_type

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
        if not isinstance(other, ResponsePipelineTriggerWebhook):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResponsePipelineTriggerWebhook):
            return True

        return self.to_dict() != other.to_dict()
