r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IgroupInitiatorConnectivityTrackingConnectionsLoginsInterface", "IgroupInitiatorConnectivityTrackingConnectionsLoginsInterfaceSchema"]
__pdoc__ = {
    "IgroupInitiatorConnectivityTrackingConnectionsLoginsInterfaceSchema.resource": False,
    "IgroupInitiatorConnectivityTrackingConnectionsLoginsInterfaceSchema.opts": False,
    "IgroupInitiatorConnectivityTrackingConnectionsLoginsInterface": False,
}


class IgroupInitiatorConnectivityTrackingConnectionsLoginsInterfaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IgroupInitiatorConnectivityTrackingConnectionsLoginsInterface object"""

    fc = marshmallow_fields.Nested("netapp_ontap.resources.fc_interface.FcInterfaceSchema", unknown=EXCLUDE, data_key="fc", allow_none=True)
    r""" The fc field of the igroup_initiator_connectivity_tracking_connections_logins_interface. """

    ip = marshmallow_fields.Nested("netapp_ontap.resources.ip_interface.IpInterfaceSchema", unknown=EXCLUDE, data_key="ip", allow_none=True)
    r""" The ip field of the igroup_initiator_connectivity_tracking_connections_logins_interface. """

    @property
    def resource(self):
        return IgroupInitiatorConnectivityTrackingConnectionsLoginsInterface

    gettable_fields = [
        "fc.links",
        "fc.name",
        "fc.uuid",
        "fc.wwpn",
        "ip.links",
        "ip.ip",
        "ip.name",
        "ip.uuid",
    ]
    """fc.links,fc.name,fc.uuid,fc.wwpn,ip.links,ip.ip,ip.name,ip.uuid,"""

    patchable_fields = [
        "fc.name",
        "fc.uuid",
        "ip.name",
        "ip.uuid",
    ]
    """fc.name,fc.uuid,ip.name,ip.uuid,"""

    postable_fields = [
        "fc.name",
        "fc.uuid",
        "ip.name",
        "ip.uuid",
    ]
    """fc.name,fc.uuid,ip.name,ip.uuid,"""


class IgroupInitiatorConnectivityTrackingConnectionsLoginsInterface(Resource):

    _schema = IgroupInitiatorConnectivityTrackingConnectionsLoginsInterfaceSchema
