r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IgroupChild", "IgroupChildSchema"]
__pdoc__ = {
    "IgroupChildSchema.resource": False,
    "IgroupChildSchema.opts": False,
    "IgroupChild": False,
}


class IgroupChildSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IgroupChild object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the igroup_child. """

    comment = marshmallow_fields.Str(data_key="comment", allow_none=True)
    r""" A comment available for use by the administrator. """

    igroups = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.igroup_child.IgroupChildSchema", unknown=EXCLUDE, allow_none=True), data_key="igroups", allow_none=True)
    r""" Further nested initiator groups. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the initiator group.


Example: igroup1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the initiator group.


Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return IgroupChild

    gettable_fields = [
        "links",
        "comment",
        "igroups",
        "name",
        "uuid",
    ]
    """links,comment,igroups,name,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class IgroupChild(Resource):

    _schema = IgroupChildSchema
