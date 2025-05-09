# coding: utf-8

"""
    transitrouter

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput(object):
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
        'auto_publish_route_enabled': 'bool',
        'bandwidth': 'int',
        'creation_time': 'str',
        'description': 'str',
        'peer_transit_router_id': 'str',
        'peer_transit_router_region_id': 'str',
        'status': 'str',
        'tags': 'list[TagForDescribeTransitRouterPeerAttachmentsOutput]',
        'transit_router_attachment_id': 'str',
        'transit_router_attachment_name': 'str',
        'transit_router_bandwidth_package_id': 'str',
        'transit_router_forward_policy_table_id': 'str',
        'transit_router_id': 'str',
        'transit_router_route_table_id': 'str',
        'transit_router_traffic_qos_marking_policy_id': 'str',
        'transit_router_traffic_qos_queue_policy_id': 'str',
        'update_time': 'str'
    }

    attribute_map = {
        'auto_publish_route_enabled': 'AutoPublishRouteEnabled',
        'bandwidth': 'Bandwidth',
        'creation_time': 'CreationTime',
        'description': 'Description',
        'peer_transit_router_id': 'PeerTransitRouterId',
        'peer_transit_router_region_id': 'PeerTransitRouterRegionId',
        'status': 'Status',
        'tags': 'Tags',
        'transit_router_attachment_id': 'TransitRouterAttachmentId',
        'transit_router_attachment_name': 'TransitRouterAttachmentName',
        'transit_router_bandwidth_package_id': 'TransitRouterBandwidthPackageId',
        'transit_router_forward_policy_table_id': 'TransitRouterForwardPolicyTableId',
        'transit_router_id': 'TransitRouterId',
        'transit_router_route_table_id': 'TransitRouterRouteTableId',
        'transit_router_traffic_qos_marking_policy_id': 'TransitRouterTrafficQosMarkingPolicyId',
        'transit_router_traffic_qos_queue_policy_id': 'TransitRouterTrafficQosQueuePolicyId',
        'update_time': 'UpdateTime'
    }

    def __init__(self, auto_publish_route_enabled=None, bandwidth=None, creation_time=None, description=None, peer_transit_router_id=None, peer_transit_router_region_id=None, status=None, tags=None, transit_router_attachment_id=None, transit_router_attachment_name=None, transit_router_bandwidth_package_id=None, transit_router_forward_policy_table_id=None, transit_router_id=None, transit_router_route_table_id=None, transit_router_traffic_qos_marking_policy_id=None, transit_router_traffic_qos_queue_policy_id=None, update_time=None, _configuration=None):  # noqa: E501
        """TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._auto_publish_route_enabled = None
        self._bandwidth = None
        self._creation_time = None
        self._description = None
        self._peer_transit_router_id = None
        self._peer_transit_router_region_id = None
        self._status = None
        self._tags = None
        self._transit_router_attachment_id = None
        self._transit_router_attachment_name = None
        self._transit_router_bandwidth_package_id = None
        self._transit_router_forward_policy_table_id = None
        self._transit_router_id = None
        self._transit_router_route_table_id = None
        self._transit_router_traffic_qos_marking_policy_id = None
        self._transit_router_traffic_qos_queue_policy_id = None
        self._update_time = None
        self.discriminator = None

        if auto_publish_route_enabled is not None:
            self.auto_publish_route_enabled = auto_publish_route_enabled
        if bandwidth is not None:
            self.bandwidth = bandwidth
        if creation_time is not None:
            self.creation_time = creation_time
        if description is not None:
            self.description = description
        if peer_transit_router_id is not None:
            self.peer_transit_router_id = peer_transit_router_id
        if peer_transit_router_region_id is not None:
            self.peer_transit_router_region_id = peer_transit_router_region_id
        if status is not None:
            self.status = status
        if tags is not None:
            self.tags = tags
        if transit_router_attachment_id is not None:
            self.transit_router_attachment_id = transit_router_attachment_id
        if transit_router_attachment_name is not None:
            self.transit_router_attachment_name = transit_router_attachment_name
        if transit_router_bandwidth_package_id is not None:
            self.transit_router_bandwidth_package_id = transit_router_bandwidth_package_id
        if transit_router_forward_policy_table_id is not None:
            self.transit_router_forward_policy_table_id = transit_router_forward_policy_table_id
        if transit_router_id is not None:
            self.transit_router_id = transit_router_id
        if transit_router_route_table_id is not None:
            self.transit_router_route_table_id = transit_router_route_table_id
        if transit_router_traffic_qos_marking_policy_id is not None:
            self.transit_router_traffic_qos_marking_policy_id = transit_router_traffic_qos_marking_policy_id
        if transit_router_traffic_qos_queue_policy_id is not None:
            self.transit_router_traffic_qos_queue_policy_id = transit_router_traffic_qos_queue_policy_id
        if update_time is not None:
            self.update_time = update_time

    @property
    def auto_publish_route_enabled(self):
        """Gets the auto_publish_route_enabled of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501


        :return: The auto_publish_route_enabled of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :rtype: bool
        """
        return self._auto_publish_route_enabled

    @auto_publish_route_enabled.setter
    def auto_publish_route_enabled(self, auto_publish_route_enabled):
        """Sets the auto_publish_route_enabled of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.


        :param auto_publish_route_enabled: The auto_publish_route_enabled of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :type: bool
        """

        self._auto_publish_route_enabled = auto_publish_route_enabled

    @property
    def bandwidth(self):
        """Gets the bandwidth of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501


        :return: The bandwidth of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :rtype: int
        """
        return self._bandwidth

    @bandwidth.setter
    def bandwidth(self, bandwidth):
        """Sets the bandwidth of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.


        :param bandwidth: The bandwidth of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :type: int
        """

        self._bandwidth = bandwidth

    @property
    def creation_time(self):
        """Gets the creation_time of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501


        :return: The creation_time of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :rtype: str
        """
        return self._creation_time

    @creation_time.setter
    def creation_time(self, creation_time):
        """Sets the creation_time of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.


        :param creation_time: The creation_time of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :type: str
        """

        self._creation_time = creation_time

    @property
    def description(self):
        """Gets the description of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501


        :return: The description of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.


        :param description: The description of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def peer_transit_router_id(self):
        """Gets the peer_transit_router_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501


        :return: The peer_transit_router_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :rtype: str
        """
        return self._peer_transit_router_id

    @peer_transit_router_id.setter
    def peer_transit_router_id(self, peer_transit_router_id):
        """Sets the peer_transit_router_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.


        :param peer_transit_router_id: The peer_transit_router_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :type: str
        """

        self._peer_transit_router_id = peer_transit_router_id

    @property
    def peer_transit_router_region_id(self):
        """Gets the peer_transit_router_region_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501


        :return: The peer_transit_router_region_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :rtype: str
        """
        return self._peer_transit_router_region_id

    @peer_transit_router_region_id.setter
    def peer_transit_router_region_id(self, peer_transit_router_region_id):
        """Sets the peer_transit_router_region_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.


        :param peer_transit_router_region_id: The peer_transit_router_region_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :type: str
        """

        self._peer_transit_router_region_id = peer_transit_router_region_id

    @property
    def status(self):
        """Gets the status of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501


        :return: The status of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.


        :param status: The status of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def tags(self):
        """Gets the tags of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501


        :return: The tags of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :rtype: list[TagForDescribeTransitRouterPeerAttachmentsOutput]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.


        :param tags: The tags of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :type: list[TagForDescribeTransitRouterPeerAttachmentsOutput]
        """

        self._tags = tags

    @property
    def transit_router_attachment_id(self):
        """Gets the transit_router_attachment_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501


        :return: The transit_router_attachment_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :rtype: str
        """
        return self._transit_router_attachment_id

    @transit_router_attachment_id.setter
    def transit_router_attachment_id(self, transit_router_attachment_id):
        """Sets the transit_router_attachment_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.


        :param transit_router_attachment_id: The transit_router_attachment_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :type: str
        """

        self._transit_router_attachment_id = transit_router_attachment_id

    @property
    def transit_router_attachment_name(self):
        """Gets the transit_router_attachment_name of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501


        :return: The transit_router_attachment_name of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :rtype: str
        """
        return self._transit_router_attachment_name

    @transit_router_attachment_name.setter
    def transit_router_attachment_name(self, transit_router_attachment_name):
        """Sets the transit_router_attachment_name of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.


        :param transit_router_attachment_name: The transit_router_attachment_name of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :type: str
        """

        self._transit_router_attachment_name = transit_router_attachment_name

    @property
    def transit_router_bandwidth_package_id(self):
        """Gets the transit_router_bandwidth_package_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501


        :return: The transit_router_bandwidth_package_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :rtype: str
        """
        return self._transit_router_bandwidth_package_id

    @transit_router_bandwidth_package_id.setter
    def transit_router_bandwidth_package_id(self, transit_router_bandwidth_package_id):
        """Sets the transit_router_bandwidth_package_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.


        :param transit_router_bandwidth_package_id: The transit_router_bandwidth_package_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :type: str
        """

        self._transit_router_bandwidth_package_id = transit_router_bandwidth_package_id

    @property
    def transit_router_forward_policy_table_id(self):
        """Gets the transit_router_forward_policy_table_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501


        :return: The transit_router_forward_policy_table_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :rtype: str
        """
        return self._transit_router_forward_policy_table_id

    @transit_router_forward_policy_table_id.setter
    def transit_router_forward_policy_table_id(self, transit_router_forward_policy_table_id):
        """Sets the transit_router_forward_policy_table_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.


        :param transit_router_forward_policy_table_id: The transit_router_forward_policy_table_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :type: str
        """

        self._transit_router_forward_policy_table_id = transit_router_forward_policy_table_id

    @property
    def transit_router_id(self):
        """Gets the transit_router_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501


        :return: The transit_router_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :rtype: str
        """
        return self._transit_router_id

    @transit_router_id.setter
    def transit_router_id(self, transit_router_id):
        """Sets the transit_router_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.


        :param transit_router_id: The transit_router_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :type: str
        """

        self._transit_router_id = transit_router_id

    @property
    def transit_router_route_table_id(self):
        """Gets the transit_router_route_table_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501


        :return: The transit_router_route_table_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :rtype: str
        """
        return self._transit_router_route_table_id

    @transit_router_route_table_id.setter
    def transit_router_route_table_id(self, transit_router_route_table_id):
        """Sets the transit_router_route_table_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.


        :param transit_router_route_table_id: The transit_router_route_table_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :type: str
        """

        self._transit_router_route_table_id = transit_router_route_table_id

    @property
    def transit_router_traffic_qos_marking_policy_id(self):
        """Gets the transit_router_traffic_qos_marking_policy_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501


        :return: The transit_router_traffic_qos_marking_policy_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :rtype: str
        """
        return self._transit_router_traffic_qos_marking_policy_id

    @transit_router_traffic_qos_marking_policy_id.setter
    def transit_router_traffic_qos_marking_policy_id(self, transit_router_traffic_qos_marking_policy_id):
        """Sets the transit_router_traffic_qos_marking_policy_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.


        :param transit_router_traffic_qos_marking_policy_id: The transit_router_traffic_qos_marking_policy_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :type: str
        """

        self._transit_router_traffic_qos_marking_policy_id = transit_router_traffic_qos_marking_policy_id

    @property
    def transit_router_traffic_qos_queue_policy_id(self):
        """Gets the transit_router_traffic_qos_queue_policy_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501


        :return: The transit_router_traffic_qos_queue_policy_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :rtype: str
        """
        return self._transit_router_traffic_qos_queue_policy_id

    @transit_router_traffic_qos_queue_policy_id.setter
    def transit_router_traffic_qos_queue_policy_id(self, transit_router_traffic_qos_queue_policy_id):
        """Sets the transit_router_traffic_qos_queue_policy_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.


        :param transit_router_traffic_qos_queue_policy_id: The transit_router_traffic_qos_queue_policy_id of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :type: str
        """

        self._transit_router_traffic_qos_queue_policy_id = transit_router_traffic_qos_queue_policy_id

    @property
    def update_time(self):
        """Gets the update_time of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501


        :return: The update_time of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :rtype: str
        """
        return self._update_time

    @update_time.setter
    def update_time(self, update_time):
        """Sets the update_time of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.


        :param update_time: The update_time of this TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput.  # noqa: E501
        :type: str
        """

        self._update_time = update_time

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
        if issubclass(TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput, dict):
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
        if not isinstance(other, TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TransitRouterAttachmentForDescribeTransitRouterPeerAttachmentsOutput):
            return True

        return self.to_dict() != other.to_dict()
