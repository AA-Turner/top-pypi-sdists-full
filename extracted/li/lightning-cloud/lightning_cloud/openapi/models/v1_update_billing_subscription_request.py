# coding: utf-8

"""
    external/v1/auth_service.proto

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: version not set
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    NOTE
    ----
    standard swagger-codegen-cli for this python client has been modified
    by custom templates. The purpose of these templates is to include
    typing information in the API and Model code. Please refer to the
    main grid repository for more info
"""

import pprint
import re  # noqa: F401

from typing import TYPE_CHECKING

import six

if TYPE_CHECKING:
    from datetime import datetime
    from lightning_cloud.openapi.models import *

class V1UpdateBillingSubscriptionRequest(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'billing_period': 'V1BillingPeriod',
        'org_id': 'str',
        'seats': 'int',
        'status': 'str'
    }

    attribute_map = {
        'billing_period': 'billingPeriod',
        'org_id': 'orgId',
        'seats': 'seats',
        'status': 'status'
    }

    def __init__(self, billing_period: 'V1BillingPeriod' =None, org_id: 'str' =None, seats: 'int' =None, status: 'str' =None):  # noqa: E501
        """V1UpdateBillingSubscriptionRequest - a model defined in Swagger"""  # noqa: E501
        self._billing_period = None
        self._org_id = None
        self._seats = None
        self._status = None
        self.discriminator = None
        if billing_period is not None:
            self.billing_period = billing_period
        if org_id is not None:
            self.org_id = org_id
        if seats is not None:
            self.seats = seats
        if status is not None:
            self.status = status

    @property
    def billing_period(self) -> 'V1BillingPeriod':
        """Gets the billing_period of this V1UpdateBillingSubscriptionRequest.  # noqa: E501


        :return: The billing_period of this V1UpdateBillingSubscriptionRequest.  # noqa: E501
        :rtype: V1BillingPeriod
        """
        return self._billing_period

    @billing_period.setter
    def billing_period(self, billing_period: 'V1BillingPeriod'):
        """Sets the billing_period of this V1UpdateBillingSubscriptionRequest.


        :param billing_period: The billing_period of this V1UpdateBillingSubscriptionRequest.  # noqa: E501
        :type: V1BillingPeriod
        """

        self._billing_period = billing_period

    @property
    def org_id(self) -> 'str':
        """Gets the org_id of this V1UpdateBillingSubscriptionRequest.  # noqa: E501


        :return: The org_id of this V1UpdateBillingSubscriptionRequest.  # noqa: E501
        :rtype: str
        """
        return self._org_id

    @org_id.setter
    def org_id(self, org_id: 'str'):
        """Sets the org_id of this V1UpdateBillingSubscriptionRequest.


        :param org_id: The org_id of this V1UpdateBillingSubscriptionRequest.  # noqa: E501
        :type: str
        """

        self._org_id = org_id

    @property
    def seats(self) -> 'int':
        """Gets the seats of this V1UpdateBillingSubscriptionRequest.  # noqa: E501


        :return: The seats of this V1UpdateBillingSubscriptionRequest.  # noqa: E501
        :rtype: int
        """
        return self._seats

    @seats.setter
    def seats(self, seats: 'int'):
        """Sets the seats of this V1UpdateBillingSubscriptionRequest.


        :param seats: The seats of this V1UpdateBillingSubscriptionRequest.  # noqa: E501
        :type: int
        """

        self._seats = seats

    @property
    def status(self) -> 'str':
        """Gets the status of this V1UpdateBillingSubscriptionRequest.  # noqa: E501


        :return: The status of this V1UpdateBillingSubscriptionRequest.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: 'str'):
        """Sets the status of this V1UpdateBillingSubscriptionRequest.


        :param status: The status of this V1UpdateBillingSubscriptionRequest.  # noqa: E501
        :type: str
        """

        self._status = status

    def to_dict(self) -> dict:
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(V1UpdateBillingSubscriptionRequest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1UpdateBillingSubscriptionRequest') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1UpdateBillingSubscriptionRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'V1UpdateBillingSubscriptionRequest') -> bool:
        """Returns true if both objects are not equal"""
        return not self == other
