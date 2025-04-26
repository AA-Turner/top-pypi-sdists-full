r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["TopMetricsClientResponseNotice", "TopMetricsClientResponseNoticeSchema"]
__pdoc__ = {
    "TopMetricsClientResponseNoticeSchema.resource": False,
    "TopMetricsClientResponseNoticeSchema.opts": False,
    "TopMetricsClientResponseNotice": False,
}


class TopMetricsClientResponseNoticeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TopMetricsClientResponseNotice object"""

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Warning code indicating why no records are returned.

Example: 111411207 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Details why no records are returned.

Example: No read/write traffic on volume """

    @property
    def resource(self):
        return TopMetricsClientResponseNotice

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


class TopMetricsClientResponseNotice(Resource):

    _schema = TopMetricsClientResponseNoticeSchema
