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


class LogFilter(object):
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
        'node_ip': 'str',
        'actor_id': 'str',
        'task_id': 'str',
        'glob': 'str',
        'cluster_id': 'str',
        'job_id': 'str',
        'job_run': 'str',
        'instance_id': 'str',
        'node_type': 'NodeType',
        'process_id': 'str',
        'session_id': 'str',
        'file_name': 'str'
    }

    attribute_map = {
        'node_ip': 'node_ip',
        'actor_id': 'actor_id',
        'task_id': 'task_id',
        'glob': 'glob',
        'cluster_id': 'cluster_id',
        'job_id': 'job_id',
        'job_run': 'job_run',
        'instance_id': 'instance_id',
        'node_type': 'node_type',
        'process_id': 'process_id',
        'session_id': 'session_id',
        'file_name': 'file_name'
    }

    def __init__(self, node_ip=None, actor_id=None, task_id=None, glob=None, cluster_id=None, job_id=None, job_run=None, instance_id=None, node_type=None, process_id=None, session_id=None, file_name=None, local_vars_configuration=None):  # noqa: E501
        """LogFilter - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._node_ip = None
        self._actor_id = None
        self._task_id = None
        self._glob = None
        self._cluster_id = None
        self._job_id = None
        self._job_run = None
        self._instance_id = None
        self._node_type = None
        self._process_id = None
        self._session_id = None
        self._file_name = None
        self.discriminator = None

        if node_ip is not None:
            self.node_ip = node_ip
        if actor_id is not None:
            self.actor_id = actor_id
        if task_id is not None:
            self.task_id = task_id
        if glob is not None:
            self.glob = glob
        if cluster_id is not None:
            self.cluster_id = cluster_id
        if job_id is not None:
            self.job_id = job_id
        if job_run is not None:
            self.job_run = job_run
        if instance_id is not None:
            self.instance_id = instance_id
        if node_type is not None:
            self.node_type = node_type
        if process_id is not None:
            self.process_id = process_id
        if session_id is not None:
            self.session_id = session_id
        if file_name is not None:
            self.file_name = file_name

    @property
    def node_ip(self):
        """Gets the node_ip of this LogFilter.  # noqa: E501

        Filter logs by node_ip (Internal Node IP).  # noqa: E501

        :return: The node_ip of this LogFilter.  # noqa: E501
        :rtype: str
        """
        return self._node_ip

    @node_ip.setter
    def node_ip(self, node_ip):
        """Sets the node_ip of this LogFilter.

        Filter logs by node_ip (Internal Node IP).  # noqa: E501

        :param node_ip: The node_ip of this LogFilter.  # noqa: E501
        :type: str
        """

        self._node_ip = node_ip

    @property
    def actor_id(self):
        """Gets the actor_id of this LogFilter.  # noqa: E501

        Filter logs by actor_id.  # noqa: E501

        :return: The actor_id of this LogFilter.  # noqa: E501
        :rtype: str
        """
        return self._actor_id

    @actor_id.setter
    def actor_id(self, actor_id):
        """Sets the actor_id of this LogFilter.

        Filter logs by actor_id.  # noqa: E501

        :param actor_id: The actor_id of this LogFilter.  # noqa: E501
        :type: str
        """

        self._actor_id = actor_id

    @property
    def task_id(self):
        """Gets the task_id of this LogFilter.  # noqa: E501

        Filter logs by task_id.  # noqa: E501

        :return: The task_id of this LogFilter.  # noqa: E501
        :rtype: str
        """
        return self._task_id

    @task_id.setter
    def task_id(self, task_id):
        """Sets the task_id of this LogFilter.

        Filter logs by task_id.  # noqa: E501

        :param task_id: The task_id of this LogFilter.  # noqa: E501
        :type: str
        """

        self._task_id = task_id

    @property
    def glob(self):
        """Gets the glob of this LogFilter.  # noqa: E501

        Filter logs by a glob filter.  # noqa: E501

        :return: The glob of this LogFilter.  # noqa: E501
        :rtype: str
        """
        return self._glob

    @glob.setter
    def glob(self, glob):
        """Sets the glob of this LogFilter.

        Filter logs by a glob filter.  # noqa: E501

        :param glob: The glob of this LogFilter.  # noqa: E501
        :type: str
        """

        self._glob = glob

    @property
    def cluster_id(self):
        """Gets the cluster_id of this LogFilter.  # noqa: E501

        Filter logs by cluster_id.  # noqa: E501

        :return: The cluster_id of this LogFilter.  # noqa: E501
        :rtype: str
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id):
        """Sets the cluster_id of this LogFilter.

        Filter logs by cluster_id.  # noqa: E501

        :param cluster_id: The cluster_id of this LogFilter.  # noqa: E501
        :type: str
        """

        self._cluster_id = cluster_id

    @property
    def job_id(self):
        """Gets the job_id of this LogFilter.  # noqa: E501

        Filter logs by job_id (Anyscale Job ID).  # noqa: E501

        :return: The job_id of this LogFilter.  # noqa: E501
        :rtype: str
        """
        return self._job_id

    @job_id.setter
    def job_id(self, job_id):
        """Sets the job_id of this LogFilter.

        Filter logs by job_id (Anyscale Job ID).  # noqa: E501

        :param job_id: The job_id of this LogFilter.  # noqa: E501
        :type: str
        """

        self._job_id = job_id

    @property
    def job_run(self):
        """Gets the job_run of this LogFilter.  # noqa: E501

        Filter logs by job_run_id (Anyscale Job Run ID).  # noqa: E501

        :return: The job_run of this LogFilter.  # noqa: E501
        :rtype: str
        """
        return self._job_run

    @job_run.setter
    def job_run(self, job_run):
        """Sets the job_run of this LogFilter.

        Filter logs by job_run_id (Anyscale Job Run ID).  # noqa: E501

        :param job_run: The job_run of this LogFilter.  # noqa: E501
        :type: str
        """

        self._job_run = job_run

    @property
    def instance_id(self):
        """Gets the instance_id of this LogFilter.  # noqa: E501

        Filter logs by instance_id (Cloud Provider Instance ID).  # noqa: E501

        :return: The instance_id of this LogFilter.  # noqa: E501
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this LogFilter.

        Filter logs by instance_id (Cloud Provider Instance ID).  # noqa: E501

        :param instance_id: The instance_id of this LogFilter.  # noqa: E501
        :type: str
        """

        self._instance_id = instance_id

    @property
    def node_type(self):
        """Gets the node_type of this LogFilter.  # noqa: E501

        Filter logs by node_type (head-node, worker-nodes).  # noqa: E501

        :return: The node_type of this LogFilter.  # noqa: E501
        :rtype: NodeType
        """
        return self._node_type

    @node_type.setter
    def node_type(self, node_type):
        """Sets the node_type of this LogFilter.

        Filter logs by node_type (head-node, worker-nodes).  # noqa: E501

        :param node_type: The node_type of this LogFilter.  # noqa: E501
        :type: NodeType
        """

        self._node_type = node_type

    @property
    def process_id(self):
        """Gets the process_id of this LogFilter.  # noqa: E501

        Filter logs by process_id.  # noqa: E501

        :return: The process_id of this LogFilter.  # noqa: E501
        :rtype: str
        """
        return self._process_id

    @process_id.setter
    def process_id(self, process_id):
        """Sets the process_id of this LogFilter.

        Filter logs by process_id.  # noqa: E501

        :param process_id: The process_id of this LogFilter.  # noqa: E501
        :type: str
        """

        self._process_id = process_id

    @property
    def session_id(self):
        """Gets the session_id of this LogFilter.  # noqa: E501

        Filter logs by session_id.  # noqa: E501

        :return: The session_id of this LogFilter.  # noqa: E501
        :rtype: str
        """
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        """Sets the session_id of this LogFilter.

        Filter logs by session_id.  # noqa: E501

        :param session_id: The session_id of this LogFilter.  # noqa: E501
        :type: str
        """

        self._session_id = session_id

    @property
    def file_name(self):
        """Gets the file_name of this LogFilter.  # noqa: E501

        Filter logs by log file name.  # noqa: E501

        :return: The file_name of this LogFilter.  # noqa: E501
        :rtype: str
        """
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        """Sets the file_name of this LogFilter.

        Filter logs by log file name.  # noqa: E501

        :param file_name: The file_name of this LogFilter.  # noqa: E501
        :type: str
        """

        self._file_name = file_name

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
        if not isinstance(other, LogFilter):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, LogFilter):
            return True

        return self.to_dict() != other.to_dict()
