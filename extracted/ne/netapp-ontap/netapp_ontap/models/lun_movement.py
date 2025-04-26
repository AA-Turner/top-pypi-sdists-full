r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LunMovement", "LunMovementSchema"]
__pdoc__ = {
    "LunMovementSchema.resource": False,
    "LunMovementSchema.opts": False,
    "LunMovement": False,
}


class LunMovementSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LunMovement object"""

    max_throughput = Size(data_key="max_throughput", allow_none=True)
    r""" The maximum data throughput, in bytes per second, that should be utilized in support of the LUN movement. This property can be used to throttle a transfer and limit its impact on the performance of the source and destination nodes. The specified value will be rounded up to the nearest megabyte.<br/>
If this property is not specified in a POST that begins a LUN movement, throttling is not applied to the data transfer.<br/>
For more information, see _Size properties_ in the _docs_ section of the ONTAP REST API documentation.<br/>
This property is valid only in a POST that begins a LUN movement or a PATCH when a LUN movement is already in process. """

    paths = marshmallow_fields.Nested("netapp_ontap.models.lun_movement_paths.LunMovementPathsSchema", unknown=EXCLUDE, data_key="paths", allow_none=True)
    r""" The fully qualified LUN path names involved in the LUN movement. """

    progress = marshmallow_fields.Nested("netapp_ontap.models.lun_movement_progress.LunMovementProgressSchema", unknown=EXCLUDE, data_key="progress", allow_none=True)
    r""" Properties related to the progress of an active or recently completed LUN movement. """

    @property
    def resource(self):
        return LunMovement

    gettable_fields = [
        "max_throughput",
        "paths",
        "progress",
    ]
    """max_throughput,paths,progress,"""

    patchable_fields = [
        "max_throughput",
        "progress",
    ]
    """max_throughput,progress,"""

    postable_fields = [
        "max_throughput",
    ]
    """max_throughput,"""


class LunMovement(Resource):

    _schema = LunMovementSchema
