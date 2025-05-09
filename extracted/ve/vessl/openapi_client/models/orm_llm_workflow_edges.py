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


class OrmLLMWorkflowEdges(object):
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
        'created_by': 'OrmUser',
        'default_resource_spec': 'OrmKernelResourceSpec',
        'llm_workflow_llm_user_group': 'list[OrmLLMWorkflowLLMUserGroup]',
        'model_service': 'OrmModelService',
        'organization': 'OrmOrganization',
        'revisions': 'list[OrmLLMWorkflowRevision]',
        'test_session_run_execution': 'OrmRunExecution'
    }

    attribute_map = {
        'created_by': 'created_by',
        'default_resource_spec': 'default_resource_spec',
        'llm_workflow_llm_user_group': 'llm_workflow_llm_user_group',
        'model_service': 'model_service',
        'organization': 'organization',
        'revisions': 'revisions',
        'test_session_run_execution': 'test_session_run_execution'
    }

    def __init__(self, created_by=None, default_resource_spec=None, llm_workflow_llm_user_group=None, model_service=None, organization=None, revisions=None, test_session_run_execution=None, local_vars_configuration=None):  # noqa: E501
        """OrmLLMWorkflowEdges - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._created_by = None
        self._default_resource_spec = None
        self._llm_workflow_llm_user_group = None
        self._model_service = None
        self._organization = None
        self._revisions = None
        self._test_session_run_execution = None
        self.discriminator = None

        if created_by is not None:
            self.created_by = created_by
        if default_resource_spec is not None:
            self.default_resource_spec = default_resource_spec
        if llm_workflow_llm_user_group is not None:
            self.llm_workflow_llm_user_group = llm_workflow_llm_user_group
        if model_service is not None:
            self.model_service = model_service
        if organization is not None:
            self.organization = organization
        if revisions is not None:
            self.revisions = revisions
        if test_session_run_execution is not None:
            self.test_session_run_execution = test_session_run_execution

    @property
    def created_by(self):
        """Gets the created_by of this OrmLLMWorkflowEdges.  # noqa: E501


        :return: The created_by of this OrmLLMWorkflowEdges.  # noqa: E501
        :rtype: OrmUser
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this OrmLLMWorkflowEdges.


        :param created_by: The created_by of this OrmLLMWorkflowEdges.  # noqa: E501
        :type created_by: OrmUser
        """

        self._created_by = created_by

    @property
    def default_resource_spec(self):
        """Gets the default_resource_spec of this OrmLLMWorkflowEdges.  # noqa: E501


        :return: The default_resource_spec of this OrmLLMWorkflowEdges.  # noqa: E501
        :rtype: OrmKernelResourceSpec
        """
        return self._default_resource_spec

    @default_resource_spec.setter
    def default_resource_spec(self, default_resource_spec):
        """Sets the default_resource_spec of this OrmLLMWorkflowEdges.


        :param default_resource_spec: The default_resource_spec of this OrmLLMWorkflowEdges.  # noqa: E501
        :type default_resource_spec: OrmKernelResourceSpec
        """

        self._default_resource_spec = default_resource_spec

    @property
    def llm_workflow_llm_user_group(self):
        """Gets the llm_workflow_llm_user_group of this OrmLLMWorkflowEdges.  # noqa: E501


        :return: The llm_workflow_llm_user_group of this OrmLLMWorkflowEdges.  # noqa: E501
        :rtype: list[OrmLLMWorkflowLLMUserGroup]
        """
        return self._llm_workflow_llm_user_group

    @llm_workflow_llm_user_group.setter
    def llm_workflow_llm_user_group(self, llm_workflow_llm_user_group):
        """Sets the llm_workflow_llm_user_group of this OrmLLMWorkflowEdges.


        :param llm_workflow_llm_user_group: The llm_workflow_llm_user_group of this OrmLLMWorkflowEdges.  # noqa: E501
        :type llm_workflow_llm_user_group: list[OrmLLMWorkflowLLMUserGroup]
        """

        self._llm_workflow_llm_user_group = llm_workflow_llm_user_group

    @property
    def model_service(self):
        """Gets the model_service of this OrmLLMWorkflowEdges.  # noqa: E501


        :return: The model_service of this OrmLLMWorkflowEdges.  # noqa: E501
        :rtype: OrmModelService
        """
        return self._model_service

    @model_service.setter
    def model_service(self, model_service):
        """Sets the model_service of this OrmLLMWorkflowEdges.


        :param model_service: The model_service of this OrmLLMWorkflowEdges.  # noqa: E501
        :type model_service: OrmModelService
        """

        self._model_service = model_service

    @property
    def organization(self):
        """Gets the organization of this OrmLLMWorkflowEdges.  # noqa: E501


        :return: The organization of this OrmLLMWorkflowEdges.  # noqa: E501
        :rtype: OrmOrganization
        """
        return self._organization

    @organization.setter
    def organization(self, organization):
        """Sets the organization of this OrmLLMWorkflowEdges.


        :param organization: The organization of this OrmLLMWorkflowEdges.  # noqa: E501
        :type organization: OrmOrganization
        """

        self._organization = organization

    @property
    def revisions(self):
        """Gets the revisions of this OrmLLMWorkflowEdges.  # noqa: E501


        :return: The revisions of this OrmLLMWorkflowEdges.  # noqa: E501
        :rtype: list[OrmLLMWorkflowRevision]
        """
        return self._revisions

    @revisions.setter
    def revisions(self, revisions):
        """Sets the revisions of this OrmLLMWorkflowEdges.


        :param revisions: The revisions of this OrmLLMWorkflowEdges.  # noqa: E501
        :type revisions: list[OrmLLMWorkflowRevision]
        """

        self._revisions = revisions

    @property
    def test_session_run_execution(self):
        """Gets the test_session_run_execution of this OrmLLMWorkflowEdges.  # noqa: E501


        :return: The test_session_run_execution of this OrmLLMWorkflowEdges.  # noqa: E501
        :rtype: OrmRunExecution
        """
        return self._test_session_run_execution

    @test_session_run_execution.setter
    def test_session_run_execution(self, test_session_run_execution):
        """Sets the test_session_run_execution of this OrmLLMWorkflowEdges.


        :param test_session_run_execution: The test_session_run_execution of this OrmLLMWorkflowEdges.  # noqa: E501
        :type test_session_run_execution: OrmRunExecution
        """

        self._test_session_run_execution = test_session_run_execution

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
        if not isinstance(other, OrmLLMWorkflowEdges):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrmLLMWorkflowEdges):
            return True

        return self.to_dict() != other.to_dict()
