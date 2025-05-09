# coding: utf-8

"""
Copyright 2016 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from datetime import datetime
from datetime import date
from pprint import pformat
import re
import json

from ..utils import sanitize_for_serialization

# type hinting support
from typing import TYPE_CHECKING
from typing import List
from typing import Dict

if TYPE_CHECKING:
    from . import BuScheduleReference
    from . import ReschedulingManagementUnitResponse

class ReschedulingOptionsRunResponse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self) -> None:
        """
        ReschedulingOptionsRunResponse - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'existing_schedule': 'BuScheduleReference',
            'start_date': 'datetime',
            'end_date': 'datetime',
            'management_units': 'list[ReschedulingManagementUnitResponse]',
            'agent_count': 'int',
            'activity_code_ids': 'list[str]',
            'do_not_change_weekly_paid_time': 'bool',
            'do_not_change_daily_paid_time': 'bool',
            'do_not_change_shift_start_times': 'bool',
            'do_not_change_manually_edited_shifts': 'bool'
        }

        self.attribute_map = {
            'existing_schedule': 'existingSchedule',
            'start_date': 'startDate',
            'end_date': 'endDate',
            'management_units': 'managementUnits',
            'agent_count': 'agentCount',
            'activity_code_ids': 'activityCodeIds',
            'do_not_change_weekly_paid_time': 'doNotChangeWeeklyPaidTime',
            'do_not_change_daily_paid_time': 'doNotChangeDailyPaidTime',
            'do_not_change_shift_start_times': 'doNotChangeShiftStartTimes',
            'do_not_change_manually_edited_shifts': 'doNotChangeManuallyEditedShifts'
        }

        self._existing_schedule = None
        self._start_date = None
        self._end_date = None
        self._management_units = None
        self._agent_count = None
        self._activity_code_ids = None
        self._do_not_change_weekly_paid_time = None
        self._do_not_change_daily_paid_time = None
        self._do_not_change_shift_start_times = None
        self._do_not_change_manually_edited_shifts = None

    @property
    def existing_schedule(self) -> 'BuScheduleReference':
        """
        Gets the existing_schedule of this ReschedulingOptionsRunResponse.
        The existing schedule to which this reschedule run applies

        :return: The existing_schedule of this ReschedulingOptionsRunResponse.
        :rtype: BuScheduleReference
        """
        return self._existing_schedule

    @existing_schedule.setter
    def existing_schedule(self, existing_schedule: 'BuScheduleReference') -> None:
        """
        Sets the existing_schedule of this ReschedulingOptionsRunResponse.
        The existing schedule to which this reschedule run applies

        :param existing_schedule: The existing_schedule of this ReschedulingOptionsRunResponse.
        :type: BuScheduleReference
        """
        

        self._existing_schedule = existing_schedule

    @property
    def start_date(self) -> datetime:
        """
        Gets the start_date of this ReschedulingOptionsRunResponse.
        The start date of the period to reschedule. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The start_date of this ReschedulingOptionsRunResponse.
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date: datetime) -> None:
        """
        Sets the start_date of this ReschedulingOptionsRunResponse.
        The start date of the period to reschedule. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param start_date: The start_date of this ReschedulingOptionsRunResponse.
        :type: datetime
        """
        

        self._start_date = start_date

    @property
    def end_date(self) -> datetime:
        """
        Gets the end_date of this ReschedulingOptionsRunResponse.
        The end date of the period to reschedule. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The end_date of this ReschedulingOptionsRunResponse.
        :rtype: datetime
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date: datetime) -> None:
        """
        Sets the end_date of this ReschedulingOptionsRunResponse.
        The end date of the period to reschedule. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param end_date: The end_date of this ReschedulingOptionsRunResponse.
        :type: datetime
        """
        

        self._end_date = end_date

    @property
    def management_units(self) -> List['ReschedulingManagementUnitResponse']:
        """
        Gets the management_units of this ReschedulingOptionsRunResponse.
        Per-management unit rescheduling options

        :return: The management_units of this ReschedulingOptionsRunResponse.
        :rtype: list[ReschedulingManagementUnitResponse]
        """
        return self._management_units

    @management_units.setter
    def management_units(self, management_units: List['ReschedulingManagementUnitResponse']) -> None:
        """
        Sets the management_units of this ReschedulingOptionsRunResponse.
        Per-management unit rescheduling options

        :param management_units: The management_units of this ReschedulingOptionsRunResponse.
        :type: list[ReschedulingManagementUnitResponse]
        """
        

        self._management_units = management_units

    @property
    def agent_count(self) -> int:
        """
        Gets the agent_count of this ReschedulingOptionsRunResponse.
        The number of agents to be considered in the reschedule

        :return: The agent_count of this ReschedulingOptionsRunResponse.
        :rtype: int
        """
        return self._agent_count

    @agent_count.setter
    def agent_count(self, agent_count: int) -> None:
        """
        Sets the agent_count of this ReschedulingOptionsRunResponse.
        The number of agents to be considered in the reschedule

        :param agent_count: The agent_count of this ReschedulingOptionsRunResponse.
        :type: int
        """
        

        self._agent_count = agent_count

    @property
    def activity_code_ids(self) -> List[str]:
        """
        Gets the activity_code_ids of this ReschedulingOptionsRunResponse.
        The IDs of the activity codes being considered for reschedule

        :return: The activity_code_ids of this ReschedulingOptionsRunResponse.
        :rtype: list[str]
        """
        return self._activity_code_ids

    @activity_code_ids.setter
    def activity_code_ids(self, activity_code_ids: List[str]) -> None:
        """
        Sets the activity_code_ids of this ReschedulingOptionsRunResponse.
        The IDs of the activity codes being considered for reschedule

        :param activity_code_ids: The activity_code_ids of this ReschedulingOptionsRunResponse.
        :type: list[str]
        """
        

        self._activity_code_ids = activity_code_ids

    @property
    def do_not_change_weekly_paid_time(self) -> bool:
        """
        Gets the do_not_change_weekly_paid_time of this ReschedulingOptionsRunResponse.
        Whether weekly paid time is allowed to be changed

        :return: The do_not_change_weekly_paid_time of this ReschedulingOptionsRunResponse.
        :rtype: bool
        """
        return self._do_not_change_weekly_paid_time

    @do_not_change_weekly_paid_time.setter
    def do_not_change_weekly_paid_time(self, do_not_change_weekly_paid_time: bool) -> None:
        """
        Sets the do_not_change_weekly_paid_time of this ReschedulingOptionsRunResponse.
        Whether weekly paid time is allowed to be changed

        :param do_not_change_weekly_paid_time: The do_not_change_weekly_paid_time of this ReschedulingOptionsRunResponse.
        :type: bool
        """
        

        self._do_not_change_weekly_paid_time = do_not_change_weekly_paid_time

    @property
    def do_not_change_daily_paid_time(self) -> bool:
        """
        Gets the do_not_change_daily_paid_time of this ReschedulingOptionsRunResponse.
        Whether daily paid time is allowed to be changed

        :return: The do_not_change_daily_paid_time of this ReschedulingOptionsRunResponse.
        :rtype: bool
        """
        return self._do_not_change_daily_paid_time

    @do_not_change_daily_paid_time.setter
    def do_not_change_daily_paid_time(self, do_not_change_daily_paid_time: bool) -> None:
        """
        Sets the do_not_change_daily_paid_time of this ReschedulingOptionsRunResponse.
        Whether daily paid time is allowed to be changed

        :param do_not_change_daily_paid_time: The do_not_change_daily_paid_time of this ReschedulingOptionsRunResponse.
        :type: bool
        """
        

        self._do_not_change_daily_paid_time = do_not_change_daily_paid_time

    @property
    def do_not_change_shift_start_times(self) -> bool:
        """
        Gets the do_not_change_shift_start_times of this ReschedulingOptionsRunResponse.
        Whether shift start times are allowed to be changed

        :return: The do_not_change_shift_start_times of this ReschedulingOptionsRunResponse.
        :rtype: bool
        """
        return self._do_not_change_shift_start_times

    @do_not_change_shift_start_times.setter
    def do_not_change_shift_start_times(self, do_not_change_shift_start_times: bool) -> None:
        """
        Sets the do_not_change_shift_start_times of this ReschedulingOptionsRunResponse.
        Whether shift start times are allowed to be changed

        :param do_not_change_shift_start_times: The do_not_change_shift_start_times of this ReschedulingOptionsRunResponse.
        :type: bool
        """
        

        self._do_not_change_shift_start_times = do_not_change_shift_start_times

    @property
    def do_not_change_manually_edited_shifts(self) -> bool:
        """
        Gets the do_not_change_manually_edited_shifts of this ReschedulingOptionsRunResponse.
        Whether manually edited shifts are allowed to be changed

        :return: The do_not_change_manually_edited_shifts of this ReschedulingOptionsRunResponse.
        :rtype: bool
        """
        return self._do_not_change_manually_edited_shifts

    @do_not_change_manually_edited_shifts.setter
    def do_not_change_manually_edited_shifts(self, do_not_change_manually_edited_shifts: bool) -> None:
        """
        Sets the do_not_change_manually_edited_shifts of this ReschedulingOptionsRunResponse.
        Whether manually edited shifts are allowed to be changed

        :param do_not_change_manually_edited_shifts: The do_not_change_manually_edited_shifts of this ReschedulingOptionsRunResponse.
        :type: bool
        """
        

        self._do_not_change_manually_edited_shifts = do_not_change_manually_edited_shifts

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in self.swagger_types.items():
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_json(self):
        """
        Returns the model as raw JSON
        """
        return json.dumps(sanitize_for_serialization(self.to_dict()))

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

