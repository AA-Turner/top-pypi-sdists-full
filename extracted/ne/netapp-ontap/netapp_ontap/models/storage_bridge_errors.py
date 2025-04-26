r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageBridgeErrors", "StorageBridgeErrorsSchema"]
__pdoc__ = {
    "StorageBridgeErrorsSchema.resource": False,
    "StorageBridgeErrorsSchema.opts": False,
    "StorageBridgeErrors": False,
}


class StorageBridgeErrorsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageBridgeErrors object"""

    component = marshmallow_fields.Nested("netapp_ontap.models.storage_bridge_errors_component.StorageBridgeErrorsComponentSchema", unknown=EXCLUDE, data_key="component", allow_none=True)
    r""" The component field of the storage_bridge_errors. """

    reason = marshmallow_fields.Nested("netapp_ontap.models.error.ErrorSchema", unknown=EXCLUDE, data_key="reason", allow_none=True)
    r""" The reason field of the storage_bridge_errors. """

    severity = marshmallow_fields.Str(data_key="severity", allow_none=True)
    r""" Bridge error severity

Valid choices:

* unknown
* notice
* warning
* error """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Bridge error type

Valid choices:

* unknown
* bridge_unreachable
* temp_above_critical_level
* temp_below_critical_level
* temp_sensor_status_critical
* temp_sensor_status_unavailable
* invalid_configuration
* sas_port_offline
* link_failure
* sas_port_online
* power_supply_offline """

    @property
    def resource(self):
        return StorageBridgeErrors

    gettable_fields = [
        "component",
        "reason",
        "severity",
        "type",
    ]
    """component,reason,severity,type,"""

    patchable_fields = [
        "component",
        "severity",
        "type",
    ]
    """component,severity,type,"""

    postable_fields = [
        "component",
        "severity",
        "type",
    ]
    """component,severity,type,"""


class StorageBridgeErrors(Resource):

    _schema = StorageBridgeErrorsSchema
