r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageSwitchZones", "StorageSwitchZonesSchema"]
__pdoc__ = {
    "StorageSwitchZonesSchema.resource": False,
    "StorageSwitchZonesSchema.opts": False,
    "StorageSwitchZones": False,
}


class StorageSwitchZonesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageSwitchZones object"""

    id = Size(data_key="id", allow_none=True)
    r""" Storage switch zone ID """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Storage switch zone name """

    port = marshmallow_fields.Nested("netapp_ontap.models.storage_switch_zones_port.StorageSwitchZonesPortSchema", unknown=EXCLUDE, data_key="port", allow_none=True)
    r""" The port field of the storage_switch_zones. """

    wwn = marshmallow_fields.Str(data_key="wwn", allow_none=True)
    r""" Storage switch zone world wide name """

    @property
    def resource(self):
        return StorageSwitchZones

    gettable_fields = [
        "id",
        "name",
        "port",
        "wwn",
    ]
    """id,name,port,wwn,"""

    patchable_fields = [
        "id",
        "name",
        "port",
        "wwn",
    ]
    """id,name,port,wwn,"""

    postable_fields = [
        "id",
        "name",
        "port",
        "wwn",
    ]
    """id,name,port,wwn,"""


class StorageSwitchZones(Resource):

    _schema = StorageSwitchZonesSchema
