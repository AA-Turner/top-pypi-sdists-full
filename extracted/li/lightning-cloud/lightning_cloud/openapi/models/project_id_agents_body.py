# coding: utf-8

"""
    external/v1/auth_service.proto

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: version not set
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    NOTE
    ----
    standard swagger-codegen-cli for this python client has been modified
    by custom templates. The purpose of these templates is to include
    typing information in the API and Model code. Please refer to the
    main grid repository for more info
"""

import pprint
import re  # noqa: F401

from typing import TYPE_CHECKING

import six

if TYPE_CHECKING:
    from datetime import datetime
    from lightning_cloud.openapi.models import *

class ProjectIdAgentsBody(object):
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
        'cloudspace_id': 'str',
        'cluster_id': 'str',
        'description': 'str',
        'endpoint': 'V1Endpoint',
        'internal_assistant_name': 'str',
        'knowledge': 'str',
        'model': 'str',
        'name': 'str',
        'org_id': 'str',
        'prompt_suggestions': 'list[V1PromptSuggestion]',
        'prompt_template': 'str',
        'thumbnail_url': 'str'
    }

    attribute_map = {
        'cloudspace_id': 'cloudspaceId',
        'cluster_id': 'clusterId',
        'description': 'description',
        'endpoint': 'endpoint',
        'internal_assistant_name': 'internalAssistantName',
        'knowledge': 'knowledge',
        'model': 'model',
        'name': 'name',
        'org_id': 'orgId',
        'prompt_suggestions': 'promptSuggestions',
        'prompt_template': 'promptTemplate',
        'thumbnail_url': 'thumbnailUrl'
    }

    def __init__(self, cloudspace_id: 'str' =None, cluster_id: 'str' =None, description: 'str' =None, endpoint: 'V1Endpoint' =None, internal_assistant_name: 'str' =None, knowledge: 'str' =None, model: 'str' =None, name: 'str' =None, org_id: 'str' =None, prompt_suggestions: 'list[V1PromptSuggestion]' =None, prompt_template: 'str' =None, thumbnail_url: 'str' =None):  # noqa: E501
        """ProjectIdAgentsBody - a model defined in Swagger"""  # noqa: E501
        self._cloudspace_id = None
        self._cluster_id = None
        self._description = None
        self._endpoint = None
        self._internal_assistant_name = None
        self._knowledge = None
        self._model = None
        self._name = None
        self._org_id = None
        self._prompt_suggestions = None
        self._prompt_template = None
        self._thumbnail_url = None
        self.discriminator = None
        if cloudspace_id is not None:
            self.cloudspace_id = cloudspace_id
        if cluster_id is not None:
            self.cluster_id = cluster_id
        if description is not None:
            self.description = description
        if endpoint is not None:
            self.endpoint = endpoint
        if internal_assistant_name is not None:
            self.internal_assistant_name = internal_assistant_name
        if knowledge is not None:
            self.knowledge = knowledge
        if model is not None:
            self.model = model
        if name is not None:
            self.name = name
        if org_id is not None:
            self.org_id = org_id
        if prompt_suggestions is not None:
            self.prompt_suggestions = prompt_suggestions
        if prompt_template is not None:
            self.prompt_template = prompt_template
        if thumbnail_url is not None:
            self.thumbnail_url = thumbnail_url

    @property
    def cloudspace_id(self) -> 'str':
        """Gets the cloudspace_id of this ProjectIdAgentsBody.  # noqa: E501


        :return: The cloudspace_id of this ProjectIdAgentsBody.  # noqa: E501
        :rtype: str
        """
        return self._cloudspace_id

    @cloudspace_id.setter
    def cloudspace_id(self, cloudspace_id: 'str'):
        """Sets the cloudspace_id of this ProjectIdAgentsBody.


        :param cloudspace_id: The cloudspace_id of this ProjectIdAgentsBody.  # noqa: E501
        :type: str
        """

        self._cloudspace_id = cloudspace_id

    @property
    def cluster_id(self) -> 'str':
        """Gets the cluster_id of this ProjectIdAgentsBody.  # noqa: E501


        :return: The cluster_id of this ProjectIdAgentsBody.  # noqa: E501
        :rtype: str
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id: 'str'):
        """Sets the cluster_id of this ProjectIdAgentsBody.


        :param cluster_id: The cluster_id of this ProjectIdAgentsBody.  # noqa: E501
        :type: str
        """

        self._cluster_id = cluster_id

    @property
    def description(self) -> 'str':
        """Gets the description of this ProjectIdAgentsBody.  # noqa: E501


        :return: The description of this ProjectIdAgentsBody.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: 'str'):
        """Sets the description of this ProjectIdAgentsBody.


        :param description: The description of this ProjectIdAgentsBody.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def endpoint(self) -> 'V1Endpoint':
        """Gets the endpoint of this ProjectIdAgentsBody.  # noqa: E501


        :return: The endpoint of this ProjectIdAgentsBody.  # noqa: E501
        :rtype: V1Endpoint
        """
        return self._endpoint

    @endpoint.setter
    def endpoint(self, endpoint: 'V1Endpoint'):
        """Sets the endpoint of this ProjectIdAgentsBody.


        :param endpoint: The endpoint of this ProjectIdAgentsBody.  # noqa: E501
        :type: V1Endpoint
        """

        self._endpoint = endpoint

    @property
    def internal_assistant_name(self) -> 'str':
        """Gets the internal_assistant_name of this ProjectIdAgentsBody.  # noqa: E501


        :return: The internal_assistant_name of this ProjectIdAgentsBody.  # noqa: E501
        :rtype: str
        """
        return self._internal_assistant_name

    @internal_assistant_name.setter
    def internal_assistant_name(self, internal_assistant_name: 'str'):
        """Sets the internal_assistant_name of this ProjectIdAgentsBody.


        :param internal_assistant_name: The internal_assistant_name of this ProjectIdAgentsBody.  # noqa: E501
        :type: str
        """

        self._internal_assistant_name = internal_assistant_name

    @property
    def knowledge(self) -> 'str':
        """Gets the knowledge of this ProjectIdAgentsBody.  # noqa: E501


        :return: The knowledge of this ProjectIdAgentsBody.  # noqa: E501
        :rtype: str
        """
        return self._knowledge

    @knowledge.setter
    def knowledge(self, knowledge: 'str'):
        """Sets the knowledge of this ProjectIdAgentsBody.


        :param knowledge: The knowledge of this ProjectIdAgentsBody.  # noqa: E501
        :type: str
        """

        self._knowledge = knowledge

    @property
    def model(self) -> 'str':
        """Gets the model of this ProjectIdAgentsBody.  # noqa: E501


        :return: The model of this ProjectIdAgentsBody.  # noqa: E501
        :rtype: str
        """
        return self._model

    @model.setter
    def model(self, model: 'str'):
        """Sets the model of this ProjectIdAgentsBody.


        :param model: The model of this ProjectIdAgentsBody.  # noqa: E501
        :type: str
        """

        self._model = model

    @property
    def name(self) -> 'str':
        """Gets the name of this ProjectIdAgentsBody.  # noqa: E501


        :return: The name of this ProjectIdAgentsBody.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: 'str'):
        """Sets the name of this ProjectIdAgentsBody.


        :param name: The name of this ProjectIdAgentsBody.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def org_id(self) -> 'str':
        """Gets the org_id of this ProjectIdAgentsBody.  # noqa: E501


        :return: The org_id of this ProjectIdAgentsBody.  # noqa: E501
        :rtype: str
        """
        return self._org_id

    @org_id.setter
    def org_id(self, org_id: 'str'):
        """Sets the org_id of this ProjectIdAgentsBody.


        :param org_id: The org_id of this ProjectIdAgentsBody.  # noqa: E501
        :type: str
        """

        self._org_id = org_id

    @property
    def prompt_suggestions(self) -> 'list[V1PromptSuggestion]':
        """Gets the prompt_suggestions of this ProjectIdAgentsBody.  # noqa: E501


        :return: The prompt_suggestions of this ProjectIdAgentsBody.  # noqa: E501
        :rtype: list[V1PromptSuggestion]
        """
        return self._prompt_suggestions

    @prompt_suggestions.setter
    def prompt_suggestions(self, prompt_suggestions: 'list[V1PromptSuggestion]'):
        """Sets the prompt_suggestions of this ProjectIdAgentsBody.


        :param prompt_suggestions: The prompt_suggestions of this ProjectIdAgentsBody.  # noqa: E501
        :type: list[V1PromptSuggestion]
        """

        self._prompt_suggestions = prompt_suggestions

    @property
    def prompt_template(self) -> 'str':
        """Gets the prompt_template of this ProjectIdAgentsBody.  # noqa: E501


        :return: The prompt_template of this ProjectIdAgentsBody.  # noqa: E501
        :rtype: str
        """
        return self._prompt_template

    @prompt_template.setter
    def prompt_template(self, prompt_template: 'str'):
        """Sets the prompt_template of this ProjectIdAgentsBody.


        :param prompt_template: The prompt_template of this ProjectIdAgentsBody.  # noqa: E501
        :type: str
        """

        self._prompt_template = prompt_template

    @property
    def thumbnail_url(self) -> 'str':
        """Gets the thumbnail_url of this ProjectIdAgentsBody.  # noqa: E501


        :return: The thumbnail_url of this ProjectIdAgentsBody.  # noqa: E501
        :rtype: str
        """
        return self._thumbnail_url

    @thumbnail_url.setter
    def thumbnail_url(self, thumbnail_url: 'str'):
        """Sets the thumbnail_url of this ProjectIdAgentsBody.


        :param thumbnail_url: The thumbnail_url of this ProjectIdAgentsBody.  # noqa: E501
        :type: str
        """

        self._thumbnail_url = thumbnail_url

    def to_dict(self) -> dict:
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
        if issubclass(ProjectIdAgentsBody, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'ProjectIdAgentsBody') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, ProjectIdAgentsBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ProjectIdAgentsBody') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
