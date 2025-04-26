r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IscsiConnectionInterface", "IscsiConnectionInterfaceSchema"]
__pdoc__ = {
    "IscsiConnectionInterfaceSchema.resource": False,
    "IscsiConnectionInterfaceSchema.opts": False,
    "IscsiConnectionInterface": False,
}


class IscsiConnectionInterfaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IscsiConnectionInterface object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the iscsi_connection_interface. """

    ip = marshmallow_fields.Nested("netapp_ontap.models.iscsi_connection_interface_ip.IscsiConnectionInterfaceIpSchema", unknown=EXCLUDE, data_key="ip", allow_none=True)
    r""" The IP information. ONTAP only supports port 3260. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the interface.

Example: lif1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The UUID that uniquely identifies the interface.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return IscsiConnectionInterface

    gettable_fields = [
        "links",
        "ip",
        "name",
        "uuid",
    ]
    """links,ip,name,uuid,"""

    patchable_fields = [
        "ip",
    ]
    """ip,"""

    postable_fields = [
        "ip",
    ]
    """ip,"""


class IscsiConnectionInterface(Resource):

    _schema = IscsiConnectionInterfaceSchema
