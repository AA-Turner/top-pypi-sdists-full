r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeConstituentsMovement", "VolumeConstituentsMovementSchema"]
__pdoc__ = {
    "VolumeConstituentsMovementSchema.resource": False,
    "VolumeConstituentsMovementSchema.opts": False,
    "VolumeConstituentsMovement": False,
}


class VolumeConstituentsMovementSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeConstituentsMovement object"""

    cutover_window = Size(data_key="cutover_window", allow_none=True)
    r""" Time window in seconds for cutover. The allowed range is between 30 to 300 seconds.

Example: 30 """

    destination_aggregate = marshmallow_fields.Nested("netapp_ontap.resources.aggregate.AggregateSchema", unknown=EXCLUDE, data_key="destination_aggregate", allow_none=True)
    r""" The destination_aggregate field of the volume_constituents_movement. """

    percent_complete = Size(data_key="percent_complete", allow_none=True)
    r""" Completion percentage """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" State of volume move operation. PATCH the state to "aborted" to abort the move operation. PATCH the state to "cutover" to trigger cutover. PATCH the state to "paused" to pause the volume move operation in progress. PATCH the state to "replicating" to resume the paused volume move operation. PATCH the state to "cutover_wait" to go into cutover manually. When volume move operation is waiting to go into "cutover" state, this is indicated by the "cutover_pending" state. A change of state is only supported if volume movement is in progress.

Valid choices:

* aborted
* cutover
* cutover_wait
* cutover_pending
* failed
* paused
* queued
* replicating
* success """

    tiering_policy = marshmallow_fields.Str(data_key="tiering_policy", allow_none=True)
    r""" Tiering policy for FabricPool

Valid choices:

* all
* auto
* backup
* none
* snapshot_only """

    @property
    def resource(self):
        return VolumeConstituentsMovement

    gettable_fields = [
        "cutover_window",
        "destination_aggregate.links",
        "destination_aggregate.name",
        "destination_aggregate.uuid",
        "percent_complete",
        "state",
    ]
    """cutover_window,destination_aggregate.links,destination_aggregate.name,destination_aggregate.uuid,percent_complete,state,"""

    patchable_fields = [
        "cutover_window",
        "destination_aggregate.name",
        "destination_aggregate.uuid",
        "state",
        "tiering_policy",
    ]
    """cutover_window,destination_aggregate.name,destination_aggregate.uuid,state,tiering_policy,"""

    postable_fields = [
        "cutover_window",
        "destination_aggregate.name",
        "destination_aggregate.uuid",
        "state",
    ]
    """cutover_window,destination_aggregate.name,destination_aggregate.uuid,state,"""


class VolumeConstituentsMovement(Resource):

    _schema = VolumeConstituentsMovementSchema
