r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageUnitMovement", "StorageUnitMovementSchema"]
__pdoc__ = {
    "StorageUnitMovementSchema.resource": False,
    "StorageUnitMovementSchema.opts": False,
    "StorageUnitMovement": False,
}


class StorageUnitMovementSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageUnitMovement object"""

    destination = marshmallow_fields.Nested("netapp_ontap.models.storage_unit_movement_destination.StorageUnitMovementDestinationSchema", unknown=EXCLUDE, data_key="destination", allow_none=True)
    r""" The destination of a storage unit move. """

    percent_complete = Size(data_key="percent_complete", allow_none=True)
    r""" The percentage complete of the move. """

    source = marshmallow_fields.Nested("netapp_ontap.models.storage_unit_movement_source.StorageUnitMovementSourceSchema", unknown=EXCLUDE, data_key="source", allow_none=True)
    r""" The source of a storage unit move. """

    start_time = ImpreciseDateTime(data_key="start_time", allow_none=True)
    r""" The start date and time of the storage unit move.


Example: 2024-12-07T08:45:12.000+0000 """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state of the storage unit move operation. Update the state to `aborted` to cancel the move operation. Update the state to `cutover` to trigger cutover. Update the state to `paused` to pause the storage unit move operation in progress. Update the state to `replicating` to resume the paused storage unit move operation. Update the state to `cutover_wait` to go into cutover manually. When the storage unit move operation is waiting to go into the `cutover` state, the operation state is `cutover_pending`. A change of state is only supported if a storage unit move operation is in progress.


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

    @property
    def resource(self):
        return StorageUnitMovement

    gettable_fields = [
        "destination",
        "percent_complete",
        "source",
        "start_time",
        "state",
    ]
    """destination,percent_complete,source,start_time,state,"""

    patchable_fields = [
        "state",
    ]
    """state,"""

    postable_fields = [
    ]
    """"""


class StorageUnitMovement(Resource):

    _schema = StorageUnitMovementSchema
