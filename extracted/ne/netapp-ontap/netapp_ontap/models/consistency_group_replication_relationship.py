r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupReplicationRelationship", "ConsistencyGroupReplicationRelationshipSchema"]
__pdoc__ = {
    "ConsistencyGroupReplicationRelationshipSchema.resource": False,
    "ConsistencyGroupReplicationRelationshipSchema.opts": False,
    "ConsistencyGroupReplicationRelationship": False,
}


class ConsistencyGroupReplicationRelationshipSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupReplicationRelationship object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the consistency_group_replication_relationship. """

    is_source = marshmallow_fields.Boolean(data_key="is_source", allow_none=True)
    r""" Indicates whether or not this consistency group is the source for replication. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the SnapMirror relationship.


Example: 02c9e252-41be-11e9-81d5-00a0986138f7 """

    @property
    def resource(self):
        return ConsistencyGroupReplicationRelationship

    gettable_fields = [
        "links",
        "is_source",
        "uuid",
    ]
    """links,is_source,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ConsistencyGroupReplicationRelationship(Resource):

    _schema = ConsistencyGroupReplicationRelationshipSchema
