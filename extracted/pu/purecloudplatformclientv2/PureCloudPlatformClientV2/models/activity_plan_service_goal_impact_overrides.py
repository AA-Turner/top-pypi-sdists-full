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
    from . import ActivityPlanAbandonRateImpactOverride
    from . import ActivityPlanAsaImpactOverride
    from . import ActivityPlanServiceLevelImpactOverride

class ActivityPlanServiceGoalImpactOverrides(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self) -> None:
        """
        ActivityPlanServiceGoalImpactOverrides - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'abandon_rate': 'ActivityPlanAbandonRateImpactOverride',
            'service_level': 'ActivityPlanServiceLevelImpactOverride',
            'average_speed_of_answer': 'ActivityPlanAsaImpactOverride'
        }

        self.attribute_map = {
            'abandon_rate': 'abandonRate',
            'service_level': 'serviceLevel',
            'average_speed_of_answer': 'averageSpeedOfAnswer'
        }

        self._abandon_rate = None
        self._service_level = None
        self._average_speed_of_answer = None

    @property
    def abandon_rate(self) -> 'ActivityPlanAbandonRateImpactOverride':
        """
        Gets the abandon_rate of this ActivityPlanServiceGoalImpactOverrides.
        Abandon rate service goal override for the associated activity plan

        :return: The abandon_rate of this ActivityPlanServiceGoalImpactOverrides.
        :rtype: ActivityPlanAbandonRateImpactOverride
        """
        return self._abandon_rate

    @abandon_rate.setter
    def abandon_rate(self, abandon_rate: 'ActivityPlanAbandonRateImpactOverride') -> None:
        """
        Sets the abandon_rate of this ActivityPlanServiceGoalImpactOverrides.
        Abandon rate service goal override for the associated activity plan

        :param abandon_rate: The abandon_rate of this ActivityPlanServiceGoalImpactOverrides.
        :type: ActivityPlanAbandonRateImpactOverride
        """
        

        self._abandon_rate = abandon_rate

    @property
    def service_level(self) -> 'ActivityPlanServiceLevelImpactOverride':
        """
        Gets the service_level of this ActivityPlanServiceGoalImpactOverrides.
        Service level goal override for the associated activity plan

        :return: The service_level of this ActivityPlanServiceGoalImpactOverrides.
        :rtype: ActivityPlanServiceLevelImpactOverride
        """
        return self._service_level

    @service_level.setter
    def service_level(self, service_level: 'ActivityPlanServiceLevelImpactOverride') -> None:
        """
        Sets the service_level of this ActivityPlanServiceGoalImpactOverrides.
        Service level goal override for the associated activity plan

        :param service_level: The service_level of this ActivityPlanServiceGoalImpactOverrides.
        :type: ActivityPlanServiceLevelImpactOverride
        """
        

        self._service_level = service_level

    @property
    def average_speed_of_answer(self) -> 'ActivityPlanAsaImpactOverride':
        """
        Gets the average_speed_of_answer of this ActivityPlanServiceGoalImpactOverrides.
        Average speed of answer service goal override for the associated activity plan

        :return: The average_speed_of_answer of this ActivityPlanServiceGoalImpactOverrides.
        :rtype: ActivityPlanAsaImpactOverride
        """
        return self._average_speed_of_answer

    @average_speed_of_answer.setter
    def average_speed_of_answer(self, average_speed_of_answer: 'ActivityPlanAsaImpactOverride') -> None:
        """
        Sets the average_speed_of_answer of this ActivityPlanServiceGoalImpactOverrides.
        Average speed of answer service goal override for the associated activity plan

        :param average_speed_of_answer: The average_speed_of_answer of this ActivityPlanServiceGoalImpactOverrides.
        :type: ActivityPlanAsaImpactOverride
        """
        

        self._average_speed_of_answer = average_speed_of_answer

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

