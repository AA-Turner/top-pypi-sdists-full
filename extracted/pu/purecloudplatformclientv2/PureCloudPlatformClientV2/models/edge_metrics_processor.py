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


class EdgeMetricsProcessor(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self) -> None:
        """
        EdgeMetricsProcessor - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'active_time_pct': 'float',
            'cpu_id': 'str',
            'idle_time_pct': 'float',
            'privileged_time_pct': 'float',
            'user_time_pct': 'float'
        }

        self.attribute_map = {
            'active_time_pct': 'activeTimePct',
            'cpu_id': 'cpuId',
            'idle_time_pct': 'idleTimePct',
            'privileged_time_pct': 'privilegedTimePct',
            'user_time_pct': 'userTimePct'
        }

        self._active_time_pct = None
        self._cpu_id = None
        self._idle_time_pct = None
        self._privileged_time_pct = None
        self._user_time_pct = None

    @property
    def active_time_pct(self) -> float:
        """
        Gets the active_time_pct of this EdgeMetricsProcessor.
        Percent time processor was active.

        :return: The active_time_pct of this EdgeMetricsProcessor.
        :rtype: float
        """
        return self._active_time_pct

    @active_time_pct.setter
    def active_time_pct(self, active_time_pct: float) -> None:
        """
        Sets the active_time_pct of this EdgeMetricsProcessor.
        Percent time processor was active.

        :param active_time_pct: The active_time_pct of this EdgeMetricsProcessor.
        :type: float
        """
        

        self._active_time_pct = active_time_pct

    @property
    def cpu_id(self) -> str:
        """
        Gets the cpu_id of this EdgeMetricsProcessor.
        Machine CPU identifier. 'total' will always be included in the array and is the total of all CPU resources.

        :return: The cpu_id of this EdgeMetricsProcessor.
        :rtype: str
        """
        return self._cpu_id

    @cpu_id.setter
    def cpu_id(self, cpu_id: str) -> None:
        """
        Sets the cpu_id of this EdgeMetricsProcessor.
        Machine CPU identifier. 'total' will always be included in the array and is the total of all CPU resources.

        :param cpu_id: The cpu_id of this EdgeMetricsProcessor.
        :type: str
        """
        

        self._cpu_id = cpu_id

    @property
    def idle_time_pct(self) -> float:
        """
        Gets the idle_time_pct of this EdgeMetricsProcessor.
        Percent time processor was idle.

        :return: The idle_time_pct of this EdgeMetricsProcessor.
        :rtype: float
        """
        return self._idle_time_pct

    @idle_time_pct.setter
    def idle_time_pct(self, idle_time_pct: float) -> None:
        """
        Sets the idle_time_pct of this EdgeMetricsProcessor.
        Percent time processor was idle.

        :param idle_time_pct: The idle_time_pct of this EdgeMetricsProcessor.
        :type: float
        """
        

        self._idle_time_pct = idle_time_pct

    @property
    def privileged_time_pct(self) -> float:
        """
        Gets the privileged_time_pct of this EdgeMetricsProcessor.
        Percent time processor spent in privileged mode.

        :return: The privileged_time_pct of this EdgeMetricsProcessor.
        :rtype: float
        """
        return self._privileged_time_pct

    @privileged_time_pct.setter
    def privileged_time_pct(self, privileged_time_pct: float) -> None:
        """
        Sets the privileged_time_pct of this EdgeMetricsProcessor.
        Percent time processor spent in privileged mode.

        :param privileged_time_pct: The privileged_time_pct of this EdgeMetricsProcessor.
        :type: float
        """
        

        self._privileged_time_pct = privileged_time_pct

    @property
    def user_time_pct(self) -> float:
        """
        Gets the user_time_pct of this EdgeMetricsProcessor.
        Percent time processor spent in user mode.

        :return: The user_time_pct of this EdgeMetricsProcessor.
        :rtype: float
        """
        return self._user_time_pct

    @user_time_pct.setter
    def user_time_pct(self, user_time_pct: float) -> None:
        """
        Sets the user_time_pct of this EdgeMetricsProcessor.
        Percent time processor spent in user mode.

        :param user_time_pct: The user_time_pct of this EdgeMetricsProcessor.
        :type: float
        """
        

        self._user_time_pct = user_time_pct

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

