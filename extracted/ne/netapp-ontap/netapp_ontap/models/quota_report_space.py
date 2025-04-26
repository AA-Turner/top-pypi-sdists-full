r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["QuotaReportSpace", "QuotaReportSpaceSchema"]
__pdoc__ = {
    "QuotaReportSpaceSchema.resource": False,
    "QuotaReportSpaceSchema.opts": False,
    "QuotaReportSpace": False,
}


class QuotaReportSpaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the QuotaReportSpace object"""

    hard_limit = Size(data_key="hard_limit", allow_none=True)
    r""" Space hard limit in bytes """

    soft_limit = Size(data_key="soft_limit", allow_none=True)
    r""" Space soft limit in bytes """

    used = marshmallow_fields.Nested("netapp_ontap.models.quota_report_space_used.QuotaReportSpaceUsedSchema", unknown=EXCLUDE, data_key="used", allow_none=True)
    r""" The used field of the quota_report_space. """

    @property
    def resource(self):
        return QuotaReportSpace

    gettable_fields = [
        "hard_limit",
        "soft_limit",
        "used",
    ]
    """hard_limit,soft_limit,used,"""

    patchable_fields = [
        "used",
    ]
    """used,"""

    postable_fields = [
        "used",
    ]
    """used,"""


class QuotaReportSpace(Resource):

    _schema = QuotaReportSpaceSchema
