r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IgroupLunMapsLun", "IgroupLunMapsLunSchema"]
__pdoc__ = {
    "IgroupLunMapsLunSchema.resource": False,
    "IgroupLunMapsLunSchema.opts": False,
    "IgroupLunMapsLun": False,
}


class IgroupLunMapsLunSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IgroupLunMapsLun object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the igroup_lun_maps_lun. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the LUN.


Example: lun1 """

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the igroup_lun_maps_lun. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the LUN.


Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return IgroupLunMapsLun

    gettable_fields = [
        "links",
        "name",
        "node.links",
        "node.name",
        "node.uuid",
        "uuid",
    ]
    """links,name,node.links,node.name,node.uuid,uuid,"""

    patchable_fields = [
        "node.name",
        "node.uuid",
    ]
    """node.name,node.uuid,"""

    postable_fields = [
        "node.name",
        "node.uuid",
    ]
    """node.name,node.uuid,"""


class IgroupLunMapsLun(Resource):

    _schema = IgroupLunMapsLunSchema
