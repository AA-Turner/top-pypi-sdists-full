r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["TopMetricsClientResponsePartialResponseReason", "TopMetricsClientResponsePartialResponseReasonSchema"]
__pdoc__ = {
    "TopMetricsClientResponsePartialResponseReasonSchema.resource": False,
    "TopMetricsClientResponsePartialResponseReasonSchema.opts": False,
    "TopMetricsClientResponsePartialResponseReason": False,
}

class TopMetricsClientResponsePartialResponseReasonSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TopMetricsClientResponsePartialResponseReason object"""

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Warning code indicating why partial data was reported.

Example: 124518424 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" A message describing the reason for partial data.

Example: The top metrics report contains partial data for read operations because NFSv4 reads using Multi-Processor I/O (MPIO) are not tracked. """

    @property
    def resource(self):
        return TopMetricsClientResponsePartialResponseReason

    gettable_fields = [
        "code",
        "message",
    ]
    """code,message,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class TopMetricsClientResponsePartialResponseReason(Resource):

    _schema = TopMetricsClientResponsePartialResponseReasonSchema
