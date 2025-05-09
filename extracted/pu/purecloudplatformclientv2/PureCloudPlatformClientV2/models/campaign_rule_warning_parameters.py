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


class CampaignRuleWarningParameters(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self) -> None:
        """
        CampaignRuleWarningParameters - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'action_id': 'str',
            'condition_id': 'str',
            'action_type': 'str',
            'condition_type': 'str'
        }

        self.attribute_map = {
            'action_id': 'actionId',
            'condition_id': 'conditionId',
            'action_type': 'actionType',
            'condition_type': 'conditionType'
        }

        self._action_id = None
        self._condition_id = None
        self._action_type = None
        self._condition_type = None

    @property
    def action_id(self) -> str:
        """
        Gets the action_id of this CampaignRuleWarningParameters.
        ID of action

        :return: The action_id of this CampaignRuleWarningParameters.
        :rtype: str
        """
        return self._action_id

    @action_id.setter
    def action_id(self, action_id: str) -> None:
        """
        Sets the action_id of this CampaignRuleWarningParameters.
        ID of action

        :param action_id: The action_id of this CampaignRuleWarningParameters.
        :type: str
        """
        

        self._action_id = action_id

    @property
    def condition_id(self) -> str:
        """
        Gets the condition_id of this CampaignRuleWarningParameters.
        ID of condition

        :return: The condition_id of this CampaignRuleWarningParameters.
        :rtype: str
        """
        return self._condition_id

    @condition_id.setter
    def condition_id(self, condition_id: str) -> None:
        """
        Sets the condition_id of this CampaignRuleWarningParameters.
        ID of condition

        :param condition_id: The condition_id of this CampaignRuleWarningParameters.
        :type: str
        """
        

        self._condition_id = condition_id

    @property
    def action_type(self) -> str:
        """
        Gets the action_type of this CampaignRuleWarningParameters.
        Type of action

        :return: The action_type of this CampaignRuleWarningParameters.
        :rtype: str
        """
        return self._action_type

    @action_type.setter
    def action_type(self, action_type: str) -> None:
        """
        Sets the action_type of this CampaignRuleWarningParameters.
        Type of action

        :param action_type: The action_type of this CampaignRuleWarningParameters.
        :type: str
        """
        if isinstance(action_type, int):
            action_type = str(action_type)
        allowed_values = ["turnOnCampaign", "turnOffCampaign", "turnOnSequence", "turnOffSequence", "setCampaignPriority", "recycleCampaign", "setCampaignDialingMode", "setCampaignAbandonRate", "setCampaignNumberOfLines", "setCampaignWeight", "setCampaignMaxCallsPerAgent", "setCampaignMessagesPerMinute", "changeCampaignQueue", "changeCampaignTemplate"]
        if action_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for action_type -> " + action_type)
            self._action_type = "outdated_sdk_version"
        else:
            self._action_type = action_type

    @property
    def condition_type(self) -> str:
        """
        Gets the condition_type of this CampaignRuleWarningParameters.
        Type of condition

        :return: The condition_type of this CampaignRuleWarningParameters.
        :rtype: str
        """
        return self._condition_type

    @condition_type.setter
    def condition_type(self, condition_type: str) -> None:
        """
        Sets the condition_type of this CampaignRuleWarningParameters.
        Type of condition

        :param condition_type: The condition_type of this CampaignRuleWarningParameters.
        :type: str
        """
        if isinstance(condition_type, int):
            condition_type = str(condition_type)
        allowed_values = ["campaignProgress", "campaignAgents", "campaignRecordsAttempted", "campaignContactsMessaged", "campaignBusinessSuccess", "campaignBusinessFailure", "campaignBusinessNeutral", "campaignValidAttempts", "campaignRightPartyContacts"]
        if condition_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for condition_type -> " + condition_type)
            self._condition_type = "outdated_sdk_version"
        else:
            self._condition_type = condition_type

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

