r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IgroupInitiatorConnectivityTracking", "IgroupInitiatorConnectivityTrackingSchema"]
__pdoc__ = {
    "IgroupInitiatorConnectivityTrackingSchema.resource": False,
    "IgroupInitiatorConnectivityTrackingSchema.opts": False,
    "IgroupInitiatorConnectivityTracking": False,
}


class IgroupInitiatorConnectivityTrackingSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IgroupInitiatorConnectivityTracking object"""

    alerts = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.igroup_connectivity_tracking_alerts.IgroupConnectivityTrackingAlertsSchema", unknown=EXCLUDE, allow_none=True), data_key="alerts", allow_none=True)
    r""" The alerts field of the igroup_initiator_connectivity_tracking. """

    connection_state = marshmallow_fields.Str(data_key="connection_state", allow_none=True)
    r""" Connection state.


Valid choices:

* full
* none
* partial
* no_lun_maps """

    connections = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.igroup_initiator_connectivity_tracking_connections.IgroupInitiatorConnectivityTrackingConnectionsSchema", unknown=EXCLUDE, allow_none=True), data_key="connections", allow_none=True)
    r""" The connections field of the igroup_initiator_connectivity_tracking. """

    @property
    def resource(self):
        return IgroupInitiatorConnectivityTracking

    gettable_fields = [
        "alerts",
        "connection_state",
        "connections",
    ]
    """alerts,connection_state,connections,"""

    patchable_fields = [
        "connections",
    ]
    """connections,"""

    postable_fields = [
        "connections",
    ]
    """connections,"""


class IgroupInitiatorConnectivityTracking(Resource):

    _schema = IgroupInitiatorConnectivityTrackingSchema
