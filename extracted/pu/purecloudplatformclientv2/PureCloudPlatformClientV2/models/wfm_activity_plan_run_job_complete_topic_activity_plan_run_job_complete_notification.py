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
    from . import WfmActivityPlanRunJobCompleteTopicActivityPlanJobException
    from . import WfmActivityPlanRunJobCompleteTopicActivityPlanReference
    from . import WfmActivityPlanRunJobCompleteTopicErrorBody

class WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self) -> None:
        """
        WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'type': 'str',
            'activity_plan': 'WfmActivityPlanRunJobCompleteTopicActivityPlanReference',
            'status': 'str',
            'exceptions': 'list[WfmActivityPlanRunJobCompleteTopicActivityPlanJobException]',
            'error': 'WfmActivityPlanRunJobCompleteTopicErrorBody'
        }

        self.attribute_map = {
            'id': 'id',
            'type': 'type',
            'activity_plan': 'activityPlan',
            'status': 'status',
            'exceptions': 'exceptions',
            'error': 'error'
        }

        self._id = None
        self._type = None
        self._activity_plan = None
        self._status = None
        self._exceptions = None
        self._error = None

    @property
    def id(self) -> str:
        """
        Gets the id of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.


        :return: The id of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str) -> None:
        """
        Sets the id of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.


        :param id: The id of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.
        :type: str
        """
        

        self._id = id

    @property
    def type(self) -> str:
        """
        Gets the type of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.


        :return: The type of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str) -> None:
        """
        Sets the type of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.


        :param type: The type of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.
        :type: str
        """
        if isinstance(type, int):
            type = str(type)
        allowed_values = ["RunPlan", "DeleteOccurrence"]
        if type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for type -> " + type)
            self._type = "outdated_sdk_version"
        else:
            self._type = type

    @property
    def activity_plan(self) -> 'WfmActivityPlanRunJobCompleteTopicActivityPlanReference':
        """
        Gets the activity_plan of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.


        :return: The activity_plan of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.
        :rtype: WfmActivityPlanRunJobCompleteTopicActivityPlanReference
        """
        return self._activity_plan

    @activity_plan.setter
    def activity_plan(self, activity_plan: 'WfmActivityPlanRunJobCompleteTopicActivityPlanReference') -> None:
        """
        Sets the activity_plan of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.


        :param activity_plan: The activity_plan of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.
        :type: WfmActivityPlanRunJobCompleteTopicActivityPlanReference
        """
        

        self._activity_plan = activity_plan

    @property
    def status(self) -> str:
        """
        Gets the status of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.


        :return: The status of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str) -> None:
        """
        Sets the status of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.


        :param status: The status of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.
        :type: str
        """
        if isinstance(status, int):
            status = str(status)
        allowed_values = ["Processing", "Complete", "Error"]
        if status.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for status -> " + status)
            self._status = "outdated_sdk_version"
        else:
            self._status = status

    @property
    def exceptions(self) -> List['WfmActivityPlanRunJobCompleteTopicActivityPlanJobException']:
        """
        Gets the exceptions of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.


        :return: The exceptions of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.
        :rtype: list[WfmActivityPlanRunJobCompleteTopicActivityPlanJobException]
        """
        return self._exceptions

    @exceptions.setter
    def exceptions(self, exceptions: List['WfmActivityPlanRunJobCompleteTopicActivityPlanJobException']) -> None:
        """
        Sets the exceptions of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.


        :param exceptions: The exceptions of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.
        :type: list[WfmActivityPlanRunJobCompleteTopicActivityPlanJobException]
        """
        

        self._exceptions = exceptions

    @property
    def error(self) -> 'WfmActivityPlanRunJobCompleteTopicErrorBody':
        """
        Gets the error of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.


        :return: The error of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.
        :rtype: WfmActivityPlanRunJobCompleteTopicErrorBody
        """
        return self._error

    @error.setter
    def error(self, error: 'WfmActivityPlanRunJobCompleteTopicErrorBody') -> None:
        """
        Sets the error of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.


        :param error: The error of this WfmActivityPlanRunJobCompleteTopicActivityPlanRunJobCompleteNotification.
        :type: WfmActivityPlanRunJobCompleteTopicErrorBody
        """
        

        self._error = error

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

