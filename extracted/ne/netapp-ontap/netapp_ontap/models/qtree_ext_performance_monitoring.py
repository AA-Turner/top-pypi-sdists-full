r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["QtreeExtPerformanceMonitoring", "QtreeExtPerformanceMonitoringSchema"]
__pdoc__ = {
    "QtreeExtPerformanceMonitoringSchema.resource": False,
    "QtreeExtPerformanceMonitoringSchema.opts": False,
    "QtreeExtPerformanceMonitoring": False,
}


class QtreeExtPerformanceMonitoringSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the QtreeExtPerformanceMonitoring object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Specifies whether extended performance monitoring is enabled for the qtree. """

    @property
    def resource(self):
        return QtreeExtPerformanceMonitoring

    gettable_fields = [
        "enabled",
    ]
    """enabled,"""

    patchable_fields = [
        "enabled",
    ]
    """enabled,"""

    postable_fields = [
        "enabled",
    ]
    """enabled,"""


class QtreeExtPerformanceMonitoring(Resource):

    _schema = QtreeExtPerformanceMonitoringSchema
