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
    from . import KeyValue
    from . import ServiceLevel

class ActionTarget(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self) -> None:
        """
        ActionTarget - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'user_data': 'list[KeyValue]',
            'supported_media_types': 'list[str]',
            'state': 'str',
            'description': 'str',
            'service_level': 'ServiceLevel',
            'short_abandon_threshold': 'int',
            'self_uri': 'str',
            'created_date': 'datetime',
            'modified_date': 'datetime'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'user_data': 'userData',
            'supported_media_types': 'supportedMediaTypes',
            'state': 'state',
            'description': 'description',
            'service_level': 'serviceLevel',
            'short_abandon_threshold': 'shortAbandonThreshold',
            'self_uri': 'selfUri',
            'created_date': 'createdDate',
            'modified_date': 'modifiedDate'
        }

        self._id = None
        self._name = None
        self._user_data = None
        self._supported_media_types = None
        self._state = None
        self._description = None
        self._service_level = None
        self._short_abandon_threshold = None
        self._self_uri = None
        self._created_date = None
        self._modified_date = None

    @property
    def id(self) -> str:
        """
        Gets the id of this ActionTarget.
        The globally unique identifier for the object.

        :return: The id of this ActionTarget.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str) -> None:
        """
        Sets the id of this ActionTarget.
        The globally unique identifier for the object.

        :param id: The id of this ActionTarget.
        :type: str
        """
        

        self._id = id

    @property
    def name(self) -> str:
        """
        Gets the name of this ActionTarget.


        :return: The name of this ActionTarget.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """
        Sets the name of this ActionTarget.


        :param name: The name of this ActionTarget.
        :type: str
        """
        

        self._name = name

    @property
    def user_data(self) -> List['KeyValue']:
        """
        Gets the user_data of this ActionTarget.
        Additional user data associated with the target in key/value format.

        :return: The user_data of this ActionTarget.
        :rtype: list[KeyValue]
        """
        return self._user_data

    @user_data.setter
    def user_data(self, user_data: List['KeyValue']) -> None:
        """
        Sets the user_data of this ActionTarget.
        Additional user data associated with the target in key/value format.

        :param user_data: The user_data of this ActionTarget.
        :type: list[KeyValue]
        """
        

        self._user_data = user_data

    @property
    def supported_media_types(self) -> List[str]:
        """
        Gets the supported_media_types of this ActionTarget.
        Supported media types of the target.

        :return: The supported_media_types of this ActionTarget.
        :rtype: list[str]
        """
        return self._supported_media_types

    @supported_media_types.setter
    def supported_media_types(self, supported_media_types: List[str]) -> None:
        """
        Sets the supported_media_types of this ActionTarget.
        Supported media types of the target.

        :param supported_media_types: The supported_media_types of this ActionTarget.
        :type: list[str]
        """
        

        self._supported_media_types = supported_media_types

    @property
    def state(self) -> str:
        """
        Gets the state of this ActionTarget.
        Indicates the state of the target.

        :return: The state of this ActionTarget.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state: str) -> None:
        """
        Sets the state of this ActionTarget.
        Indicates the state of the target.

        :param state: The state of this ActionTarget.
        :type: str
        """
        if isinstance(state, int):
            state = str(state)
        allowed_values = ["active", "inactive", "deleted"]
        if state.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for state -> " + state)
            self._state = "outdated_sdk_version"
        else:
            self._state = state

    @property
    def description(self) -> str:
        """
        Gets the description of this ActionTarget.
        Description of the target.

        :return: The description of this ActionTarget.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        """
        Sets the description of this ActionTarget.
        Description of the target.

        :param description: The description of this ActionTarget.
        :type: str
        """
        

        self._description = description

    @property
    def service_level(self) -> 'ServiceLevel':
        """
        Gets the service_level of this ActionTarget.
        Service Level of the action target. Chat offers for the target will be throttled with the aim of achieving this service level.

        :return: The service_level of this ActionTarget.
        :rtype: ServiceLevel
        """
        return self._service_level

    @service_level.setter
    def service_level(self, service_level: 'ServiceLevel') -> None:
        """
        Sets the service_level of this ActionTarget.
        Service Level of the action target. Chat offers for the target will be throttled with the aim of achieving this service level.

        :param service_level: The service_level of this ActionTarget.
        :type: ServiceLevel
        """
        

        self._service_level = service_level

    @property
    def short_abandon_threshold(self) -> int:
        """
        Gets the short_abandon_threshold of this ActionTarget.
        Indicates the non-default short abandon threshold

        :return: The short_abandon_threshold of this ActionTarget.
        :rtype: int
        """
        return self._short_abandon_threshold

    @short_abandon_threshold.setter
    def short_abandon_threshold(self, short_abandon_threshold: int) -> None:
        """
        Sets the short_abandon_threshold of this ActionTarget.
        Indicates the non-default short abandon threshold

        :param short_abandon_threshold: The short_abandon_threshold of this ActionTarget.
        :type: int
        """
        

        self._short_abandon_threshold = short_abandon_threshold

    @property
    def self_uri(self) -> str:
        """
        Gets the self_uri of this ActionTarget.
        The URI for this object

        :return: The self_uri of this ActionTarget.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri: str) -> None:
        """
        Sets the self_uri of this ActionTarget.
        The URI for this object

        :param self_uri: The self_uri of this ActionTarget.
        :type: str
        """
        

        self._self_uri = self_uri

    @property
    def created_date(self) -> datetime:
        """
        Gets the created_date of this ActionTarget.
        The date the target was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The created_date of this ActionTarget.
        :rtype: datetime
        """
        return self._created_date

    @created_date.setter
    def created_date(self, created_date: datetime) -> None:
        """
        Sets the created_date of this ActionTarget.
        The date the target was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param created_date: The created_date of this ActionTarget.
        :type: datetime
        """
        

        self._created_date = created_date

    @property
    def modified_date(self) -> datetime:
        """
        Gets the modified_date of this ActionTarget.
        The date the target was last modified. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The modified_date of this ActionTarget.
        :rtype: datetime
        """
        return self._modified_date

    @modified_date.setter
    def modified_date(self, modified_date: datetime) -> None:
        """
        Sets the modified_date of this ActionTarget.
        The date the target was last modified. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param modified_date: The modified_date of this ActionTarget.
        :type: datetime
        """
        

        self._modified_date = modified_date

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

