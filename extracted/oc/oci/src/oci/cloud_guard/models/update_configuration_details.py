# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20200131


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateConfigurationDetails(object):
    """
    Parameters to update Cloud Guard configuration details for a tenancy.
    """

    #: A constant which can be used with the status property of a UpdateConfigurationDetails.
    #: This constant has a value of "ENABLED"
    STATUS_ENABLED = "ENABLED"

    #: A constant which can be used with the status property of a UpdateConfigurationDetails.
    #: This constant has a value of "DISABLED"
    STATUS_DISABLED = "DISABLED"

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateConfigurationDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param reporting_region:
            The value to assign to the reporting_region property of this UpdateConfigurationDetails.
        :type reporting_region: str

        :param status:
            The value to assign to the status property of this UpdateConfigurationDetails.
            Allowed values for this property are: "ENABLED", "DISABLED"
        :type status: str

        :param service_configurations:
            The value to assign to the service_configurations property of this UpdateConfigurationDetails.
        :type service_configurations: list[oci.cloud_guard.models.ServiceConfiguration]

        :param self_manage_resources:
            The value to assign to the self_manage_resources property of this UpdateConfigurationDetails.
        :type self_manage_resources: bool

        """
        self.swagger_types = {
            'reporting_region': 'str',
            'status': 'str',
            'service_configurations': 'list[ServiceConfiguration]',
            'self_manage_resources': 'bool'
        }
        self.attribute_map = {
            'reporting_region': 'reportingRegion',
            'status': 'status',
            'service_configurations': 'serviceConfigurations',
            'self_manage_resources': 'selfManageResources'
        }
        self._reporting_region = None
        self._status = None
        self._service_configurations = None
        self._self_manage_resources = None

    @property
    def reporting_region(self):
        """
        **[Required]** Gets the reporting_region of this UpdateConfigurationDetails.
        The reporting region


        :return: The reporting_region of this UpdateConfigurationDetails.
        :rtype: str
        """
        return self._reporting_region

    @reporting_region.setter
    def reporting_region(self, reporting_region):
        """
        Sets the reporting_region of this UpdateConfigurationDetails.
        The reporting region


        :param reporting_region: The reporting_region of this UpdateConfigurationDetails.
        :type: str
        """
        self._reporting_region = reporting_region

    @property
    def status(self):
        """
        **[Required]** Gets the status of this UpdateConfigurationDetails.
        Status of Cloud Guard tenant

        Allowed values for this property are: "ENABLED", "DISABLED"


        :return: The status of this UpdateConfigurationDetails.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this UpdateConfigurationDetails.
        Status of Cloud Guard tenant


        :param status: The status of this UpdateConfigurationDetails.
        :type: str
        """
        allowed_values = ["ENABLED", "DISABLED"]
        if not value_allowed_none_or_none_sentinel(status, allowed_values):
            raise ValueError(
                f"Invalid value for `status`, must be None or one of {allowed_values}"
            )
        self._status = status

    @property
    def service_configurations(self):
        """
        Gets the service_configurations of this UpdateConfigurationDetails.
        List of service configurations for tenant


        :return: The service_configurations of this UpdateConfigurationDetails.
        :rtype: list[oci.cloud_guard.models.ServiceConfiguration]
        """
        return self._service_configurations

    @service_configurations.setter
    def service_configurations(self, service_configurations):
        """
        Sets the service_configurations of this UpdateConfigurationDetails.
        List of service configurations for tenant


        :param service_configurations: The service_configurations of this UpdateConfigurationDetails.
        :type: list[oci.cloud_guard.models.ServiceConfiguration]
        """
        self._service_configurations = service_configurations

    @property
    def self_manage_resources(self):
        """
        Gets the self_manage_resources of this UpdateConfigurationDetails.
        Identifies if Oracle managed resources will be created by customers.
        If no value is specified false is the default.


        :return: The self_manage_resources of this UpdateConfigurationDetails.
        :rtype: bool
        """
        return self._self_manage_resources

    @self_manage_resources.setter
    def self_manage_resources(self, self_manage_resources):
        """
        Sets the self_manage_resources of this UpdateConfigurationDetails.
        Identifies if Oracle managed resources will be created by customers.
        If no value is specified false is the default.


        :param self_manage_resources: The self_manage_resources of this UpdateConfigurationDetails.
        :type: bool
        """
        self._self_manage_resources = self_manage_resources

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
