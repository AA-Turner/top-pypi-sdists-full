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
    from . import ContentDatePickerAvailableTime

class ContentDatePicker(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self) -> None:
        """
        ContentDatePicker - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'title': 'str',
            'subtitle': 'str',
            'image_url': 'str',
            'date_minimum': 'datetime',
            'date_maximum': 'datetime',
            'available_times': 'list[ContentDatePickerAvailableTime]'
        }

        self.attribute_map = {
            'title': 'title',
            'subtitle': 'subtitle',
            'image_url': 'imageUrl',
            'date_minimum': 'dateMinimum',
            'date_maximum': 'dateMaximum',
            'available_times': 'availableTimes'
        }

        self._title = None
        self._subtitle = None
        self._image_url = None
        self._date_minimum = None
        self._date_maximum = None
        self._available_times = None

    @property
    def title(self) -> str:
        """
        Gets the title of this ContentDatePicker.
        Text to show in the title.

        :return: The title of this ContentDatePicker.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        """
        Sets the title of this ContentDatePicker.
        Text to show in the title.

        :param title: The title of this ContentDatePicker.
        :type: str
        """
        

        self._title = title

    @property
    def subtitle(self) -> str:
        """
        Gets the subtitle of this ContentDatePicker.
        Text to show in the description.

        :return: The subtitle of this ContentDatePicker.
        :rtype: str
        """
        return self._subtitle

    @subtitle.setter
    def subtitle(self, subtitle: str) -> None:
        """
        Sets the subtitle of this ContentDatePicker.
        Text to show in the description.

        :param subtitle: The subtitle of this ContentDatePicker.
        :type: str
        """
        

        self._subtitle = subtitle

    @property
    def image_url(self) -> str:
        """
        Gets the image_url of this ContentDatePicker.
        URL of an image

        :return: The image_url of this ContentDatePicker.
        :rtype: str
        """
        return self._image_url

    @image_url.setter
    def image_url(self, image_url: str) -> None:
        """
        Sets the image_url of this ContentDatePicker.
        URL of an image

        :param image_url: The image_url of this ContentDatePicker.
        :type: str
        """
        

        self._image_url = image_url

    @property
    def date_minimum(self) -> datetime:
        """
        Gets the date_minimum of this ContentDatePicker.
        The minimum Date Enabled in the datepicker calendar. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_minimum of this ContentDatePicker.
        :rtype: datetime
        """
        return self._date_minimum

    @date_minimum.setter
    def date_minimum(self, date_minimum: datetime) -> None:
        """
        Sets the date_minimum of this ContentDatePicker.
        The minimum Date Enabled in the datepicker calendar. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_minimum: The date_minimum of this ContentDatePicker.
        :type: datetime
        """
        

        self._date_minimum = date_minimum

    @property
    def date_maximum(self) -> datetime:
        """
        Gets the date_maximum of this ContentDatePicker.
        The maximum Date Enabled in the datepicker calendar. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_maximum of this ContentDatePicker.
        :rtype: datetime
        """
        return self._date_maximum

    @date_maximum.setter
    def date_maximum(self, date_maximum: datetime) -> None:
        """
        Sets the date_maximum of this ContentDatePicker.
        The maximum Date Enabled in the datepicker calendar. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_maximum: The date_maximum of this ContentDatePicker.
        :type: datetime
        """
        

        self._date_maximum = date_maximum

    @property
    def available_times(self) -> List['ContentDatePickerAvailableTime']:
        """
        Gets the available_times of this ContentDatePicker.
        An array of available times objects.

        :return: The available_times of this ContentDatePicker.
        :rtype: list[ContentDatePickerAvailableTime]
        """
        return self._available_times

    @available_times.setter
    def available_times(self, available_times: List['ContentDatePickerAvailableTime']) -> None:
        """
        Sets the available_times of this ContentDatePicker.
        An array of available times objects.

        :param available_times: The available_times of this ContentDatePicker.
        :type: list[ContentDatePickerAvailableTime]
        """
        

        self._available_times = available_times

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

