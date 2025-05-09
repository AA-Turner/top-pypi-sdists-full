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


class ResponseWorkloadInfo(object):
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
        'created_by': 'ResponseSimpleUser',
        'created_dt': 'datetime',
        'experiment': 'ResponseSimpleExperiment',
        'model_service_revision': 'ResponseModelServiceRevision',
        'project': 'ResponseSimpleProject',
        'run_execution': 'ResponseReducedRunExecution',
        'status': 'str',
        'type': 'str',
        'workspace': 'ResponseSimpleWorkspace'
    }

    attribute_map = {
        'created_by': 'created_by',
        'created_dt': 'created_dt',
        'experiment': 'experiment',
        'model_service_revision': 'model_service_revision',
        'project': 'project',
        'run_execution': 'run_execution',
        'status': 'status',
        'type': 'type',
        'workspace': 'workspace'
    }

    def __init__(self, created_by=None, created_dt=None, experiment=None, model_service_revision=None, project=None, run_execution=None, status=None, type=None, workspace=None, local_vars_configuration=None):  # noqa: E501
        """ResponseWorkloadInfo - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._created_by = None
        self._created_dt = None
        self._experiment = None
        self._model_service_revision = None
        self._project = None
        self._run_execution = None
        self._status = None
        self._type = None
        self._workspace = None
        self.discriminator = None

        self.created_by = created_by
        self.created_dt = created_dt
        if experiment is not None:
            self.experiment = experiment
        if model_service_revision is not None:
            self.model_service_revision = model_service_revision
        if project is not None:
            self.project = project
        if run_execution is not None:
            self.run_execution = run_execution
        if status is not None:
            self.status = status
        if type is not None:
            self.type = type
        if workspace is not None:
            self.workspace = workspace

    @property
    def created_by(self):
        """Gets the created_by of this ResponseWorkloadInfo.  # noqa: E501


        :return: The created_by of this ResponseWorkloadInfo.  # noqa: E501
        :rtype: ResponseSimpleUser
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this ResponseWorkloadInfo.


        :param created_by: The created_by of this ResponseWorkloadInfo.  # noqa: E501
        :type created_by: ResponseSimpleUser
        """
        if self.local_vars_configuration.client_side_validation and created_by is None:  # noqa: E501
            raise ValueError("Invalid value for `created_by`, must not be `None`")  # noqa: E501

        self._created_by = created_by

    @property
    def created_dt(self):
        """Gets the created_dt of this ResponseWorkloadInfo.  # noqa: E501


        :return: The created_dt of this ResponseWorkloadInfo.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this ResponseWorkloadInfo.


        :param created_dt: The created_dt of this ResponseWorkloadInfo.  # noqa: E501
        :type created_dt: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_dt is None:  # noqa: E501
            raise ValueError("Invalid value for `created_dt`, must not be `None`")  # noqa: E501

        self._created_dt = created_dt

    @property
    def experiment(self):
        """Gets the experiment of this ResponseWorkloadInfo.  # noqa: E501


        :return: The experiment of this ResponseWorkloadInfo.  # noqa: E501
        :rtype: ResponseSimpleExperiment
        """
        return self._experiment

    @experiment.setter
    def experiment(self, experiment):
        """Sets the experiment of this ResponseWorkloadInfo.


        :param experiment: The experiment of this ResponseWorkloadInfo.  # noqa: E501
        :type experiment: ResponseSimpleExperiment
        """

        self._experiment = experiment

    @property
    def model_service_revision(self):
        """Gets the model_service_revision of this ResponseWorkloadInfo.  # noqa: E501


        :return: The model_service_revision of this ResponseWorkloadInfo.  # noqa: E501
        :rtype: ResponseModelServiceRevision
        """
        return self._model_service_revision

    @model_service_revision.setter
    def model_service_revision(self, model_service_revision):
        """Sets the model_service_revision of this ResponseWorkloadInfo.


        :param model_service_revision: The model_service_revision of this ResponseWorkloadInfo.  # noqa: E501
        :type model_service_revision: ResponseModelServiceRevision
        """

        self._model_service_revision = model_service_revision

    @property
    def project(self):
        """Gets the project of this ResponseWorkloadInfo.  # noqa: E501


        :return: The project of this ResponseWorkloadInfo.  # noqa: E501
        :rtype: ResponseSimpleProject
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this ResponseWorkloadInfo.


        :param project: The project of this ResponseWorkloadInfo.  # noqa: E501
        :type project: ResponseSimpleProject
        """

        self._project = project

    @property
    def run_execution(self):
        """Gets the run_execution of this ResponseWorkloadInfo.  # noqa: E501


        :return: The run_execution of this ResponseWorkloadInfo.  # noqa: E501
        :rtype: ResponseReducedRunExecution
        """
        return self._run_execution

    @run_execution.setter
    def run_execution(self, run_execution):
        """Sets the run_execution of this ResponseWorkloadInfo.


        :param run_execution: The run_execution of this ResponseWorkloadInfo.  # noqa: E501
        :type run_execution: ResponseReducedRunExecution
        """

        self._run_execution = run_execution

    @property
    def status(self):
        """Gets the status of this ResponseWorkloadInfo.  # noqa: E501


        :return: The status of this ResponseWorkloadInfo.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ResponseWorkloadInfo.


        :param status: The status of this ResponseWorkloadInfo.  # noqa: E501
        :type status: str
        """

        self._status = status

    @property
    def type(self):
        """Gets the type of this ResponseWorkloadInfo.  # noqa: E501


        :return: The type of this ResponseWorkloadInfo.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ResponseWorkloadInfo.


        :param type: The type of this ResponseWorkloadInfo.  # noqa: E501
        :type type: str
        """

        self._type = type

    @property
    def workspace(self):
        """Gets the workspace of this ResponseWorkloadInfo.  # noqa: E501


        :return: The workspace of this ResponseWorkloadInfo.  # noqa: E501
        :rtype: ResponseSimpleWorkspace
        """
        return self._workspace

    @workspace.setter
    def workspace(self, workspace):
        """Sets the workspace of this ResponseWorkloadInfo.


        :param workspace: The workspace of this ResponseWorkloadInfo.  # noqa: E501
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
        if not isinstance(other, ResponseWorkloadInfo):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResponseWorkloadInfo):
            return True

        return self.to_dict() != other.to_dict()
