r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["PerformanceSvmNfsMetricHistorical", "PerformanceSvmNfsMetricHistoricalSchema"]
__pdoc__ = {
    "PerformanceSvmNfsMetricHistoricalSchema.resource": False,
    "PerformanceSvmNfsMetricHistoricalSchema.opts": False,
    "PerformanceSvmNfsMetricHistorical": False,
}


class PerformanceSvmNfsMetricHistoricalSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the PerformanceSvmNfsMetricHistorical object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the performance_svm_nfs_metric_historical. """

    timestamp = ImpreciseDateTime(data_key="timestamp", allow_none=True)
    r""" The timestamp of the performance data.

Example: 2017-01-25T11:20:13.000+0000 """

    v3 = marshmallow_fields.Nested("netapp_ontap.models.performance_svm_nfs_metric_historical_v3.PerformanceSvmNfsMetricHistoricalV3Schema", unknown=EXCLUDE, data_key="v3", allow_none=True)
    r""" The NFSv3 operations """

    v4 = marshmallow_fields.Nested("netapp_ontap.models.performance_svm_nfs_metric_historical_v4.PerformanceSvmNfsMetricHistoricalV4Schema", unknown=EXCLUDE, data_key="v4", allow_none=True)
    r""" The NFSv4 operations """

    v41 = marshmallow_fields.Nested("netapp_ontap.models.performance_svm_nfs_metric_historical_v41.PerformanceSvmNfsMetricHistoricalV41Schema", unknown=EXCLUDE, data_key="v41", allow_none=True)
    r""" The NFSv4.1 operations """

    @property
    def resource(self):
        return PerformanceSvmNfsMetricHistorical

    gettable_fields = [
        "links",
        "timestamp",
        "v3",
        "v4",
        "v41",
    ]
    """links,timestamp,v3,v4,v41,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class PerformanceSvmNfsMetricHistorical(Resource):

    _schema = PerformanceSvmNfsMetricHistoricalSchema
