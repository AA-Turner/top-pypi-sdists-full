# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20200601


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class VerifyOutput(object):
    """
    Verify acceleration output.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new VerifyOutput object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param scheduled_task_id:
            The value to assign to the scheduled_task_id property of this VerifyOutput.
        :type scheduled_task_id: str

        :param response_time_in_ms:
            The value to assign to the response_time_in_ms property of this VerifyOutput.
        :type response_time_in_ms: int

        :param total_matched_count:
            The value to assign to the total_matched_count property of this VerifyOutput.
        :type total_matched_count: int

        :param total_count:
            The value to assign to the total_count property of this VerifyOutput.
        :type total_count: int

        :param columns:
            The value to assign to the columns property of this VerifyOutput.
        :type columns: list[oci.log_analytics.models.ResultColumn]

        :param results:
            The value to assign to the results property of this VerifyOutput.
        :type results: list[dict(str, object)]

        """
        self.swagger_types = {
            'scheduled_task_id': 'str',
            'response_time_in_ms': 'int',
            'total_matched_count': 'int',
            'total_count': 'int',
            'columns': 'list[ResultColumn]',
            'results': 'list[dict(str, object)]'
        }
        self.attribute_map = {
            'scheduled_task_id': 'scheduledTaskId',
            'response_time_in_ms': 'responseTimeInMs',
            'total_matched_count': 'totalMatchedCount',
            'total_count': 'totalCount',
            'columns': 'columns',
            'results': 'results'
        }
        self._scheduled_task_id = None
        self._response_time_in_ms = None
        self._total_matched_count = None
        self._total_count = None
        self._columns = None
        self._results = None

    @property
    def scheduled_task_id(self):
        """
        **[Required]** Gets the scheduled_task_id of this VerifyOutput.
        Acceleration task identifier.


        :return: The scheduled_task_id of this VerifyOutput.
        :rtype: str
        """
        return self._scheduled_task_id

    @scheduled_task_id.setter
    def scheduled_task_id(self, scheduled_task_id):
        """
        Sets the scheduled_task_id of this VerifyOutput.
        Acceleration task identifier.


        :param scheduled_task_id: The scheduled_task_id of this VerifyOutput.
        :type: str
        """
        self._scheduled_task_id = scheduled_task_id

    @property
    def response_time_in_ms(self):
        """
        **[Required]** Gets the response_time_in_ms of this VerifyOutput.
        Response time in ms.


        :return: The response_time_in_ms of this VerifyOutput.
        :rtype: int
        """
        return self._response_time_in_ms

    @response_time_in_ms.setter
    def response_time_in_ms(self, response_time_in_ms):
        """
        Sets the response_time_in_ms of this VerifyOutput.
        Response time in ms.


        :param response_time_in_ms: The response_time_in_ms of this VerifyOutput.
        :type: int
        """
        self._response_time_in_ms = response_time_in_ms

    @property
    def total_matched_count(self):
        """
        **[Required]** Gets the total_matched_count of this VerifyOutput.
        Total match count.


        :return: The total_matched_count of this VerifyOutput.
        :rtype: int
        """
        return self._total_matched_count

    @total_matched_count.setter
    def total_matched_count(self, total_matched_count):
        """
        Sets the total_matched_count of this VerifyOutput.
        Total match count.


        :param total_matched_count: The total_matched_count of this VerifyOutput.
        :type: int
        """
        self._total_matched_count = total_matched_count

    @property
    def total_count(self):
        """
        **[Required]** Gets the total_count of this VerifyOutput.
        Total count.


        :return: The total_count of this VerifyOutput.
        :rtype: int
        """
        return self._total_count

    @total_count.setter
    def total_count(self, total_count):
        """
        Sets the total_count of this VerifyOutput.
        Total count.


        :param total_count: The total_count of this VerifyOutput.
        :type: int
        """
        self._total_count = total_count

    @property
    def columns(self):
        """
        Gets the columns of this VerifyOutput.
        Acceleration result columns, included if requested (shouldIncludeResults).


        :return: The columns of this VerifyOutput.
        :rtype: list[oci.log_analytics.models.ResultColumn]
        """
        return self._columns

    @columns.setter
    def columns(self, columns):
        """
        Sets the columns of this VerifyOutput.
        Acceleration result columns, included if requested (shouldIncludeResults).


        :param columns: The columns of this VerifyOutput.
        :type: list[oci.log_analytics.models.ResultColumn]
        """
        self._columns = columns

    @property
    def results(self):
        """
        Gets the results of this VerifyOutput.
        Acceleration result values, included if requested (shouldIncludeResults).


        :return: The results of this VerifyOutput.
        :rtype: list[dict(str, object)]
        """
        return self._results

    @results.setter
    def results(self, results):
        """
        Sets the results of this VerifyOutput.
        Acceleration result values, included if requested (shouldIncludeResults).


        :param results: The results of this VerifyOutput.
        :type: list[dict(str, object)]
        """
        self._results = results

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
