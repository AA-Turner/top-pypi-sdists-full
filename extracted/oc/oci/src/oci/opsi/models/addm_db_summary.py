# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20200630


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AddmDbSummary(object):
    """
    ADDM summary for a database
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AddmDbSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param database_details:
            The value to assign to the database_details property of this AddmDbSummary.
        :type database_details: oci.opsi.models.DatabaseDetails

        :param number_of_findings:
            The value to assign to the number_of_findings property of this AddmDbSummary.
        :type number_of_findings: int

        :param number_of_addm_tasks:
            The value to assign to the number_of_addm_tasks property of this AddmDbSummary.
        :type number_of_addm_tasks: int

        :param time_first_snapshot_begin:
            The value to assign to the time_first_snapshot_begin property of this AddmDbSummary.
        :type time_first_snapshot_begin: datetime

        :param time_latest_snapshot_end:
            The value to assign to the time_latest_snapshot_end property of this AddmDbSummary.
        :type time_latest_snapshot_end: datetime

        :param snapshot_interval_start:
            The value to assign to the snapshot_interval_start property of this AddmDbSummary.
        :type snapshot_interval_start: str

        :param snapshot_interval_end:
            The value to assign to the snapshot_interval_end property of this AddmDbSummary.
        :type snapshot_interval_end: str

        :param max_overall_impact:
            The value to assign to the max_overall_impact property of this AddmDbSummary.
        :type max_overall_impact: float

        :param most_frequent_category_name:
            The value to assign to the most_frequent_category_name property of this AddmDbSummary.
        :type most_frequent_category_name: str

        :param most_frequent_category_display_name:
            The value to assign to the most_frequent_category_display_name property of this AddmDbSummary.
        :type most_frequent_category_display_name: str

        """
        self.swagger_types = {
            'database_details': 'DatabaseDetails',
            'number_of_findings': 'int',
            'number_of_addm_tasks': 'int',
            'time_first_snapshot_begin': 'datetime',
            'time_latest_snapshot_end': 'datetime',
            'snapshot_interval_start': 'str',
            'snapshot_interval_end': 'str',
            'max_overall_impact': 'float',
            'most_frequent_category_name': 'str',
            'most_frequent_category_display_name': 'str'
        }
        self.attribute_map = {
            'database_details': 'databaseDetails',
            'number_of_findings': 'numberOfFindings',
            'number_of_addm_tasks': 'numberOfAddmTasks',
            'time_first_snapshot_begin': 'timeFirstSnapshotBegin',
            'time_latest_snapshot_end': 'timeLatestSnapshotEnd',
            'snapshot_interval_start': 'snapshotIntervalStart',
            'snapshot_interval_end': 'snapshotIntervalEnd',
            'max_overall_impact': 'maxOverallImpact',
            'most_frequent_category_name': 'mostFrequentCategoryName',
            'most_frequent_category_display_name': 'mostFrequentCategoryDisplayName'
        }
        self._database_details = None
        self._number_of_findings = None
        self._number_of_addm_tasks = None
        self._time_first_snapshot_begin = None
        self._time_latest_snapshot_end = None
        self._snapshot_interval_start = None
        self._snapshot_interval_end = None
        self._max_overall_impact = None
        self._most_frequent_category_name = None
        self._most_frequent_category_display_name = None

    @property
    def database_details(self):
        """
        **[Required]** Gets the database_details of this AddmDbSummary.

        :return: The database_details of this AddmDbSummary.
        :rtype: oci.opsi.models.DatabaseDetails
        """
        return self._database_details

    @database_details.setter
    def database_details(self, database_details):
        """
        Sets the database_details of this AddmDbSummary.

        :param database_details: The database_details of this AddmDbSummary.
        :type: oci.opsi.models.DatabaseDetails
        """
        self._database_details = database_details

    @property
    def number_of_findings(self):
        """
        Gets the number_of_findings of this AddmDbSummary.
        Number of ADDM findings


        :return: The number_of_findings of this AddmDbSummary.
        :rtype: int
        """
        return self._number_of_findings

    @number_of_findings.setter
    def number_of_findings(self, number_of_findings):
        """
        Sets the number_of_findings of this AddmDbSummary.
        Number of ADDM findings


        :param number_of_findings: The number_of_findings of this AddmDbSummary.
        :type: int
        """
        self._number_of_findings = number_of_findings

    @property
    def number_of_addm_tasks(self):
        """
        Gets the number_of_addm_tasks of this AddmDbSummary.
        Number of ADDM tasks


        :return: The number_of_addm_tasks of this AddmDbSummary.
        :rtype: int
        """
        return self._number_of_addm_tasks

    @number_of_addm_tasks.setter
    def number_of_addm_tasks(self, number_of_addm_tasks):
        """
        Sets the number_of_addm_tasks of this AddmDbSummary.
        Number of ADDM tasks


        :param number_of_addm_tasks: The number_of_addm_tasks of this AddmDbSummary.
        :type: int
        """
        self._number_of_addm_tasks = number_of_addm_tasks

    @property
    def time_first_snapshot_begin(self):
        """
        Gets the time_first_snapshot_begin of this AddmDbSummary.
        The start timestamp that was passed into the request.


        :return: The time_first_snapshot_begin of this AddmDbSummary.
        :rtype: datetime
        """
        return self._time_first_snapshot_begin

    @time_first_snapshot_begin.setter
    def time_first_snapshot_begin(self, time_first_snapshot_begin):
        """
        Sets the time_first_snapshot_begin of this AddmDbSummary.
        The start timestamp that was passed into the request.


        :param time_first_snapshot_begin: The time_first_snapshot_begin of this AddmDbSummary.
        :type: datetime
        """
        self._time_first_snapshot_begin = time_first_snapshot_begin

    @property
    def time_latest_snapshot_end(self):
        """
        Gets the time_latest_snapshot_end of this AddmDbSummary.
        The end timestamp that was passed into the request.


        :return: The time_latest_snapshot_end of this AddmDbSummary.
        :rtype: datetime
        """
        return self._time_latest_snapshot_end

    @time_latest_snapshot_end.setter
    def time_latest_snapshot_end(self, time_latest_snapshot_end):
        """
        Sets the time_latest_snapshot_end of this AddmDbSummary.
        The end timestamp that was passed into the request.


        :param time_latest_snapshot_end: The time_latest_snapshot_end of this AddmDbSummary.
        :type: datetime
        """
        self._time_latest_snapshot_end = time_latest_snapshot_end

    @property
    def snapshot_interval_start(self):
        """
        Gets the snapshot_interval_start of this AddmDbSummary.
        AWR snapshot id.


        :return: The snapshot_interval_start of this AddmDbSummary.
        :rtype: str
        """
        return self._snapshot_interval_start

    @snapshot_interval_start.setter
    def snapshot_interval_start(self, snapshot_interval_start):
        """
        Sets the snapshot_interval_start of this AddmDbSummary.
        AWR snapshot id.


        :param snapshot_interval_start: The snapshot_interval_start of this AddmDbSummary.
        :type: str
        """
        self._snapshot_interval_start = snapshot_interval_start

    @property
    def snapshot_interval_end(self):
        """
        Gets the snapshot_interval_end of this AddmDbSummary.
        AWR snapshot id.


        :return: The snapshot_interval_end of this AddmDbSummary.
        :rtype: str
        """
        return self._snapshot_interval_end

    @snapshot_interval_end.setter
    def snapshot_interval_end(self, snapshot_interval_end):
        """
        Sets the snapshot_interval_end of this AddmDbSummary.
        AWR snapshot id.


        :param snapshot_interval_end: The snapshot_interval_end of this AddmDbSummary.
        :type: str
        """
        self._snapshot_interval_end = snapshot_interval_end

    @property
    def max_overall_impact(self):
        """
        Gets the max_overall_impact of this AddmDbSummary.
        Maximum overall impact in terms of percentage of total activity


        :return: The max_overall_impact of this AddmDbSummary.
        :rtype: float
        """
        return self._max_overall_impact

    @max_overall_impact.setter
    def max_overall_impact(self, max_overall_impact):
        """
        Sets the max_overall_impact of this AddmDbSummary.
        Maximum overall impact in terms of percentage of total activity


        :param max_overall_impact: The max_overall_impact of this AddmDbSummary.
        :type: float
        """
        self._max_overall_impact = max_overall_impact

    @property
    def most_frequent_category_name(self):
        """
        Gets the most_frequent_category_name of this AddmDbSummary.
        Category name


        :return: The most_frequent_category_name of this AddmDbSummary.
        :rtype: str
        """
        return self._most_frequent_category_name

    @most_frequent_category_name.setter
    def most_frequent_category_name(self, most_frequent_category_name):
        """
        Sets the most_frequent_category_name of this AddmDbSummary.
        Category name


        :param most_frequent_category_name: The most_frequent_category_name of this AddmDbSummary.
        :type: str
        """
        self._most_frequent_category_name = most_frequent_category_name

    @property
    def most_frequent_category_display_name(self):
        """
        Gets the most_frequent_category_display_name of this AddmDbSummary.
        Category display name


        :return: The most_frequent_category_display_name of this AddmDbSummary.
        :rtype: str
        """
        return self._most_frequent_category_display_name

    @most_frequent_category_display_name.setter
    def most_frequent_category_display_name(self, most_frequent_category_display_name):
        """
        Sets the most_frequent_category_display_name of this AddmDbSummary.
        Category display name


        :param most_frequent_category_display_name: The most_frequent_category_display_name of this AddmDbSummary.
        :type: str
        """
        self._most_frequent_category_display_name = most_frequent_category_display_name

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
