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
    from . import AddressableEntityRef
    from . import DomainEntityRef

class WhatsAppConfig(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self) -> None:
        """
        WhatsAppConfig - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'whats_app_columns': 'list[str]',
            'whats_app_integration': 'AddressableEntityRef',
            'content_template': 'DomainEntityRef'
        }

        self.attribute_map = {
            'whats_app_columns': 'whatsAppColumns',
            'whats_app_integration': 'whatsAppIntegration',
            'content_template': 'contentTemplate'
        }

        self._whats_app_columns = None
        self._whats_app_integration = None
        self._content_template = None

    @property
    def whats_app_columns(self) -> List[str]:
        """
        Gets the whats_app_columns of this WhatsAppConfig.
        The contact list columns specifying the WhatsApp address(es) of the contact.

        :return: The whats_app_columns of this WhatsAppConfig.
        :rtype: list[str]
        """
        return self._whats_app_columns

    @whats_app_columns.setter
    def whats_app_columns(self, whats_app_columns: List[str]) -> None:
        """
        Sets the whats_app_columns of this WhatsAppConfig.
        The contact list columns specifying the WhatsApp address(es) of the contact.

        :param whats_app_columns: The whats_app_columns of this WhatsAppConfig.
        :type: list[str]
        """
        

        self._whats_app_columns = whats_app_columns

    @property
    def whats_app_integration(self) -> 'AddressableEntityRef':
        """
        Gets the whats_app_integration of this WhatsAppConfig.
        The WhatsApp integration used to send message to the contact.

        :return: The whats_app_integration of this WhatsAppConfig.
        :rtype: AddressableEntityRef
        """
        return self._whats_app_integration

    @whats_app_integration.setter
    def whats_app_integration(self, whats_app_integration: 'AddressableEntityRef') -> None:
        """
        Sets the whats_app_integration of this WhatsAppConfig.
        The WhatsApp integration used to send message to the contact.

        :param whats_app_integration: The whats_app_integration of this WhatsAppConfig.
        :type: AddressableEntityRef
        """
        

        self._whats_app_integration = whats_app_integration

    @property
    def content_template(self) -> 'DomainEntityRef':
        """
        Gets the content_template of this WhatsAppConfig.
        The content template used to formulate the WhatsApp message to send to the contact.

        :return: The content_template of this WhatsAppConfig.
        :rtype: DomainEntityRef
        """
        return self._content_template

    @content_template.setter
    def content_template(self, content_template: 'DomainEntityRef') -> None:
        """
        Sets the content_template of this WhatsAppConfig.
        The content template used to formulate the WhatsApp message to send to the contact.

        :param content_template: The content_template of this WhatsAppConfig.
        :type: DomainEntityRef
        """
        

        self._content_template = content_template

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

