# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20190101

from .schedule_http_action_details import ScheduleHttpActionDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateJobRunScheduleActionDetails(ScheduleHttpActionDetails):
    """
    create job run details
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateJobRunScheduleActionDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.data_science.models.CreateJobRunScheduleActionDetails.http_action_type` attribute
        of this class is ``CREATE_JOB_RUN`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param http_action_type:
            The value to assign to the http_action_type property of this CreateJobRunScheduleActionDetails.
            Allowed values for this property are: "CREATE_JOB_RUN", "CREATE_PIPELINE_RUN", "INVOKE_ML_APPLICATION_PROVIDER_TRIGGER"
        :type http_action_type: str

        :param create_job_run_details:
            The value to assign to the create_job_run_details property of this CreateJobRunScheduleActionDetails.
        :type create_job_run_details: oci.data_science.models.CreateJobRunDetails

        """
        self.swagger_types = {
            'http_action_type': 'str',
            'create_job_run_details': 'CreateJobRunDetails'
        }
        self.attribute_map = {
            'http_action_type': 'httpActionType',
            'create_job_run_details': 'createJobRunDetails'
        }
        self._http_action_type = None
        self._create_job_run_details = None
        self._http_action_type = 'CREATE_JOB_RUN'

    @property
    def create_job_run_details(self):
        """
        **[Required]** Gets the create_job_run_details of this CreateJobRunScheduleActionDetails.

        :return: The create_job_run_details of this CreateJobRunScheduleActionDetails.
        :rtype: oci.data_science.models.CreateJobRunDetails
        """
        return self._create_job_run_details

    @create_job_run_details.setter
    def create_job_run_details(self, create_job_run_details):
        """
        Sets the create_job_run_details of this CreateJobRunScheduleActionDetails.

        :param create_job_run_details: The create_job_run_details of this CreateJobRunScheduleActionDetails.
        :type: oci.data_science.models.CreateJobRunDetails
        """
        self._create_job_run_details = create_job_run_details

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
