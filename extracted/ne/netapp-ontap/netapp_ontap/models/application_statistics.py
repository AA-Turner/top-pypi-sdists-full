r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationStatistics", "ApplicationStatisticsSchema"]
__pdoc__ = {
    "ApplicationStatisticsSchema.resource": False,
    "ApplicationStatisticsSchema.opts": False,
    "ApplicationStatistics": False,
}


class ApplicationStatisticsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationStatistics object"""

    components = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.application_statistics_components.ApplicationStatisticsComponentsSchema", unknown=EXCLUDE, allow_none=True), data_key="components", allow_none=True)
    r""" The components field of the application_statistics. """

    iops = marshmallow_fields.Nested("netapp_ontap.models.application_statistics_iops.ApplicationStatisticsIopsSchema", unknown=EXCLUDE, data_key="iops", allow_none=True)
    r""" The iops field of the application_statistics. """

    latency = marshmallow_fields.Nested("netapp_ontap.models.application_statistics_latency.ApplicationStatisticsLatencySchema", unknown=EXCLUDE, data_key="latency", allow_none=True)
    r""" The latency field of the application_statistics. """

    shared_storage_pool = marshmallow_fields.Boolean(data_key="shared_storage_pool", allow_none=True)
    r""" An application is considered to use a shared storage pool if storage elements for multiple components reside on the same aggregate. """

    snapshot = marshmallow_fields.Nested("netapp_ontap.models.application_statistics_components_snapshot.ApplicationStatisticsComponentsSnapshotSchema", unknown=EXCLUDE, data_key="snapshot", allow_none=True)
    r""" The snapshot field of the application_statistics. """

    space = marshmallow_fields.Nested("netapp_ontap.models.application_statistics_space.ApplicationStatisticsSpaceSchema", unknown=EXCLUDE, data_key="space", allow_none=True)
    r""" The space field of the application_statistics. """

    statistics_incomplete = marshmallow_fields.Boolean(data_key="statistics_incomplete", allow_none=True)
    r""" If not all storage elements of the application are currently available, the returned statistics might only include data from those elements that were available. """

    @property
    def resource(self):
        return ApplicationStatistics

    gettable_fields = [
        "components",
        "iops",
        "latency",
        "shared_storage_pool",
        "snapshot",
        "space",
        "statistics_incomplete",
    ]
    """components,iops,latency,shared_storage_pool,snapshot,space,statistics_incomplete,"""

    patchable_fields = [
        "iops",
        "latency",
        "snapshot",
        "space",
    ]
    """iops,latency,snapshot,space,"""

    postable_fields = [
        "iops",
        "latency",
        "snapshot",
        "space",
    ]
    """iops,latency,snapshot,space,"""


class ApplicationStatistics(Resource):

    _schema = ApplicationStatisticsSchema
