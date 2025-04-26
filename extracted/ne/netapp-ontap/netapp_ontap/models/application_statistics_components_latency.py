r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationStatisticsComponentsLatency", "ApplicationStatisticsComponentsLatencySchema"]
__pdoc__ = {
    "ApplicationStatisticsComponentsLatencySchema.resource": False,
    "ApplicationStatisticsComponentsLatencySchema.opts": False,
    "ApplicationStatisticsComponentsLatency": False,
}


class ApplicationStatisticsComponentsLatencySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationStatisticsComponentsLatency object"""

    average = Size(data_key="average", allow_none=True)
    r""" The cumulative average response time in microseconds for this component. """

    raw = Size(data_key="raw", allow_none=True)
    r""" The cumulative response time in microseconds for this component. """

    @property
    def resource(self):
        return ApplicationStatisticsComponentsLatency

    gettable_fields = [
        "average",
        "raw",
    ]
    """average,raw,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ApplicationStatisticsComponentsLatency(Resource):

    _schema = ApplicationStatisticsComponentsLatencySchema
