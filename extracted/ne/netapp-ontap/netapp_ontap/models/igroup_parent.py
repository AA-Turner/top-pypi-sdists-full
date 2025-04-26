r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IgroupParent", "IgroupParentSchema"]
__pdoc__ = {
    "IgroupParentSchema.resource": False,
    "IgroupParentSchema.opts": False,
    "IgroupParent": False,
}


class IgroupParentSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IgroupParent object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the igroup_parent. """

    comment = marshmallow_fields.Str(data_key="comment", allow_none=True)
    r""" A comment available for use by the administrator. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the initiator group.


Example: igroup1 """

    parent_igroups = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.igroup_parent.IgroupParentSchema", unknown=EXCLUDE, allow_none=True), data_key="parent_igroups", allow_none=True)
    r""" The initiator groups that contain this initiator group as a member. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the initiator group.


Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return IgroupParent

    gettable_fields = [
        "links",
        "comment",
        "name",
        "parent_igroups",
        "uuid",
    ]
    """links,comment,name,parent_igroups,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class IgroupParent(Resource):

    _schema = IgroupParentSchema
