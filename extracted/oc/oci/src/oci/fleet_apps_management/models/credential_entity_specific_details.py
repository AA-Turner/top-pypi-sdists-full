# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20250228


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CredentialEntitySpecificDetails(object):
    """
    Credential specific Details.
    """

    #: A constant which can be used with the credential_level property of a CredentialEntitySpecificDetails.
    #: This constant has a value of "FLEET"
    CREDENTIAL_LEVEL_FLEET = "FLEET"

    #: A constant which can be used with the credential_level property of a CredentialEntitySpecificDetails.
    #: This constant has a value of "RESOURCE"
    CREDENTIAL_LEVEL_RESOURCE = "RESOURCE"

    #: A constant which can be used with the credential_level property of a CredentialEntitySpecificDetails.
    #: This constant has a value of "TARGET"
    CREDENTIAL_LEVEL_TARGET = "TARGET"

    def __init__(self, **kwargs):
        """
        Initializes a new CredentialEntitySpecificDetails object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.fleet_apps_management.models.TargetCredentialEntitySpecificDetails`
        * :class:`~oci.fleet_apps_management.models.FleetCredentialEntitySpecificDetails`
        * :class:`~oci.fleet_apps_management.models.ResourceCredentialEntitySpecificDetails`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param credential_level:
            The value to assign to the credential_level property of this CredentialEntitySpecificDetails.
            Allowed values for this property are: "FLEET", "RESOURCE", "TARGET", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type credential_level: str

        """
        self.swagger_types = {
            'credential_level': 'str'
        }
        self.attribute_map = {
            'credential_level': 'credentialLevel'
        }
        self._credential_level = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['credentialLevel']

        if type == 'TARGET':
            return 'TargetCredentialEntitySpecificDetails'

        if type == 'FLEET':
            return 'FleetCredentialEntitySpecificDetails'

        if type == 'RESOURCE':
            return 'ResourceCredentialEntitySpecificDetails'
        else:
            return 'CredentialEntitySpecificDetails'

    @property
    def credential_level(self):
        """
        **[Required]** Gets the credential_level of this CredentialEntitySpecificDetails.
        At what level the credential is provided?

        Allowed values for this property are: "FLEET", "RESOURCE", "TARGET", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The credential_level of this CredentialEntitySpecificDetails.
        :rtype: str
        """
        return self._credential_level

    @credential_level.setter
    def credential_level(self, credential_level):
        """
        Sets the credential_level of this CredentialEntitySpecificDetails.
        At what level the credential is provided?


        :param credential_level: The credential_level of this CredentialEntitySpecificDetails.
        :type: str
        """
        allowed_values = ["FLEET", "RESOURCE", "TARGET"]
        if not value_allowed_none_or_none_sentinel(credential_level, allowed_values):
            credential_level = 'UNKNOWN_ENUM_VALUE'
        self._credential_level = credential_level

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
