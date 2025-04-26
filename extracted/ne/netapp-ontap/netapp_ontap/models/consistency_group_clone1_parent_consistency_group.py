r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupClone1ParentConsistencyGroup", "ConsistencyGroupClone1ParentConsistencyGroupSchema"]
__pdoc__ = {
    "ConsistencyGroupClone1ParentConsistencyGroupSchema.resource": False,
    "ConsistencyGroupClone1ParentConsistencyGroupSchema.opts": False,
    "ConsistencyGroupClone1ParentConsistencyGroup": False,
}


class ConsistencyGroupClone1ParentConsistencyGroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupClone1ParentConsistencyGroup object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the consistency_group_clone1_parent_consistency_group. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the consistency group. """

    parent_name = marshmallow_fields.Str(data_key="parent_name", allow_none=True)
    r""" The name of the parent consistency group used when cloning a child consistency group. """

    parent_uuid = marshmallow_fields.Str(data_key="parent_uuid", allow_none=True)
    r""" The unique identifier of the parent consistency group used when cloning a child consistency group. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the consistency group. """

    @property
    def resource(self):
        return ConsistencyGroupClone1ParentConsistencyGroup

    gettable_fields = [
        "links",
        "name",
        "parent_name",
        "parent_uuid",
        "uuid",
    ]
    """links,name,parent_name,parent_uuid,uuid,"""

    patchable_fields = [
        "parent_name",
        "parent_uuid",
    ]
    """parent_name,parent_uuid,"""

    postable_fields = [
        "name",
        "parent_name",
        "parent_uuid",
        "uuid",
    ]
    """name,parent_name,parent_uuid,uuid,"""


class ConsistencyGroupClone1ParentConsistencyGroup(Resource):

    _schema = ConsistencyGroupClone1ParentConsistencyGroupSchema
