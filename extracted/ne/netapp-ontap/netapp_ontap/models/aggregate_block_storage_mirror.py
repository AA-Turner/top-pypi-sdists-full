r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AggregateBlockStorageMirror", "AggregateBlockStorageMirrorSchema"]
__pdoc__ = {
    "AggregateBlockStorageMirrorSchema.resource": False,
    "AggregateBlockStorageMirrorSchema.opts": False,
    "AggregateBlockStorageMirror": False,
}


class AggregateBlockStorageMirrorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AggregateBlockStorageMirror object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Aggregate is SyncMirror protected

Example: false """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state field of the aggregate_block_storage_mirror.

Valid choices:

* unmirrored
* normal
* degraded
* resynchronizing
* failed """

    @property
    def resource(self):
        return AggregateBlockStorageMirror

    gettable_fields = [
        "enabled",
        "state",
    ]
    """enabled,state,"""

    patchable_fields = [
        "enabled",
    ]
    """enabled,"""

    postable_fields = [
        "enabled",
    ]
    """enabled,"""


class AggregateBlockStorageMirror(Resource):

    _schema = AggregateBlockStorageMirrorSchema
