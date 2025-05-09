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


class UpgradeAgentResponse(object):
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
        'agent_image': 'str',
        'result': 'UpgradeAgentResult'
    }

    attribute_map = {
        'agent_image': 'agent_image',
        'result': 'result'
    }

    def __init__(self, agent_image=None, result=None):  # noqa: E501
        """UpgradeAgentResponse - a model defined in Swagger"""  # noqa: E501

        self._agent_image = None
        self._result = None
        self.discriminator = None

        if agent_image is not None:
            self.agent_image = agent_image
        if result is not None:
            self.result = result

    @property
    def agent_image(self):
        """Gets the agent_image of this UpgradeAgentResponse.  # noqa: E501

        Full image reference of the image that the agent has upgraded to, for example `quay.io/registry-proxy.engineering.redhat.com/rh-osbs/openshift4-assisted-installer-agent-rhel8:v1.0.0-142`.   # noqa: E501

        :return: The agent_image of this UpgradeAgentResponse.  # noqa: E501
        :rtype: str
        """
        return self._agent_image

    @agent_image.setter
    def agent_image(self, agent_image):
        """Sets the agent_image of this UpgradeAgentResponse.

        Full image reference of the image that the agent has upgraded to, for example `quay.io/registry-proxy.engineering.redhat.com/rh-osbs/openshift4-assisted-installer-agent-rhel8:v1.0.0-142`.   # noqa: E501

        :param agent_image: The agent_image of this UpgradeAgentResponse.  # noqa: E501
        :type: str
        """

        self._agent_image = agent_image

    @property
    def result(self):
        """Gets the result of this UpgradeAgentResponse.  # noqa: E501


        :return: The result of this UpgradeAgentResponse.  # noqa: E501
        :rtype: UpgradeAgentResult
        """
        return self._result

    @result.setter
    def result(self, result):
        """Sets the result of this UpgradeAgentResponse.


        :param result: The result of this UpgradeAgentResponse.  # noqa: E501
        :type: UpgradeAgentResult
        """

        self._result = result

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
        if issubclass(UpgradeAgentResponse, dict):
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
        if not isinstance(other, UpgradeAgentResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
