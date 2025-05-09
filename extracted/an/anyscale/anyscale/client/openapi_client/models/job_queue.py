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


class JobQueue(object):
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
        'id': 'str',
        'name': 'str',
        'user_provided_id': 'str',
        'created_at': 'datetime',
        'creator_id': 'str',
        'project_id': 'str',
        'cloud_id': 'str',
        'compute_config_id': 'str',
        'cluster_environment_build_id': 'str',
        'max_concurrency': 'int',
        'idle_timeout_sec': 'int',
        'execution_mode': 'JobQueueExecutionMode',
        'state': 'JobQueueState'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'user_provided_id': 'user_provided_id',
        'created_at': 'created_at',
        'creator_id': 'creator_id',
        'project_id': 'project_id',
        'cloud_id': 'cloud_id',
        'compute_config_id': 'compute_config_id',
        'cluster_environment_build_id': 'cluster_environment_build_id',
        'max_concurrency': 'max_concurrency',
        'idle_timeout_sec': 'idle_timeout_sec',
        'execution_mode': 'execution_mode',
        'state': 'state'
    }

    def __init__(self, id=None, name=None, user_provided_id=None, created_at=None, creator_id=None, project_id=None, cloud_id=None, compute_config_id=None, cluster_environment_build_id=None, max_concurrency=1, idle_timeout_sec=None, execution_mode=None, state=None, local_vars_configuration=None):  # noqa: E501
        """JobQueue - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._user_provided_id = None
        self._created_at = None
        self._creator_id = None
        self._project_id = None
        self._cloud_id = None
        self._compute_config_id = None
        self._cluster_environment_build_id = None
        self._max_concurrency = None
        self._idle_timeout_sec = None
        self._execution_mode = None
        self._state = None
        self.discriminator = None

        self.id = id
        if name is not None:
            self.name = name
        if user_provided_id is not None:
            self.user_provided_id = user_provided_id
        self.created_at = created_at
        self.creator_id = creator_id
        self.project_id = project_id
        self.cloud_id = cloud_id
        self.compute_config_id = compute_config_id
        self.cluster_environment_build_id = cluster_environment_build_id
        if max_concurrency is not None:
            self.max_concurrency = max_concurrency
        self.idle_timeout_sec = idle_timeout_sec
        if execution_mode is not None:
            self.execution_mode = execution_mode
        self.state = state

    @property
    def id(self):
        """Gets the id of this JobQueue.  # noqa: E501

        The id of this job queue  # noqa: E501

        :return: The id of this JobQueue.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this JobQueue.

        The id of this job queue  # noqa: E501

        :param id: The id of this JobQueue.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this JobQueue.  # noqa: E501

        Name of the job queue  # noqa: E501

        :return: The name of this JobQueue.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this JobQueue.

        Name of the job queue  # noqa: E501

        :param name: The name of this JobQueue.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def user_provided_id(self):
        """Gets the user_provided_id of this JobQueue.  # noqa: E501

        Optional user-provided identifier of the queue that could be subsequently used to reference the queue when submitting jobs.   # noqa: E501

        :return: The user_provided_id of this JobQueue.  # noqa: E501
        :rtype: str
        """
        return self._user_provided_id

    @user_provided_id.setter
    def user_provided_id(self, user_provided_id):
        """Sets the user_provided_id of this JobQueue.

        Optional user-provided identifier of the queue that could be subsequently used to reference the queue when submitting jobs.   # noqa: E501

        :param user_provided_id: The user_provided_id of this JobQueue.  # noqa: E501
        :type: str
        """

        self._user_provided_id = user_provided_id

    @property
    def created_at(self):
        """Gets the created_at of this JobQueue.  # noqa: E501

        The time this job queue was created  # noqa: E501

        :return: The created_at of this JobQueue.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this JobQueue.

        The time this job queue was created  # noqa: E501

        :param created_at: The created_at of this JobQueue.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_at is None:  # noqa: E501
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def creator_id(self):
        """Gets the creator_id of this JobQueue.  # noqa: E501

        The id of the user who created this job queue  # noqa: E501

        :return: The creator_id of this JobQueue.  # noqa: E501
        :rtype: str
        """
        return self._creator_id

    @creator_id.setter
    def creator_id(self, creator_id):
        """Sets the creator_id of this JobQueue.

        The id of the user who created this job queue  # noqa: E501

        :param creator_id: The creator_id of this JobQueue.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and creator_id is None:  # noqa: E501
            raise ValueError("Invalid value for `creator_id`, must not be `None`")  # noqa: E501

        self._creator_id = creator_id

    @property
    def project_id(self):
        """Gets the project_id of this JobQueue.  # noqa: E501

        The project id to which the job queue belongs to.  # noqa: E501

        :return: The project_id of this JobQueue.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this JobQueue.

        The project id to which the job queue belongs to.  # noqa: E501

        :param project_id: The project_id of this JobQueue.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and project_id is None:  # noqa: E501
            raise ValueError("Invalid value for `project_id`, must not be `None`")  # noqa: E501

        self._project_id = project_id

    @property
    def cloud_id(self):
        """Gets the cloud_id of this JobQueue.  # noqa: E501

        The cloud id to which the job queue belongs to.  # noqa: E501

        :return: The cloud_id of this JobQueue.  # noqa: E501
        :rtype: str
        """
        return self._cloud_id

    @cloud_id.setter
    def cloud_id(self, cloud_id):
        """Sets the cloud_id of this JobQueue.

        The cloud id to which the job queue belongs to.  # noqa: E501

        :param cloud_id: The cloud_id of this JobQueue.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and cloud_id is None:  # noqa: E501
            raise ValueError("Invalid value for `cloud_id`, must not be `None`")  # noqa: E501

        self._cloud_id = cloud_id

    @property
    def compute_config_id(self):
        """Gets the compute_config_id of this JobQueue.  # noqa: E501

        The id of the compute configuration that will be used to create cluster associated with the queue.  # noqa: E501

        :return: The compute_config_id of this JobQueue.  # noqa: E501
        :rtype: str
        """
        return self._compute_config_id

    @compute_config_id.setter
    def compute_config_id(self, compute_config_id):
        """Sets the compute_config_id of this JobQueue.

        The id of the compute configuration that will be used to create cluster associated with the queue.  # noqa: E501

        :param compute_config_id: The compute_config_id of this JobQueue.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and compute_config_id is None:  # noqa: E501
            raise ValueError("Invalid value for `compute_config_id`, must not be `None`")  # noqa: E501

        self._compute_config_id = compute_config_id

    @property
    def cluster_environment_build_id(self):
        """Gets the cluster_environment_build_id of this JobQueue.  # noqa: E501

        The id of the cluster environment build that will be used to create cluster associated with the queue.  # noqa: E501

        :return: The cluster_environment_build_id of this JobQueue.  # noqa: E501
        :rtype: str
        """
        return self._cluster_environment_build_id

    @cluster_environment_build_id.setter
    def cluster_environment_build_id(self, cluster_environment_build_id):
        """Sets the cluster_environment_build_id of this JobQueue.

        The id of the cluster environment build that will be used to create cluster associated with the queue.  # noqa: E501

        :param cluster_environment_build_id: The cluster_environment_build_id of this JobQueue.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and cluster_environment_build_id is None:  # noqa: E501
            raise ValueError("Invalid value for `cluster_environment_build_id`, must not be `None`")  # noqa: E501

        self._cluster_environment_build_id = cluster_environment_build_id

    @property
    def max_concurrency(self):
        """Gets the max_concurrency of this JobQueue.  # noqa: E501

        Max number of jobs to be run concurrently. Defaults to 1, ie running no more than 1 job at a time.  # noqa: E501

        :return: The max_concurrency of this JobQueue.  # noqa: E501
        :rtype: int
        """
        return self._max_concurrency

    @max_concurrency.setter
    def max_concurrency(self, max_concurrency):
        """Sets the max_concurrency of this JobQueue.

        Max number of jobs to be run concurrently. Defaults to 1, ie running no more than 1 job at a time.  # noqa: E501

        :param max_concurrency: The max_concurrency of this JobQueue.  # noqa: E501
        :type: int
        """

        self._max_concurrency = max_concurrency

    @property
    def idle_timeout_sec(self):
        """Gets the idle_timeout_sec of this JobQueue.  # noqa: E501

        Max period of time queue will be accepting new jobs, before being sealed off and its associated cluster being shutdown  # noqa: E501

        :return: The idle_timeout_sec of this JobQueue.  # noqa: E501
        :rtype: int
        """
        return self._idle_timeout_sec

    @idle_timeout_sec.setter
    def idle_timeout_sec(self, idle_timeout_sec):
        """Sets the idle_timeout_sec of this JobQueue.

        Max period of time queue will be accepting new jobs, before being sealed off and its associated cluster being shutdown  # noqa: E501

        :param idle_timeout_sec: The idle_timeout_sec of this JobQueue.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and idle_timeout_sec is None:  # noqa: E501
            raise ValueError("Invalid value for `idle_timeout_sec`, must not be `None`")  # noqa: E501

        self._idle_timeout_sec = idle_timeout_sec

    @property
    def execution_mode(self):
        """Gets the execution_mode of this JobQueue.  # noqa: E501

        Execution mode of the jobs submitted into the queue (one of: FIFO,LIFO,PRIORITY  # noqa: E501

        :return: The execution_mode of this JobQueue.  # noqa: E501
        :rtype: JobQueueExecutionMode
        """
        return self._execution_mode

    @execution_mode.setter
    def execution_mode(self, execution_mode):
        """Sets the execution_mode of this JobQueue.

        Execution mode of the jobs submitted into the queue (one of: FIFO,LIFO,PRIORITY  # noqa: E501

        :param execution_mode: The execution_mode of this JobQueue.  # noqa: E501
        :type: JobQueueExecutionMode
        """

        self._execution_mode = execution_mode

    @property
    def state(self):
        """Gets the state of this JobQueue.  # noqa: E501

        The current state of this job queue  # noqa: E501

        :return: The state of this JobQueue.  # noqa: E501
        :rtype: JobQueueState
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this JobQueue.

        The current state of this job queue  # noqa: E501

        :param state: The state of this JobQueue.  # noqa: E501
        :type: JobQueueState
        """
        if self.local_vars_configuration.client_side_validation and state is None:  # noqa: E501
            raise ValueError("Invalid value for `state`, must not be `None`")  # noqa: E501

        self._state = state

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
        if not isinstance(other, JobQueue):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, JobQueue):
            return True

        return self.to_dict() != other.to_dict()
