# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20250228


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SetDefaultRunbookDetails(object):
    """
    Request to set default Runbook
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SetDefaultRunbookDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param runbook_id:
            The value to assign to the runbook_id property of this SetDefaultRunbookDetails.
        :type runbook_id: str

        """
        self.swagger_types = {
            'runbook_id': 'str'
        }
        self.attribute_map = {
            'runbook_id': 'runbookId'
        }
        self._runbook_id = None

    @property
    def runbook_id(self):
        """
        **[Required]** Gets the runbook_id of this SetDefaultRunbookDetails.
        The OCID of the resource.


        :return: The runbook_id of this SetDefaultRunbookDetails.
        :rtype: str
        """
        return self._runbook_id

    @runbook_id.setter
    def runbook_id(self, runbook_id):
        """
        Sets the runbook_id of this SetDefaultRunbookDetails.
        The OCID of the resource.


        :param runbook_id: The runbook_id of this SetDefaultRunbookDetails.
        :type: str
        """
        self._runbook_id = runbook_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
