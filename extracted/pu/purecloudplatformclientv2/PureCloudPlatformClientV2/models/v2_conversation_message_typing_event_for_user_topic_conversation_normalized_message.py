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
    from . import V2ConversationMessageTypingEventForUserTopicConversationMessageEvent
    from . import V2ConversationMessageTypingEventForUserTopicConversationMessagingChannel

class V2ConversationMessageTypingEventForUserTopicConversationNormalizedMessage(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self) -> None:
        """
        V2ConversationMessageTypingEventForUserTopicConversationNormalizedMessage - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'channel': 'V2ConversationMessageTypingEventForUserTopicConversationMessagingChannel',
            'type': 'str',
            'events': 'list[V2ConversationMessageTypingEventForUserTopicConversationMessageEvent]',
            'direction': 'str'
        }

        self.attribute_map = {
            'channel': 'channel',
            'type': 'type',
            'events': 'events',
            'direction': 'direction'
        }

        self._channel = None
        self._type = None
        self._events = None
        self._direction = None

    @property
    def channel(self) -> 'V2ConversationMessageTypingEventForUserTopicConversationMessagingChannel':
        """
        Gets the channel of this V2ConversationMessageTypingEventForUserTopicConversationNormalizedMessage.


        :return: The channel of this V2ConversationMessageTypingEventForUserTopicConversationNormalizedMessage.
        :rtype: V2ConversationMessageTypingEventForUserTopicConversationMessagingChannel
        """
        return self._channel

    @channel.setter
    def channel(self, channel: 'V2ConversationMessageTypingEventForUserTopicConversationMessagingChannel') -> None:
        """
        Sets the channel of this V2ConversationMessageTypingEventForUserTopicConversationNormalizedMessage.


        :param channel: The channel of this V2ConversationMessageTypingEventForUserTopicConversationNormalizedMessage.
        :type: V2ConversationMessageTypingEventForUserTopicConversationMessagingChannel
        """
        

        self._channel = channel

    @property
    def type(self) -> str:
        """
        Gets the type of this V2ConversationMessageTypingEventForUserTopicConversationNormalizedMessage.


        :return: The type of this V2ConversationMessageTypingEventForUserTopicConversationNormalizedMessage.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str) -> None:
        """
        Sets the type of this V2ConversationMessageTypingEventForUserTopicConversationNormalizedMessage.


        :param type: The type of this V2ConversationMessageTypingEventForUserTopicConversationNormalizedMessage.
        :type: str
        """
        if isinstance(type, int):
            type = str(type)
        allowed_values = ["Event"]
        if type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for type -> " + type)
            self._type = "outdated_sdk_version"
        else:
            self._type = type

    @property
    def events(self) -> List['V2ConversationMessageTypingEventForUserTopicConversationMessageEvent']:
        """
        Gets the events of this V2ConversationMessageTypingEventForUserTopicConversationNormalizedMessage.


        :return: The events of this V2ConversationMessageTypingEventForUserTopicConversationNormalizedMessage.
        :rtype: list[V2ConversationMessageTypingEventForUserTopicConversationMessageEvent]
        """
        return self._events

    @events.setter
    def events(self, events: List['V2ConversationMessageTypingEventForUserTopicConversationMessageEvent']) -> None:
        """
        Sets the events of this V2ConversationMessageTypingEventForUserTopicConversationNormalizedMessage.


        :param events: The events of this V2ConversationMessageTypingEventForUserTopicConversationNormalizedMessage.
        :type: list[V2ConversationMessageTypingEventForUserTopicConversationMessageEvent]
        """
        

        self._events = events

    @property
    def direction(self) -> str:
        """
        Gets the direction of this V2ConversationMessageTypingEventForUserTopicConversationNormalizedMessage.


        :return: The direction of this V2ConversationMessageTypingEventForUserTopicConversationNormalizedMessage.
        :rtype: str
        """
        return self._direction

    @direction.setter
    def direction(self, direction: str) -> None:
        """
        Sets the direction of this V2ConversationMessageTypingEventForUserTopicConversationNormalizedMessage.


        :param direction: The direction of this V2ConversationMessageTypingEventForUserTopicConversationNormalizedMessage.
        :type: str
        """
        if isinstance(direction, int):
            direction = str(direction)
        allowed_values = ["Inbound", "Outbound"]
        if direction.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for direction -> " + direction)
            self._direction = "outdated_sdk_version"
        else:
            self._direction = direction

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

