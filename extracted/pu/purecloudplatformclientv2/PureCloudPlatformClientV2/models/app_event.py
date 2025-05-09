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
    from . import CustomEventAttribute
    from . import Device
    from . import JourneyApp
    from . import JourneyCampaign
    from . import JourneyGeolocation
    from . import NetworkConnectivity
    from . import SdkLibrary

class AppEvent(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self) -> None:
        """
        AppEvent - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'event_name': 'str',
            'screen_name': 'str',
            'app': 'JourneyApp',
            'device': 'Device',
            'ip_address': 'str',
            'ip_organization': 'str',
            'geolocation': 'JourneyGeolocation',
            'sdk_library': 'SdkLibrary',
            'network_connectivity': 'NetworkConnectivity',
            'mkt_campaign': 'JourneyCampaign',
            'search_query': 'str',
            'attributes': 'dict(str, CustomEventAttribute)',
            'traits': 'dict(str, CustomEventAttribute)'
        }

        self.attribute_map = {
            'event_name': 'eventName',
            'screen_name': 'screenName',
            'app': 'app',
            'device': 'device',
            'ip_address': 'ipAddress',
            'ip_organization': 'ipOrganization',
            'geolocation': 'geolocation',
            'sdk_library': 'sdkLibrary',
            'network_connectivity': 'networkConnectivity',
            'mkt_campaign': 'mktCampaign',
            'search_query': 'searchQuery',
            'attributes': 'attributes',
            'traits': 'traits'
        }

        self._event_name = None
        self._screen_name = None
        self._app = None
        self._device = None
        self._ip_address = None
        self._ip_organization = None
        self._geolocation = None
        self._sdk_library = None
        self._network_connectivity = None
        self._mkt_campaign = None
        self._search_query = None
        self._attributes = None
        self._traits = None

    @property
    def event_name(self) -> str:
        """
        Gets the event_name of this AppEvent.
        Represents the action the customer performed. A good event name is typically an object followed by the action performed in past tense (e.g. screen_viewed, order_completed, user_registered).

        :return: The event_name of this AppEvent.
        :rtype: str
        """
        return self._event_name

    @event_name.setter
    def event_name(self, event_name: str) -> None:
        """
        Sets the event_name of this AppEvent.
        Represents the action the customer performed. A good event name is typically an object followed by the action performed in past tense (e.g. screen_viewed, order_completed, user_registered).

        :param event_name: The event_name of this AppEvent.
        :type: str
        """
        

        self._event_name = event_name

    @property
    def screen_name(self) -> str:
        """
        Gets the screen_name of this AppEvent.
        The name of the screen in the app that the event took place.

        :return: The screen_name of this AppEvent.
        :rtype: str
        """
        return self._screen_name

    @screen_name.setter
    def screen_name(self, screen_name: str) -> None:
        """
        Sets the screen_name of this AppEvent.
        The name of the screen in the app that the event took place.

        :param screen_name: The screen_name of this AppEvent.
        :type: str
        """
        

        self._screen_name = screen_name

    @property
    def app(self) -> 'JourneyApp':
        """
        Gets the app of this AppEvent.
        Application that the customer is interacting with.

        :return: The app of this AppEvent.
        :rtype: JourneyApp
        """
        return self._app

    @app.setter
    def app(self, app: 'JourneyApp') -> None:
        """
        Sets the app of this AppEvent.
        Application that the customer is interacting with.

        :param app: The app of this AppEvent.
        :type: JourneyApp
        """
        

        self._app = app

    @property
    def device(self) -> 'Device':
        """
        Gets the device of this AppEvent.
        Customer's device.

        :return: The device of this AppEvent.
        :rtype: Device
        """
        return self._device

    @device.setter
    def device(self, device: 'Device') -> None:
        """
        Sets the device of this AppEvent.
        Customer's device.

        :param device: The device of this AppEvent.
        :type: Device
        """
        

        self._device = device

    @property
    def ip_address(self) -> str:
        """
        Gets the ip_address of this AppEvent.
        Customer's IP address. May be null if the business configures the tracker to not collect IP addresses.

        :return: The ip_address of this AppEvent.
        :rtype: str
        """
        return self._ip_address

    @ip_address.setter
    def ip_address(self, ip_address: str) -> None:
        """
        Sets the ip_address of this AppEvent.
        Customer's IP address. May be null if the business configures the tracker to not collect IP addresses.

        :param ip_address: The ip_address of this AppEvent.
        :type: str
        """
        

        self._ip_address = ip_address

    @property
    def ip_organization(self) -> str:
        """
        Gets the ip_organization of this AppEvent.
        Customer's IP-based organization or ISP name.

        :return: The ip_organization of this AppEvent.
        :rtype: str
        """
        return self._ip_organization

    @ip_organization.setter
    def ip_organization(self, ip_organization: str) -> None:
        """
        Sets the ip_organization of this AppEvent.
        Customer's IP-based organization or ISP name.

        :param ip_organization: The ip_organization of this AppEvent.
        :type: str
        """
        

        self._ip_organization = ip_organization

    @property
    def geolocation(self) -> 'JourneyGeolocation':
        """
        Gets the geolocation of this AppEvent.
        Customer's geolocation.

        :return: The geolocation of this AppEvent.
        :rtype: JourneyGeolocation
        """
        return self._geolocation

    @geolocation.setter
    def geolocation(self, geolocation: 'JourneyGeolocation') -> None:
        """
        Sets the geolocation of this AppEvent.
        Customer's geolocation.

        :param geolocation: The geolocation of this AppEvent.
        :type: JourneyGeolocation
        """
        

        self._geolocation = geolocation

    @property
    def sdk_library(self) -> 'SdkLibrary':
        """
        Gets the sdk_library of this AppEvent.
        SDK library used to generate the event.

        :return: The sdk_library of this AppEvent.
        :rtype: SdkLibrary
        """
        return self._sdk_library

    @sdk_library.setter
    def sdk_library(self, sdk_library: 'SdkLibrary') -> None:
        """
        Sets the sdk_library of this AppEvent.
        SDK library used to generate the event.

        :param sdk_library: The sdk_library of this AppEvent.
        :type: SdkLibrary
        """
        

        self._sdk_library = sdk_library

    @property
    def network_connectivity(self) -> 'NetworkConnectivity':
        """
        Gets the network_connectivity of this AppEvent.
        Information relating to the device's network connectivity.

        :return: The network_connectivity of this AppEvent.
        :rtype: NetworkConnectivity
        """
        return self._network_connectivity

    @network_connectivity.setter
    def network_connectivity(self, network_connectivity: 'NetworkConnectivity') -> None:
        """
        Sets the network_connectivity of this AppEvent.
        Information relating to the device's network connectivity.

        :param network_connectivity: The network_connectivity of this AppEvent.
        :type: NetworkConnectivity
        """
        

        self._network_connectivity = network_connectivity

    @property
    def mkt_campaign(self) -> 'JourneyCampaign':
        """
        Gets the mkt_campaign of this AppEvent.
        Marketing / traffic source information.

        :return: The mkt_campaign of this AppEvent.
        :rtype: JourneyCampaign
        """
        return self._mkt_campaign

    @mkt_campaign.setter
    def mkt_campaign(self, mkt_campaign: 'JourneyCampaign') -> None:
        """
        Sets the mkt_campaign of this AppEvent.
        Marketing / traffic source information.

        :param mkt_campaign: The mkt_campaign of this AppEvent.
        :type: JourneyCampaign
        """
        

        self._mkt_campaign = mkt_campaign

    @property
    def search_query(self) -> str:
        """
        Gets the search_query of this AppEvent.
        Represents the keywords in a customer search query.

        :return: The search_query of this AppEvent.
        :rtype: str
        """
        return self._search_query

    @search_query.setter
    def search_query(self, search_query: str) -> None:
        """
        Sets the search_query of this AppEvent.
        Represents the keywords in a customer search query.

        :param search_query: The search_query of this AppEvent.
        :type: str
        """
        

        self._search_query = search_query

    @property
    def attributes(self) -> Dict[str, 'CustomEventAttribute']:
        """
        Gets the attributes of this AppEvent.
        User-defined attributes associated with a particular event.

        :return: The attributes of this AppEvent.
        :rtype: dict(str, CustomEventAttribute)
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes: Dict[str, 'CustomEventAttribute']) -> None:
        """
        Sets the attributes of this AppEvent.
        User-defined attributes associated with a particular event.

        :param attributes: The attributes of this AppEvent.
        :type: dict(str, CustomEventAttribute)
        """
        

        self._attributes = attributes

    @property
    def traits(self) -> Dict[str, 'CustomEventAttribute']:
        """
        Gets the traits of this AppEvent.
        Traits are attributes intrinsic to the customer that may be sent in selected events. Examples are email, givenName, cellPhone.

        :return: The traits of this AppEvent.
        :rtype: dict(str, CustomEventAttribute)
        """
        return self._traits

    @traits.setter
    def traits(self, traits: Dict[str, 'CustomEventAttribute']) -> None:
        """
        Sets the traits of this AppEvent.
        Traits are attributes intrinsic to the customer that may be sent in selected events. Examples are email, givenName, cellPhone.

        :param traits: The traits of this AppEvent.
        :type: dict(str, CustomEventAttribute)
        """
        

        self._traits = traits

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

