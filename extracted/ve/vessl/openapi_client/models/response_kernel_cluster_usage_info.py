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


class ResponseKernelClusterUsageInfo(object):
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
        'cpu_device_hours': 'float',
        'cpu_limit': 'float',
        'created_by': 'ResponseSimpleUser',
        'created_dt': 'datetime',
        'experiment': 'ResponseSimpleExperiment',
        'gpu_device_hours': 'float',
        'gpu_limit': 'int',
        'gpu_type': 'str',
        'memory_limit': 'str',
        'name': 'str',
        'organization': 'ResponseOrganization',
        'path': 'str',
        'project': 'ResponseSimpleProject',
        'resource_type': 'str',
        'run_execution': 'ResponseReducedRunExecution',
        'status': 'str',
        'workload_type': 'str',
        'workspace': 'ResponseSimpleWorkspace'
    }

    attribute_map = {
        'cpu_device_hours': 'cpu_device_hours',
        'cpu_limit': 'cpu_limit',
        'created_by': 'created_by',
        'created_dt': 'created_dt',
        'experiment': 'experiment',
        'gpu_device_hours': 'gpu_device_hours',
        'gpu_limit': 'gpu_limit',
        'gpu_type': 'gpu_type',
        'memory_limit': 'memory_limit',
        'name': 'name',
        'organization': 'organization',
        'path': 'path',
        'project': 'project',
        'resource_type': 'resource_type',
        'run_execution': 'run_execution',
        'status': 'status',
        'workload_type': 'workload_type',
        'workspace': 'workspace'
    }

    def __init__(self, cpu_device_hours=None, cpu_limit=None, created_by=None, created_dt=None, experiment=None, gpu_device_hours=None, gpu_limit=None, gpu_type=None, memory_limit=None, name=None, organization=None, path=None, project=None, resource_type=None, run_execution=None, status=None, workload_type=None, workspace=None, local_vars_configuration=None):  # noqa: E501
        """ResponseKernelClusterUsageInfo - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._cpu_device_hours = None
        self._cpu_limit = None
        self._created_by = None
        self._created_dt = None
        self._experiment = None
        self._gpu_device_hours = None
        self._gpu_limit = None
        self._gpu_type = None
        self._memory_limit = None
        self._name = None
        self._organization = None
        self._path = None
        self._project = None
        self._resource_type = None
        self._run_execution = None
        self._status = None
        self._workload_type = None
        self._workspace = None
        self.discriminator = None

        if cpu_device_hours is not None:
            self.cpu_device_hours = cpu_device_hours
        self.cpu_limit = cpu_limit
        self.created_by = created_by
        self.created_dt = created_dt
        if experiment is not None:
            self.experiment = experiment
        if gpu_device_hours is not None:
            self.gpu_device_hours = gpu_device_hours
        self.gpu_limit = gpu_limit
        self.gpu_type = gpu_type
        self.memory_limit = memory_limit
        self.name = name
        self.organization = organization
        self.path = path
        self.project = project
        self.resource_type = resource_type
        if run_execution is not None:
            self.run_execution = run_execution
        self.status = status
        self.workload_type = workload_type
        if workspace is not None:
            self.workspace = workspace

    @property
    def cpu_device_hours(self):
        """Gets the cpu_device_hours of this ResponseKernelClusterUsageInfo.  # noqa: E501


        :return: The cpu_device_hours of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :rtype: float
        """
        return self._cpu_device_hours

    @cpu_device_hours.setter
    def cpu_device_hours(self, cpu_device_hours):
        """Sets the cpu_device_hours of this ResponseKernelClusterUsageInfo.


        :param cpu_device_hours: The cpu_device_hours of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :type cpu_device_hours: float
        """

        self._cpu_device_hours = cpu_device_hours

    @property
    def cpu_limit(self):
        """Gets the cpu_limit of this ResponseKernelClusterUsageInfo.  # noqa: E501


        :return: The cpu_limit of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :rtype: float
        """
        return self._cpu_limit

    @cpu_limit.setter
    def cpu_limit(self, cpu_limit):
        """Sets the cpu_limit of this ResponseKernelClusterUsageInfo.


        :param cpu_limit: The cpu_limit of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :type cpu_limit: float
        """

        self._cpu_limit = cpu_limit

    @property
    def created_by(self):
        """Gets the created_by of this ResponseKernelClusterUsageInfo.  # noqa: E501


        :return: The created_by of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :rtype: ResponseSimpleUser
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this ResponseKernelClusterUsageInfo.


        :param created_by: The created_by of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :type created_by: ResponseSimpleUser
        """
        if self.local_vars_configuration.client_side_validation and created_by is None:  # noqa: E501
            raise ValueError("Invalid value for `created_by`, must not be `None`")  # noqa: E501

        self._created_by = created_by

    @property
    def created_dt(self):
        """Gets the created_dt of this ResponseKernelClusterUsageInfo.  # noqa: E501


        :return: The created_dt of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this ResponseKernelClusterUsageInfo.


        :param created_dt: The created_dt of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :type created_dt: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_dt is None:  # noqa: E501
            raise ValueError("Invalid value for `created_dt`, must not be `None`")  # noqa: E501

        self._created_dt = created_dt

    @property
    def experiment(self):
        """Gets the experiment of this ResponseKernelClusterUsageInfo.  # noqa: E501


        :return: The experiment of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :rtype: ResponseSimpleExperiment
        """
        return self._experiment

    @experiment.setter
    def experiment(self, experiment):
        """Sets the experiment of this ResponseKernelClusterUsageInfo.


        :param experiment: The experiment of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :type experiment: ResponseSimpleExperiment
        """

        self._experiment = experiment

    @property
    def gpu_device_hours(self):
        """Gets the gpu_device_hours of this ResponseKernelClusterUsageInfo.  # noqa: E501


        :return: The gpu_device_hours of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :rtype: float
        """
        return self._gpu_device_hours

    @gpu_device_hours.setter
    def gpu_device_hours(self, gpu_device_hours):
        """Sets the gpu_device_hours of this ResponseKernelClusterUsageInfo.


        :param gpu_device_hours: The gpu_device_hours of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :type gpu_device_hours: float
        """

        self._gpu_device_hours = gpu_device_hours

    @property
    def gpu_limit(self):
        """Gets the gpu_limit of this ResponseKernelClusterUsageInfo.  # noqa: E501


        :return: The gpu_limit of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :rtype: int
        """
        return self._gpu_limit

    @gpu_limit.setter
    def gpu_limit(self, gpu_limit):
        """Sets the gpu_limit of this ResponseKernelClusterUsageInfo.


        :param gpu_limit: The gpu_limit of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :type gpu_limit: int
        """

        self._gpu_limit = gpu_limit

    @property
    def gpu_type(self):
        """Gets the gpu_type of this ResponseKernelClusterUsageInfo.  # noqa: E501


        :return: The gpu_type of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :rtype: str
        """
        return self._gpu_type

    @gpu_type.setter
    def gpu_type(self, gpu_type):
        """Sets the gpu_type of this ResponseKernelClusterUsageInfo.


        :param gpu_type: The gpu_type of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :type gpu_type: str
        """

        self._gpu_type = gpu_type

    @property
    def memory_limit(self):
        """Gets the memory_limit of this ResponseKernelClusterUsageInfo.  # noqa: E501


        :return: The memory_limit of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :rtype: str
        """
        return self._memory_limit

    @memory_limit.setter
    def memory_limit(self, memory_limit):
        """Sets the memory_limit of this ResponseKernelClusterUsageInfo.


        :param memory_limit: The memory_limit of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :type memory_limit: str
        """

        self._memory_limit = memory_limit

    @property
    def name(self):
        """Gets the name of this ResponseKernelClusterUsageInfo.  # noqa: E501


        :return: The name of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ResponseKernelClusterUsageInfo.


        :param name: The name of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def organization(self):
        """Gets the organization of this ResponseKernelClusterUsageInfo.  # noqa: E501


        :return: The organization of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :rtype: ResponseOrganization
        """
        return self._organization

    @organization.setter
    def organization(self, organization):
        """Sets the organization of this ResponseKernelClusterUsageInfo.


        :param organization: The organization of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :type organization: ResponseOrganization
        """
        if self.local_vars_configuration.client_side_validation and organization is None:  # noqa: E501
            raise ValueError("Invalid value for `organization`, must not be `None`")  # noqa: E501

        self._organization = organization

    @property
    def path(self):
        """Gets the path of this ResponseKernelClusterUsageInfo.  # noqa: E501


        :return: The path of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this ResponseKernelClusterUsageInfo.


        :param path: The path of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :type path: str
        """
        if self.local_vars_configuration.client_side_validation and path is None:  # noqa: E501
            raise ValueError("Invalid value for `path`, must not be `None`")  # noqa: E501

        self._path = path

    @property
    def project(self):
        """Gets the project of this ResponseKernelClusterUsageInfo.  # noqa: E501


        :return: The project of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :rtype: ResponseSimpleProject
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this ResponseKernelClusterUsageInfo.


        :param project: The project of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :type project: ResponseSimpleProject
        """
        if self.local_vars_configuration.client_side_validation and project is None:  # noqa: E501
            raise ValueError("Invalid value for `project`, must not be `None`")  # noqa: E501

        self._project = project

    @property
    def resource_type(self):
        """Gets the resource_type of this ResponseKernelClusterUsageInfo.  # noqa: E501


        :return: The resource_type of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :rtype: str
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type):
        """Sets the resource_type of this ResponseKernelClusterUsageInfo.


        :param resource_type: The resource_type of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :type resource_type: str
        """
        if self.local_vars_configuration.client_side_validation and resource_type is None:  # noqa: E501
            raise ValueError("Invalid value for `resource_type`, must not be `None`")  # noqa: E501

        self._resource_type = resource_type

    @property
    def run_execution(self):
        """Gets the run_execution of this ResponseKernelClusterUsageInfo.  # noqa: E501


        :return: The run_execution of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :rtype: ResponseReducedRunExecution
        """
        return self._run_execution

    @run_execution.setter
    def run_execution(self, run_execution):
        """Sets the run_execution of this ResponseKernelClusterUsageInfo.


        :param run_execution: The run_execution of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :type run_execution: ResponseReducedRunExecution
        """

        self._run_execution = run_execution

    @property
    def status(self):
        """Gets the status of this ResponseKernelClusterUsageInfo.  # noqa: E501


        :return: The status of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ResponseKernelClusterUsageInfo.


        :param status: The status of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :type status: str
        """
        if self.local_vars_configuration.client_side_validation and status is None:  # noqa: E501
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def workload_type(self):
        """Gets the workload_type of this ResponseKernelClusterUsageInfo.  # noqa: E501


        :return: The workload_type of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :rtype: str
        """
        return self._workload_type

    @workload_type.setter
    def workload_type(self, workload_type):
        """Sets the workload_type of this ResponseKernelClusterUsageInfo.


        :param workload_type: The workload_type of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :type workload_type: str
        """
        if self.local_vars_configuration.client_side_validation and workload_type is None:  # noqa: E501
            raise ValueError("Invalid value for `workload_type`, must not be `None`")  # noqa: E501

        self._workload_type = workload_type

    @property
    def workspace(self):
        """Gets the workspace of this ResponseKernelClusterUsageInfo.  # noqa: E501


        :return: The workspace of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :rtype: ResponseSimpleWorkspace
        """
        return self._workspace

    @workspace.setter
    def workspace(self, workspace):
        """Sets the workspace of this ResponseKernelClusterUsageInfo.


        :param workspace: The workspace of this ResponseKernelClusterUsageInfo.  # noqa: E501
        :type workspace: ResponseSimpleWorkspace
        """

        self._workspace = workspace

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
        if not isinstance(other, ResponseKernelClusterUsageInfo):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResponseKernelClusterUsageInfo):
            return True

        return self.to_dict() != other.to_dict()
