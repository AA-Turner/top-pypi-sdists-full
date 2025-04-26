r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["QuotaReportUsers", "QuotaReportUsersSchema"]
__pdoc__ = {
    "QuotaReportUsersSchema.resource": False,
    "QuotaReportUsersSchema.opts": False,
    "QuotaReportUsers": False,
}


class QuotaReportUsersSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the QuotaReportUsers object"""

    id = marshmallow_fields.Str(data_key="id", allow_none=True)
    r""" Quota target user ID """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Quota target user name """

    @property
    def resource(self):
        return QuotaReportUsers

    gettable_fields = [
        "id",
        "name",
    ]
    """id,name,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class QuotaReportUsers(Resource):

    _schema = QuotaReportUsersSchema
