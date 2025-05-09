# coding: utf-8

"""
    Managed Ray API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from openapi_client.configuration import Configuration


class CreateExperimentalWorkspace(object):
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
        'name': 'str',
        'description': 'str',
        'project_id': 'str',
        'cloud_id': 'str',
        'compute_config_id': 'str',
        'base_snapshot': 'str',
        'cluster_environment_build_id': 'str',
        'idle_timeout_minutes': 'int',
        'cloned_job_id': 'str',
        'cloned_workspace_id': 'str',
        'template_id': 'str',
        'template_url': 'str',
        'skip_start': 'bool'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'project_id': 'project_id',
        'cloud_id': 'cloud_id',
        'compute_config_id': 'compute_config_id',
        'base_snapshot': 'base_snapshot',
        'cluster_environment_build_id': 'cluster_environment_build_id',
        'idle_timeout_minutes': 'idle_timeout_minutes',
        'cloned_job_id': 'cloned_job_id',
        'cloned_workspace_id': 'cloned_workspace_id',
        'template_id': 'template_id',
        'template_url': 'template_url',
        'skip_start': 'skip_start'
    }

    def __init__(self, name=None, description=None, project_id=None, cloud_id=None, compute_config_id=None, base_snapshot=None, cluster_environment_build_id=None, idle_timeout_minutes=None, cloned_job_id=None, cloned_workspace_id=None, template_id=None, template_url=None, skip_start=None, local_vars_configuration=None):  # noqa: E501
        """CreateExperimentalWorkspace - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._description = None
        self._project_id = None
        self._cloud_id = None
        self._compute_config_id = None
        self._base_snapshot = None
        self._cluster_environment_build_id = None
        self._idle_timeout_minutes = None
        self._cloned_job_id = None
        self._cloned_workspace_id = None
        self._template_id = None
        self._template_url = None
        self._skip_start = None
        self.discriminator = None

        self.name = name
        if description is not None:
            self.description = description
        self.project_id = project_id
        self.cloud_id = cloud_id
        self.compute_config_id = compute_config_id
        if base_snapshot is not None:
            self.base_snapshot = base_snapshot
        self.cluster_environment_build_id = cluster_environment_build_id
        if idle_timeout_minutes is not None:
            self.idle_timeout_minutes = idle_timeout_minutes
        if cloned_job_id is not None:
            self.cloned_job_id = cloned_job_id
        if cloned_workspace_id is not None:
            self.cloned_workspace_id = cloned_workspace_id
        if template_id is not None:
            self.template_id = template_id
        if template_url is not None:
            self.template_url = template_url
        if skip_start is not None:
            self.skip_start = skip_start

    @property
    def name(self):
        """Gets the name of this CreateExperimentalWorkspace.  # noqa: E501

        Name of the workspace to be created.  # noqa: E501

        :return: The name of this CreateExperimentalWorkspace.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateExperimentalWorkspace.

        Name of the workspace to be created.  # noqa: E501

        :param name: The name of this CreateExperimentalWorkspace.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this CreateExperimentalWorkspace.  # noqa: E501

        Description of Workspace.  # noqa: E501

        :return: The description of this CreateExperimentalWorkspace.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CreateExperimentalWorkspace.

        Description of Workspace.  # noqa: E501

        :param description: The description of this CreateExperimentalWorkspace.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def project_id(self):
        """Gets the project_id of this CreateExperimentalWorkspace.  # noqa: E501

        Id of the project that this workspace belongs to.  # noqa: E501

        :return: The project_id of this CreateExperimentalWorkspace.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this CreateExperimentalWorkspace.

        Id of the project that this workspace belongs to.  # noqa: E501

        :param project_id: The project_id of this CreateExperimentalWorkspace.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and project_id is None:  # noqa: E501
            raise ValueError("Invalid value for `project_id`, must not be `None`")  # noqa: E501

        self._project_id = project_id

    @property
    def cloud_id(self):
        """Gets the cloud_id of this CreateExperimentalWorkspace.  # noqa: E501

        The cloud id for the workspace. DEPRECATED: We figure out the cloud_id from the compute_config.  # noqa: E501

        :return: The cloud_id of this CreateExperimentalWorkspace.  # noqa: E501
        :rtype: str
        """
        return self._cloud_id

    @cloud_id.setter
    def cloud_id(self, cloud_id):
        """Sets the cloud_id of this CreateExperimentalWorkspace.

        The cloud id for the workspace. DEPRECATED: We figure out the cloud_id from the compute_config.  # noqa: E501

        :param cloud_id: The cloud_id of this CreateExperimentalWorkspace.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and cloud_id is None:  # noqa: E501
            raise ValueError("Invalid value for `cloud_id`, must not be `None`")  # noqa: E501

        self._cloud_id = cloud_id

    @property
    def compute_config_id(self):
        """Gets the compute_config_id of this CreateExperimentalWorkspace.  # noqa: E501

        The compute config id for the workspace  # noqa: E501

        :return: The compute_config_id of this CreateExperimentalWorkspace.  # noqa: E501
        :rtype: str
        """
        return self._compute_config_id

    @compute_config_id.setter
    def compute_config_id(self, compute_config_id):
        """Sets the compute_config_id of this CreateExperimentalWorkspace.

        The compute config id for the workspace  # noqa: E501

        :param compute_config_id: The compute_config_id of this CreateExperimentalWorkspace.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and compute_config_id is None:  # noqa: E501
            raise ValueError("Invalid value for `compute_config_id`, must not be `None`")  # noqa: E501

        self._compute_config_id = compute_config_id

    @property
    def base_snapshot(self):
        """Gets the base_snapshot of this CreateExperimentalWorkspace.  # noqa: E501

        Metadata on base snapshot  # noqa: E501

        :return: The base_snapshot of this CreateExperimentalWorkspace.  # noqa: E501
        :rtype: str
        """
        return self._base_snapshot

    @base_snapshot.setter
    def base_snapshot(self, base_snapshot):
        """Sets the base_snapshot of this CreateExperimentalWorkspace.

        Metadata on base snapshot  # noqa: E501

        :param base_snapshot: The base_snapshot of this CreateExperimentalWorkspace.  # noqa: E501
        :type: str
        """

        self._base_snapshot = base_snapshot

    @property
    def cluster_environment_build_id(self):
        """Gets the cluster_environment_build_id of this CreateExperimentalWorkspace.  # noqa: E501

        The cluster environment build id for the cluster used by the workspace  # noqa: E501

        :return: The cluster_environment_build_id of this CreateExperimentalWorkspace.  # noqa: E501
        :rtype: str
        """
        return self._cluster_environment_build_id

    @cluster_environment_build_id.setter
    def cluster_environment_build_id(self, cluster_environment_build_id):
        """Sets the cluster_environment_build_id of this CreateExperimentalWorkspace.

        The cluster environment build id for the cluster used by the workspace  # noqa: E501

        :param cluster_environment_build_id: The cluster_environment_build_id of this CreateExperimentalWorkspace.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and cluster_environment_build_id is None:  # noqa: E501
            raise ValueError("Invalid value for `cluster_environment_build_id`, must not be `None`")  # noqa: E501

        self._cluster_environment_build_id = cluster_environment_build_id

    @property
    def idle_timeout_minutes(self):
        """Gets the idle_timeout_minutes of this CreateExperimentalWorkspace.  # noqa: E501

        Idle timeout (in minutes), after which the Cluster is terminated. Idle time is defined as the time during which a Cluster is not running a user command (through 'anyscale exec' or the Web UI), and does not have an attached driver. Time spent running Jupyter commands, or commands run through ssh, is still considered 'idle'.  # noqa: E501

        :return: The idle_timeout_minutes of this CreateExperimentalWorkspace.  # noqa: E501
        :rtype: int
        """
        return self._idle_timeout_minutes

    @idle_timeout_minutes.setter
    def idle_timeout_minutes(self, idle_timeout_minutes):
        """Sets the idle_timeout_minutes of this CreateExperimentalWorkspace.

        Idle timeout (in minutes), after which the Cluster is terminated. Idle time is defined as the time during which a Cluster is not running a user command (through 'anyscale exec' or the Web UI), and does not have an attached driver. Time spent running Jupyter commands, or commands run through ssh, is still considered 'idle'.  # noqa: E501

        :param idle_timeout_minutes: The idle_timeout_minutes of this CreateExperimentalWorkspace.  # noqa: E501
        :type: int
        """

        self._idle_timeout_minutes = idle_timeout_minutes

    @property
    def cloned_job_id(self):
        """Gets the cloned_job_id of this CreateExperimentalWorkspace.  # noqa: E501

        Ha job id of the associated ha job (could be job or v1 service).  # noqa: E501

        :return: The cloned_job_id of this CreateExperimentalWorkspace.  # noqa: E501
        :rtype: str
        """
        return self._cloned_job_id

    @cloned_job_id.setter
    def cloned_job_id(self, cloned_job_id):
        """Sets the cloned_job_id of this CreateExperimentalWorkspace.

        Ha job id of the associated ha job (could be job or v1 service).  # noqa: E501

        :param cloned_job_id: The cloned_job_id of this CreateExperimentalWorkspace.  # noqa: E501
        :type: str
        """

        self._cloned_job_id = cloned_job_id

    @property
    def cloned_workspace_id(self):
        """Gets the cloned_workspace_id of this CreateExperimentalWorkspace.  # noqa: E501

        Id of the cloned workspace.  # noqa: E501

        :return: The cloned_workspace_id of this CreateExperimentalWorkspace.  # noqa: E501
        :rtype: str
        """
        return self._cloned_workspace_id

    @cloned_workspace_id.setter
    def cloned_workspace_id(self, cloned_workspace_id):
        """Sets the cloned_workspace_id of this CreateExperimentalWorkspace.

        Id of the cloned workspace.  # noqa: E501

        :param cloned_workspace_id: The cloned_workspace_id of this CreateExperimentalWorkspace.  # noqa: E501
        :type: str
        """

        self._cloned_workspace_id = cloned_workspace_id

    @property
    def template_id(self):
        """Gets the template_id of this CreateExperimentalWorkspace.  # noqa: E501

        The Id of the template to use.  # noqa: E501

        :return: The template_id of this CreateExperimentalWorkspace.  # noqa: E501
        :rtype: str
        """
        return self._template_id

    @template_id.setter
    def template_id(self, template_id):
        """Sets the template_id of this CreateExperimentalWorkspace.

        The Id of the template to use.  # noqa: E501

        :param template_id: The template_id of this CreateExperimentalWorkspace.  # noqa: E501
        :type: str
        """

        self._template_id = template_id

    @property
    def template_url(self):
        """Gets the template_url of this CreateExperimentalWorkspace.  # noqa: E501

        The template's URL to use. When this is specified, the template_id is only used for generating the build id.  # noqa: E501

        :return: The template_url of this CreateExperimentalWorkspace.  # noqa: E501
        :rtype: str
        """
        return self._template_url

    @template_url.setter
    def template_url(self, template_url):
        """Sets the template_url of this CreateExperimentalWorkspace.

        The template's URL to use. When this is specified, the template_id is only used for generating the build id.  # noqa: E501

        :param template_url: The template_url of this CreateExperimentalWorkspace.  # noqa: E501
        :type: str
        """

        self._template_url = template_url

    @property
    def skip_start(self):
        """Gets the skip_start of this CreateExperimentalWorkspace.  # noqa: E501

        Skip start the workspace on creation.  # noqa: E501

        :return: The skip_start of this CreateExperimentalWorkspace.  # noqa: E501
        :rtype: bool
        """
        return self._skip_start

    @skip_start.setter
    def skip_start(self, skip_start):
        """Sets the skip_start of this CreateExperimentalWorkspace.

        Skip start the workspace on creation.  # noqa: E501

        :param skip_start: The skip_start of this CreateExperimentalWorkspace.  # noqa: E501
        :type: bool
        """

        self._skip_start = skip_start

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CreateExperimentalWorkspace):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateExperimentalWorkspace):
            return True

        return self.to_dict() != other.to_dict()
