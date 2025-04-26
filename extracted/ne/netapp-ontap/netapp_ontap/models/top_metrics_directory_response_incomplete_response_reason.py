r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["TopMetricsDirectoryResponseIncompleteResponseReason", "TopMetricsDirectoryResponseIncompleteResponseReasonSchema"]
__pdoc__ = {
    "TopMetricsDirectoryResponseIncompleteResponseReasonSchema.resource": False,
    "TopMetricsDirectoryResponseIncompleteResponseReasonSchema.opts": False,
    "TopMetricsDirectoryResponseIncompleteResponseReason": False,
}


class TopMetricsDirectoryResponseIncompleteResponseReasonSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TopMetricsDirectoryResponseIncompleteResponseReason object"""

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Warning code indicating why partial data was reported.

Example: 111411207 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" A message describing the reason for partial data.

Example: Partial data has been returned for this metric report. Reason: Data collection for the large directory report is in progress. """

    @property
    def resource(self):
        return TopMetricsDirectoryResponseIncompleteResponseReason

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


class TopMetricsDirectoryResponseIncompleteResponseReason(Resource):

    _schema = TopMetricsDirectoryResponseIncompleteResponseReasonSchema
