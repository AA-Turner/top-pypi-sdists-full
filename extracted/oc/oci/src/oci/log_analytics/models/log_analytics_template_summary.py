# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20200601


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class LogAnalyticsTemplateSummary(object):
    """
    Summary of a template object.
    """

    #: A constant which can be used with the lifecycle_state property of a LogAnalyticsTemplateSummary.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a LogAnalyticsTemplateSummary.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    def __init__(self, **kwargs):
        """
        Initializes a new LogAnalyticsTemplateSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this LogAnalyticsTemplateSummary.
        :type id: str

        :param description:
            The value to assign to the description property of this LogAnalyticsTemplateSummary.
        :type description: str

        :param compartment_id:
            The value to assign to the compartment_id property of this LogAnalyticsTemplateSummary.
        :type compartment_id: str

        :param time_created:
            The value to assign to the time_created property of this LogAnalyticsTemplateSummary.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this LogAnalyticsTemplateSummary.
        :type time_updated: datetime

        :param freeform_tags:
            The value to assign to the freeform_tags property of this LogAnalyticsTemplateSummary.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this LogAnalyticsTemplateSummary.
        :type defined_tags: dict(str, dict(str, object))

        :param name:
            The value to assign to the name property of this LogAnalyticsTemplateSummary.
        :type name: str

        :param type:
            The value to assign to the type property of this LogAnalyticsTemplateSummary.
        :type type: str

        :param is_system:
            The value to assign to the is_system property of this LogAnalyticsTemplateSummary.
        :type is_system: bool

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this LogAnalyticsTemplateSummary.
            Allowed values for this property are: "ACTIVE", "DELETED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param facets:
            The value to assign to the facets property of this LogAnalyticsTemplateSummary.
        :type facets: list[oci.log_analytics.models.TemplateFacet]

        """
        self.swagger_types = {
            'id': 'str',
            'description': 'str',
            'compartment_id': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'name': 'str',
            'type': 'str',
            'is_system': 'bool',
            'lifecycle_state': 'str',
            'facets': 'list[TemplateFacet]'
        }
        self.attribute_map = {
            'id': 'id',
            'description': 'description',
            'compartment_id': 'compartmentId',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'name': 'name',
            'type': 'type',
            'is_system': 'isSystem',
            'lifecycle_state': 'lifecycleState',
            'facets': 'facets'
        }
        self._id = None
        self._description = None
        self._compartment_id = None
        self._time_created = None
        self._time_updated = None
        self._freeform_tags = None
        self._defined_tags = None
        self._name = None
        self._type = None
        self._is_system = None
        self._lifecycle_state = None
        self._facets = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this LogAnalyticsTemplateSummary.
        The log analytics entity OCID. This ID is a reference used by log analytics features and it represents
        a resource that is provisioned and managed by the customer on their premises or on the cloud.


        :return: The id of this LogAnalyticsTemplateSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this LogAnalyticsTemplateSummary.
        The log analytics entity OCID. This ID is a reference used by log analytics features and it represents
        a resource that is provisioned and managed by the customer on their premises or on the cloud.


        :param id: The id of this LogAnalyticsTemplateSummary.
        :type: str
        """
        self._id = id

    @property
    def description(self):
        """
        Gets the description of this LogAnalyticsTemplateSummary.
        Description for this resource.


        :return: The description of this LogAnalyticsTemplateSummary.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this LogAnalyticsTemplateSummary.
        Description for this resource.


        :param description: The description of this LogAnalyticsTemplateSummary.
        :type: str
        """
        self._description = description

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this LogAnalyticsTemplateSummary.
        Compartment Identifier `OCID]`__.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this LogAnalyticsTemplateSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this LogAnalyticsTemplateSummary.
        Compartment Identifier `OCID]`__.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this LogAnalyticsTemplateSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this LogAnalyticsTemplateSummary.
        The date and time the resource was created, in the format defined by RFC3339.


        :return: The time_created of this LogAnalyticsTemplateSummary.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this LogAnalyticsTemplateSummary.
        The date and time the resource was created, in the format defined by RFC3339.


        :param time_created: The time_created of this LogAnalyticsTemplateSummary.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this LogAnalyticsTemplateSummary.
        The date and time the resource was last updated, in the format defined by RFC3339.


        :return: The time_updated of this LogAnalyticsTemplateSummary.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this LogAnalyticsTemplateSummary.
        The date and time the resource was last updated, in the format defined by RFC3339.


        :param time_updated: The time_updated of this LogAnalyticsTemplateSummary.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this LogAnalyticsTemplateSummary.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this LogAnalyticsTemplateSummary.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this LogAnalyticsTemplateSummary.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this LogAnalyticsTemplateSummary.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this LogAnalyticsTemplateSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this LogAnalyticsTemplateSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this LogAnalyticsTemplateSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this LogAnalyticsTemplateSummary.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def name(self):
        """
        **[Required]** Gets the name of this LogAnalyticsTemplateSummary.
        The template name.


        :return: The name of this LogAnalyticsTemplateSummary.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this LogAnalyticsTemplateSummary.
        The template name.


        :param name: The name of this LogAnalyticsTemplateSummary.
        :type: str
        """
        self._name = name

    @property
    def type(self):
        """
        Gets the type of this LogAnalyticsTemplateSummary.
        The template type.


        :return: The type of this LogAnalyticsTemplateSummary.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this LogAnalyticsTemplateSummary.
        The template type.


        :param type: The type of this LogAnalyticsTemplateSummary.
        :type: str
        """
        self._type = type

    @property
    def is_system(self):
        """
        Gets the is_system of this LogAnalyticsTemplateSummary.
        The system flag.  A value of false denotes a custom, or user
        defined object.  A value of true denotes a built in object.


        :return: The is_system of this LogAnalyticsTemplateSummary.
        :rtype: bool
        """
        return self._is_system

    @is_system.setter
    def is_system(self, is_system):
        """
        Sets the is_system of this LogAnalyticsTemplateSummary.
        The system flag.  A value of false denotes a custom, or user
        defined object.  A value of true denotes a built in object.


        :param is_system: The is_system of this LogAnalyticsTemplateSummary.
        :type: bool
        """
        self._is_system = is_system

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this LogAnalyticsTemplateSummary.
        The current state of the template.

        Allowed values for this property are: "ACTIVE", "DELETED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this LogAnalyticsTemplateSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this LogAnalyticsTemplateSummary.
        The current state of the template.


        :param lifecycle_state: The lifecycle_state of this LogAnalyticsTemplateSummary.
        :type: str
        """
        allowed_values = ["ACTIVE", "DELETED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def facets(self):
        """
        Gets the facets of this LogAnalyticsTemplateSummary.
        Facets of the template


        :return: The facets of this LogAnalyticsTemplateSummary.
        :rtype: list[oci.log_analytics.models.TemplateFacet]
        """
        return self._facets

    @facets.setter
    def facets(self, facets):
        """
        Sets the facets of this LogAnalyticsTemplateSummary.
        Facets of the template


        :param facets: The facets of this LogAnalyticsTemplateSummary.
        :type: list[oci.log_analytics.models.TemplateFacet]
        """
        self._facets = facets

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
