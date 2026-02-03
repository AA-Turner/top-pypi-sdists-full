r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["SwitchPortRemotePortDeviceDcn", "SwitchPortRemotePortDeviceDcnSchema"]
__pdoc__ = {
    "SwitchPortRemotePortDeviceDcnSchema.resource": False,
    "SwitchPortRemotePortDeviceDcnSchema.opts": False,
    "SwitchPortRemotePortDeviceDcn": False,
}

class SwitchPortRemotePortDeviceDcnSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SwitchPortRemotePortDeviceDcn object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                unknown=EXCLUDE,
                data_key="_links",
                allow_none=True
            )
    r""" The links field of the switch_port_remote_port_device_dcn. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Compute node name.

Example: node1 """

    serial_number = marshmallow_fields.Str(data_key="serial_number", allow_none=True)
    r""" Compute node serial number.

Example: 4048820-60-9 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Compute node UUID.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return SwitchPortRemotePortDeviceDcn

    gettable_fields = [
        "links",
        "name",
        "serial_number",
        "uuid",
    ]
    """links,name,serial_number,uuid,"""

    patchable_fields = [
        "name",
        "serial_number",
        "uuid",
    ]
    """name,serial_number,uuid,"""

    postable_fields = [
        "name",
        "serial_number",
        "uuid",
    ]
    """name,serial_number,uuid,"""


class SwitchPortRemotePortDeviceDcn(Resource):

    _schema = SwitchPortRemotePortDeviceDcnSchema
