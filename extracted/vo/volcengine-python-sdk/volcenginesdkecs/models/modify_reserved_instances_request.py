# coding: utf-8

"""
    ecs

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class ModifyReservedInstancesRequest(object):
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
        'auto_renew': 'bool',
        'auto_renew_period': 'int',
        'client_token': 'str',
        'configurations': 'list[ConfigurationForModifyReservedInstancesInput]',
        'description': 'str',
        'project_name': 'str',
        'region_id': 'str',
        'reserved_instance_ids': 'list[str]',
        'tags': 'list[TagForModifyReservedInstancesInput]'
    }

    attribute_map = {
        'auto_renew': 'AutoRenew',
        'auto_renew_period': 'AutoRenewPeriod',
        'client_token': 'ClientToken',
        'configurations': 'Configurations',
        'description': 'Description',
        'project_name': 'ProjectName',
        'region_id': 'RegionId',
        'reserved_instance_ids': 'ReservedInstanceIds',
        'tags': 'Tags'
    }

    def __init__(self, auto_renew=None, auto_renew_period=None, client_token=None, configurations=None, description=None, project_name=None, region_id=None, reserved_instance_ids=None, tags=None, _configuration=None):  # noqa: E501
        """ModifyReservedInstancesRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._auto_renew = None
        self._auto_renew_period = None
        self._client_token = None
        self._configurations = None
        self._description = None
        self._project_name = None
        self._region_id = None
        self._reserved_instance_ids = None
        self._tags = None
        self.discriminator = None

        if auto_renew is not None:
            self.auto_renew = auto_renew
        if auto_renew_period is not None:
            self.auto_renew_period = auto_renew_period
        if client_token is not None:
            self.client_token = client_token
        if configurations is not None:
            self.configurations = configurations
        if description is not None:
            self.description = description
        if project_name is not None:
            self.project_name = project_name
        if region_id is not None:
            self.region_id = region_id
        if reserved_instance_ids is not None:
            self.reserved_instance_ids = reserved_instance_ids
        if tags is not None:
            self.tags = tags

    @property
    def auto_renew(self):
        """Gets the auto_renew of this ModifyReservedInstancesRequest.  # noqa: E501


        :return: The auto_renew of this ModifyReservedInstancesRequest.  # noqa: E501
        :rtype: bool
        """
        return self._auto_renew

    @auto_renew.setter
    def auto_renew(self, auto_renew):
        """Sets the auto_renew of this ModifyReservedInstancesRequest.


        :param auto_renew: The auto_renew of this ModifyReservedInstancesRequest.  # noqa: E501
        :type: bool
        """

        self._auto_renew = auto_renew

    @property
    def auto_renew_period(self):
        """Gets the auto_renew_period of this ModifyReservedInstancesRequest.  # noqa: E501


        :return: The auto_renew_period of this ModifyReservedInstancesRequest.  # noqa: E501
        :rtype: int
        """
        return self._auto_renew_period

    @auto_renew_period.setter
    def auto_renew_period(self, auto_renew_period):
        """Sets the auto_renew_period of this ModifyReservedInstancesRequest.


        :param auto_renew_period: The auto_renew_period of this ModifyReservedInstancesRequest.  # noqa: E501
        :type: int
        """

        self._auto_renew_period = auto_renew_period

    @property
    def client_token(self):
        """Gets the client_token of this ModifyReservedInstancesRequest.  # noqa: E501


        :return: The client_token of this ModifyReservedInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._client_token

    @client_token.setter
    def client_token(self, client_token):
        """Sets the client_token of this ModifyReservedInstancesRequest.


        :param client_token: The client_token of this ModifyReservedInstancesRequest.  # noqa: E501
        :type: str
        """

        self._client_token = client_token

    @property
    def configurations(self):
        """Gets the configurations of this ModifyReservedInstancesRequest.  # noqa: E501


        :return: The configurations of this ModifyReservedInstancesRequest.  # noqa: E501
        :rtype: list[ConfigurationForModifyReservedInstancesInput]
        """
        return self._configurations

    @configurations.setter
    def configurations(self, configurations):
        """Sets the configurations of this ModifyReservedInstancesRequest.


        :param configurations: The configurations of this ModifyReservedInstancesRequest.  # noqa: E501
        :type: list[ConfigurationForModifyReservedInstancesInput]
        """

        self._configurations = configurations

    @property
    def description(self):
        """Gets the description of this ModifyReservedInstancesRequest.  # noqa: E501


        :return: The description of this ModifyReservedInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ModifyReservedInstancesRequest.


        :param description: The description of this ModifyReservedInstancesRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def project_name(self):
        """Gets the project_name of this ModifyReservedInstancesRequest.  # noqa: E501


        :return: The project_name of this ModifyReservedInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Sets the project_name of this ModifyReservedInstancesRequest.


        :param project_name: The project_name of this ModifyReservedInstancesRequest.  # noqa: E501
        :type: str
        """

        self._project_name = project_name

    @property
    def region_id(self):
        """Gets the region_id of this ModifyReservedInstancesRequest.  # noqa: E501


        :return: The region_id of this ModifyReservedInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._region_id

    @region_id.setter
    def region_id(self, region_id):
        """Sets the region_id of this ModifyReservedInstancesRequest.


        :param region_id: The region_id of this ModifyReservedInstancesRequest.  # noqa: E501
        :type: str
        """

        self._region_id = region_id

    @property
    def reserved_instance_ids(self):
        """Gets the reserved_instance_ids of this ModifyReservedInstancesRequest.  # noqa: E501


        :return: The reserved_instance_ids of this ModifyReservedInstancesRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._reserved_instance_ids

    @reserved_instance_ids.setter
    def reserved_instance_ids(self, reserved_instance_ids):
        """Sets the reserved_instance_ids of this ModifyReservedInstancesRequest.


        :param reserved_instance_ids: The reserved_instance_ids of this ModifyReservedInstancesRequest.  # noqa: E501
        :type: list[str]
        """

        self._reserved_instance_ids = reserved_instance_ids

    @property
    def tags(self):
        """Gets the tags of this ModifyReservedInstancesRequest.  # noqa: E501


        :return: The tags of this ModifyReservedInstancesRequest.  # noqa: E501
        :rtype: list[TagForModifyReservedInstancesInput]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this ModifyReservedInstancesRequest.


        :param tags: The tags of this ModifyReservedInstancesRequest.  # noqa: E501
        :type: list[TagForModifyReservedInstancesInput]
        """

        self._tags = tags

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
        if issubclass(ModifyReservedInstancesRequest, dict):
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
        if not isinstance(other, ModifyReservedInstancesRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ModifyReservedInstancesRequest):
            return True

        return self.to_dict() != other.to_dict()
