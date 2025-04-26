r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ScheduleCluster", "ScheduleClusterSchema"]
__pdoc__ = {
    "ScheduleClusterSchema.resource": False,
    "ScheduleClusterSchema.opts": False,
    "ScheduleCluster": False,
}


class ScheduleClusterSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ScheduleCluster object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Cluster name

Example: cluster1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Cluster UUID

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return ScheduleCluster

    gettable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    patchable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class ScheduleCluster(Resource):

    _schema = ScheduleClusterSchema
