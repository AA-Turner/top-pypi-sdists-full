r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["ConsistencyGroupConsistencyGroupsLunsClone", "ConsistencyGroupConsistencyGroupsLunsCloneSchema"]
__pdoc__ = {
    "ConsistencyGroupConsistencyGroupsLunsCloneSchema.resource": False,
    "ConsistencyGroupConsistencyGroupsLunsCloneSchema.opts": False,
    "ConsistencyGroupConsistencyGroupsLunsClone": False,
}

class ConsistencyGroupConsistencyGroupsLunsCloneSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupConsistencyGroupsLunsClone object"""

    created_as_clone = marshmallow_fields.Boolean(data_key="created_as_clone", allow_none=True)
    r""" This property is _true_ when the LUN was created as a clone of another LUN. Note that this property only indicates how the LUN was created and does not imply space savings by itself. If the clone and its source have diverged significantly since the clone was created, the original space saving behavior of a clone will have been lost.
This property is unset for LUNs that are not clones. """

    source = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.consistency_group_consistency_groups_luns_clone_source", "ConsistencyGroupConsistencyGroupsLunsCloneSourceSchema"),
                unknown=EXCLUDE,
                data_key="source",
                allow_none=True
            )
    r""" The source LUN for a LUN clone operation. This can be specified using property `clone.source.uuid` or `clone.source.name`. If both properties are supplied, they must refer to the same LUN.<br/>
Valid in POST to create a new LUN as a clone of the source.<br/>
Valid in PATCH to overwrite an existing LUN's data as a clone of another. """

    @property
    def resource(self):
        return ConsistencyGroupConsistencyGroupsLunsClone

    gettable_fields = [
        "created_as_clone",
    ]
    """created_as_clone,"""

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
