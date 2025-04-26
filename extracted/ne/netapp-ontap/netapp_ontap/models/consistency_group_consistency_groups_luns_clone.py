r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupConsistencyGroupsLunsClone", "ConsistencyGroupConsistencyGroupsLunsCloneSchema"]
__pdoc__ = {
    "ConsistencyGroupConsistencyGroupsLunsCloneSchema.resource": False,
    "ConsistencyGroupConsistencyGroupsLunsCloneSchema.opts": False,
    "ConsistencyGroupConsistencyGroupsLunsClone": False,
}


class ConsistencyGroupConsistencyGroupsLunsCloneSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupConsistencyGroupsLunsClone object"""

    source = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_consistency_groups_luns_clone_source.ConsistencyGroupConsistencyGroupsLunsCloneSourceSchema", unknown=EXCLUDE, data_key="source", allow_none=True)
    r""" The source LUN for a LUN clone operation. This can be specified using property `clone.source.uuid` or `clone.source.name`. If both properties are supplied, they must refer to the same LUN.<br/>
Valid in POST to create a new LUN as a clone of the source.<br/>
Valid in PATCH to overwrite an existing LUN's data as a clone of another. """

    @property
    def resource(self):
        return ConsistencyGroupConsistencyGroupsLunsClone

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
        "source",
    ]
    """source,"""

    postable_fields = [
        "source",
    ]
    """source,"""


class ConsistencyGroupConsistencyGroupsLunsClone(Resource):

    _schema = ConsistencyGroupConsistencyGroupsLunsCloneSchema
