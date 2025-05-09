# coding: utf-8

"""
    AssistedInstall

    Assisted installation  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class L3Connectivity(object):
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
        'outgoing_nic': 'str',
        'remote_ip_address': 'str',
        'successful': 'bool',
        'average_rtt_ms': 'float',
        'packet_loss_percentage': 'float'
    }

    attribute_map = {
        'outgoing_nic': 'outgoing_nic',
        'remote_ip_address': 'remote_ip_address',
        'successful': 'successful',
        'average_rtt_ms': 'average_rtt_ms',
        'packet_loss_percentage': 'packet_loss_percentage'
    }

    def __init__(self, outgoing_nic=None, remote_ip_address=None, successful=None, average_rtt_ms=None, packet_loss_percentage=None):  # noqa: E501
        """L3Connectivity - a model defined in Swagger"""  # noqa: E501

        self._outgoing_nic = None
        self._remote_ip_address = None
        self._successful = None
        self._average_rtt_ms = None
        self._packet_loss_percentage = None
        self.discriminator = None

        if outgoing_nic is not None:
            self.outgoing_nic = outgoing_nic
        if remote_ip_address is not None:
            self.remote_ip_address = remote_ip_address
        if successful is not None:
            self.successful = successful
        if average_rtt_ms is not None:
            self.average_rtt_ms = average_rtt_ms
        if packet_loss_percentage is not None:
            self.packet_loss_percentage = packet_loss_percentage

    @property
    def outgoing_nic(self):
        """Gets the outgoing_nic of this L3Connectivity.  # noqa: E501


        :return: The outgoing_nic of this L3Connectivity.  # noqa: E501
        :rtype: str
        """
        return self._outgoing_nic

    @outgoing_nic.setter
    def outgoing_nic(self, outgoing_nic):
        """Sets the outgoing_nic of this L3Connectivity.


        :param outgoing_nic: The outgoing_nic of this L3Connectivity.  # noqa: E501
        :type: str
        """

        self._outgoing_nic = outgoing_nic

    @property
    def remote_ip_address(self):
        """Gets the remote_ip_address of this L3Connectivity.  # noqa: E501


        :return: The remote_ip_address of this L3Connectivity.  # noqa: E501
        :rtype: str
        """
        return self._remote_ip_address

    @remote_ip_address.setter
    def remote_ip_address(self, remote_ip_address):
        """Sets the remote_ip_address of this L3Connectivity.


        :param remote_ip_address: The remote_ip_address of this L3Connectivity.  # noqa: E501
        :type: str
        """

        self._remote_ip_address = remote_ip_address

    @property
    def successful(self):
        """Gets the successful of this L3Connectivity.  # noqa: E501


        :return: The successful of this L3Connectivity.  # noqa: E501
        :rtype: bool
        """
        return self._successful

    @successful.setter
    def successful(self, successful):
        """Sets the successful of this L3Connectivity.


        :param successful: The successful of this L3Connectivity.  # noqa: E501
        :type: bool
        """

        self._successful = successful

    @property
    def average_rtt_ms(self):
        """Gets the average_rtt_ms of this L3Connectivity.  # noqa: E501

        Average round trip time in milliseconds.  # noqa: E501

        :return: The average_rtt_ms of this L3Connectivity.  # noqa: E501
        :rtype: float
        """
        return self._average_rtt_ms

    @average_rtt_ms.setter
    def average_rtt_ms(self, average_rtt_ms):
        """Sets the average_rtt_ms of this L3Connectivity.

        Average round trip time in milliseconds.  # noqa: E501

        :param average_rtt_ms: The average_rtt_ms of this L3Connectivity.  # noqa: E501
        :type: float
        """

        self._average_rtt_ms = average_rtt_ms

    @property
    def packet_loss_percentage(self):
        """Gets the packet_loss_percentage of this L3Connectivity.  # noqa: E501

        Percentage of packets lost during connectivity check.  # noqa: E501

        :return: The packet_loss_percentage of this L3Connectivity.  # noqa: E501
        :rtype: float
        """
        return self._packet_loss_percentage

    @packet_loss_percentage.setter
    def packet_loss_percentage(self, packet_loss_percentage):
        """Sets the packet_loss_percentage of this L3Connectivity.

        Percentage of packets lost during connectivity check.  # noqa: E501

        :param packet_loss_percentage: The packet_loss_percentage of this L3Connectivity.  # noqa: E501
        :type: float
        """

        self._packet_loss_percentage = packet_loss_percentage

    def to_dict(self):
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
        if issubclass(L3Connectivity, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, L3Connectivity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
