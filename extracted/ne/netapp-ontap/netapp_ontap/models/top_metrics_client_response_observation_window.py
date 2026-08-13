r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["TopMetricsClientResponseObservationWindow", "TopMetricsClientResponseObservationWindowSchema"]
__pdoc__ = {
    "TopMetricsClientResponseObservationWindowSchema.resource": False,
    "TopMetricsClientResponseObservationWindowSchema.opts": False,
    "TopMetricsClientResponseObservationWindow": False,
}

class TopMetricsClientResponseObservationWindowSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TopMetricsClientResponseObservationWindow object"""

    duration = Size(data_key="duration", allow_none=True)
    r""" Duration of the observation window in seconds.

Example: 60 """

    end = marshmallow_fields.Str(data_key="end", allow_none=True)
    r""" End timestamp of the observation window in UTC.

Example: 2026-01-11T01:30:00.000+0000 """

    start = marshmallow_fields.Str(data_key="start", allow_none=True)
    r""" Start timestamp of the observation window in UTC.

Example: 2026-01-11T01:29:55.000+0000 """

    @property
    def resource(self):
        return TopMetricsClientResponseObservationWindow

    gettable_fields = [
        "duration",
        "end",
        "start",
    ]
    """duration,end,start,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class TopMetricsClientResponseObservationWindow(Resource):

    _schema = TopMetricsClientResponseObservationWindowSchema
