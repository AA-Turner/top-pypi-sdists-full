# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20190506


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class OdaPrivateEndpointAttachment(object):
    """
    ODA Private Endpoint Attachment is used to attach ODA Private Endpoint to ODA (Digital Assistant) Instance.
    """

    #: A constant which can be used with the lifecycle_state property of a OdaPrivateEndpointAttachment.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a OdaPrivateEndpointAttachment.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a OdaPrivateEndpointAttachment.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a OdaPrivateEndpointAttachment.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a OdaPrivateEndpointAttachment.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a OdaPrivateEndpointAttachment.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new OdaPrivateEndpointAttachment object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this OdaPrivateEndpointAttachment.
        :type id: str

        :param oda_instance_id:
            The value to assign to the oda_instance_id property of this OdaPrivateEndpointAttachment.
        :type oda_instance_id: str

        :param oda_private_endpoint_id:
            The value to assign to the oda_private_endpoint_id property of this OdaPrivateEndpointAttachment.
        :type oda_private_endpoint_id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this OdaPrivateEndpointAttachment.
        :type compartment_id: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this OdaPrivateEndpointAttachment.
            Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param time_created:
            The value to assign to the time_created property of this OdaPrivateEndpointAttachment.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this OdaPrivateEndpointAttachment.
        :type time_updated: datetime

        """
        self.swagger_types = {
            'id': 'str',
            'oda_instance_id': 'str',
            'oda_private_endpoint_id': 'str',
            'compartment_id': 'str',
            'lifecycle_state': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime'
        }
        self.attribute_map = {
            'id': 'id',
            'oda_instance_id': 'odaInstanceId',
            'oda_private_endpoint_id': 'odaPrivateEndpointId',
            'compartment_id': 'compartmentId',
            'lifecycle_state': 'lifecycleState',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated'
        }
        self._id = None
        self._oda_instance_id = None
        self._oda_private_endpoint_id = None
        self._compartment_id = None
        self._lifecycle_state = None
        self._time_created = None
        self._time_updated = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this OdaPrivateEndpointAttachment.
        The `OCID`__ of the ODA Private Endpoint Attachment.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The id of this OdaPrivateEndpointAttachment.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this OdaPrivateEndpointAttachment.
        The `OCID`__ of the ODA Private Endpoint Attachment.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param id: The id of this OdaPrivateEndpointAttachment.
        :type: str
        """
        self._id = id

    @property
    def oda_instance_id(self):
        """
        **[Required]** Gets the oda_instance_id of this OdaPrivateEndpointAttachment.
        The `OCID`__ of the attached ODA Instance.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The oda_instance_id of this OdaPrivateEndpointAttachment.
        :rtype: str
        """
        return self._oda_instance_id

    @oda_instance_id.setter
    def oda_instance_id(self, oda_instance_id):
        """
        Sets the oda_instance_id of this OdaPrivateEndpointAttachment.
        The `OCID`__ of the attached ODA Instance.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param oda_instance_id: The oda_instance_id of this OdaPrivateEndpointAttachment.
        :type: str
        """
        self._oda_instance_id = oda_instance_id

    @property
    def oda_private_endpoint_id(self):
        """
        **[Required]** Gets the oda_private_endpoint_id of this OdaPrivateEndpointAttachment.
        The `OCID`__ of the ODA Private Endpoint.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The oda_private_endpoint_id of this OdaPrivateEndpointAttachment.
        :rtype: str
        """
        return self._oda_private_endpoint_id

    @oda_private_endpoint_id.setter
    def oda_private_endpoint_id(self, oda_private_endpoint_id):
        """
        Sets the oda_private_endpoint_id of this OdaPrivateEndpointAttachment.
        The `OCID`__ of the ODA Private Endpoint.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param oda_private_endpoint_id: The oda_private_endpoint_id of this OdaPrivateEndpointAttachment.
        :type: str
        """
        self._oda_private_endpoint_id = oda_private_endpoint_id

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this OdaPrivateEndpointAttachment.
        The `OCID`__ of the compartment that the ODA private endpoint attachment belongs to.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this OdaPrivateEndpointAttachment.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this OdaPrivateEndpointAttachment.
        The `OCID`__ of the compartment that the ODA private endpoint attachment belongs to.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this OdaPrivateEndpointAttachment.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this OdaPrivateEndpointAttachment.
        The current state of the ODA Private Endpoint attachment.

        Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this OdaPrivateEndpointAttachment.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this OdaPrivateEndpointAttachment.
        The current state of the ODA Private Endpoint attachment.


        :param lifecycle_state: The lifecycle_state of this OdaPrivateEndpointAttachment.
        :type: str
        """
        allowed_values = ["CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this OdaPrivateEndpointAttachment.
        When the resource was created. A date-time string as described in `RFC 3339`__, section 14.29.

        __ https://tools.ietf.org/rfc/rfc3339


        :return: The time_created of this OdaPrivateEndpointAttachment.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this OdaPrivateEndpointAttachment.
        When the resource was created. A date-time string as described in `RFC 3339`__, section 14.29.

        __ https://tools.ietf.org/rfc/rfc3339


        :param time_created: The time_created of this OdaPrivateEndpointAttachment.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this OdaPrivateEndpointAttachment.
        When the resource was last updated. A date-time string as described in `RFC 3339`__, section 14.29.

        __ https://tools.ietf.org/rfc/rfc3339


        :return: The time_updated of this OdaPrivateEndpointAttachment.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this OdaPrivateEndpointAttachment.
        When the resource was last updated. A date-time string as described in `RFC 3339`__, section 14.29.

        __ https://tools.ietf.org/rfc/rfc3339


        :param time_updated: The time_updated of this OdaPrivateEndpointAttachment.
        :type: datetime
        """
        self._time_updated = time_updated

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
