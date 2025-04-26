r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SnapmirrorConsistencyGroupFailover", "SnapmirrorConsistencyGroupFailoverSchema"]
__pdoc__ = {
    "SnapmirrorConsistencyGroupFailoverSchema.resource": False,
    "SnapmirrorConsistencyGroupFailoverSchema.opts": False,
    "SnapmirrorConsistencyGroupFailover": False,
}


class SnapmirrorConsistencyGroupFailoverSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnapmirrorConsistencyGroupFailover object"""

    error = marshmallow_fields.Nested("netapp_ontap.models.error.ErrorSchema", unknown=EXCLUDE, data_key="error", allow_none=True)
    r""" The error field of the snapmirror_consistency_group_failover. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" SnapMirror Consistency Group failover state.

Valid choices:

* started
* failed
* completed
* completed_with_warnings
* vetoed """

    status = marshmallow_fields.Nested("netapp_ontap.models.snapmirror_consistency_group_failover_status.SnapmirrorConsistencyGroupFailoverStatusSchema", unknown=EXCLUDE, data_key="status", allow_none=True)
    r""" The status field of the snapmirror_consistency_group_failover. """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" SnapMirror Consistency Group failover type.

Valid choices:

* planned
* unplanned
* incapable """

    @property
    def resource(self):
        return SnapmirrorConsistencyGroupFailover

    gettable_fields = [
        "error",
        "state",
        "status",
        "type",
    ]
    """error,state,status,type,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class SnapmirrorConsistencyGroupFailover(Resource):

    _schema = SnapmirrorConsistencyGroupFailoverSchema
