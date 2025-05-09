# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20220901


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RebootEventData(object):
    """
    Provides additional information for a reboot event.
    """

    #: A constant which can be used with the reboot_status property of a RebootEventData.
    #: This constant has a value of "REBOOT_STARTED"
    REBOOT_STATUS_REBOOT_STARTED = "REBOOT_STARTED"

    #: A constant which can be used with the reboot_status property of a RebootEventData.
    #: This constant has a value of "REBOOT_SUCCEEDED"
    REBOOT_STATUS_REBOOT_SUCCEEDED = "REBOOT_SUCCEEDED"

    #: A constant which can be used with the reboot_status property of a RebootEventData.
    #: This constant has a value of "REBOOT_FAILED"
    REBOOT_STATUS_REBOOT_FAILED = "REBOOT_FAILED"

    #: A constant which can be used with the reboot_status property of a RebootEventData.
    #: This constant has a value of "REBOOT_SUCCEEDED_AFTER_TIMEOUT"
    REBOOT_STATUS_REBOOT_SUCCEEDED_AFTER_TIMEOUT = "REBOOT_SUCCEEDED_AFTER_TIMEOUT"

    def __init__(self, **kwargs):
        """
        Initializes a new RebootEventData object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param reboot_status:
            The value to assign to the reboot_status property of this RebootEventData.
            Allowed values for this property are: "REBOOT_STARTED", "REBOOT_SUCCEEDED", "REBOOT_FAILED", "REBOOT_SUCCEEDED_AFTER_TIMEOUT", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type reboot_status: str

        :param additional_details:
            The value to assign to the additional_details property of this RebootEventData.
        :type additional_details: oci.os_management_hub.models.WorkRequestEventDataAdditionalDetails

        """
        self.swagger_types = {
            'reboot_status': 'str',
            'additional_details': 'WorkRequestEventDataAdditionalDetails'
        }
        self.attribute_map = {
            'reboot_status': 'rebootStatus',
            'additional_details': 'additionalDetails'
        }
        self._reboot_status = None
        self._additional_details = None

    @property
    def reboot_status(self):
        """
        **[Required]** Gets the reboot_status of this RebootEventData.
        Reboot status for the current event

        Allowed values for this property are: "REBOOT_STARTED", "REBOOT_SUCCEEDED", "REBOOT_FAILED", "REBOOT_SUCCEEDED_AFTER_TIMEOUT", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The reboot_status of this RebootEventData.
        :rtype: str
        """
        return self._reboot_status

    @reboot_status.setter
    def reboot_status(self, reboot_status):
        """
        Sets the reboot_status of this RebootEventData.
        Reboot status for the current event


        :param reboot_status: The reboot_status of this RebootEventData.
        :type: str
        """
        allowed_values = ["REBOOT_STARTED", "REBOOT_SUCCEEDED", "REBOOT_FAILED", "REBOOT_SUCCEEDED_AFTER_TIMEOUT"]
        if not value_allowed_none_or_none_sentinel(reboot_status, allowed_values):
            reboot_status = 'UNKNOWN_ENUM_VALUE'
        self._reboot_status = reboot_status

    @property
    def additional_details(self):
        """
        Gets the additional_details of this RebootEventData.

        :return: The additional_details of this RebootEventData.
        :rtype: oci.os_management_hub.models.WorkRequestEventDataAdditionalDetails
        """
        return self._additional_details

    @additional_details.setter
    def additional_details(self, additional_details):
        """
        Sets the additional_details of this RebootEventData.

        :param additional_details: The additional_details of this RebootEventData.
        :type: oci.os_management_hub.models.WorkRequestEventDataAdditionalDetails
        """
        self._additional_details = additional_details

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
