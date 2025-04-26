r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["PerformanceSvm", "PerformanceSvmSchema"]
__pdoc__ = {
    "PerformanceSvmSchema.resource": False,
    "PerformanceSvmSchema.opts": False,
    "PerformanceSvm": False,
}


class PerformanceSvmSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the PerformanceSvm object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.collection_links.CollectionLinksSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the performance_svm. """

    num_records = Size(data_key="num_records", allow_none=True)
    r""" Number of records

Example: 1 """

    records = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.performance_metric_svm.PerformanceMetricSvmSchema", unknown=EXCLUDE, allow_none=True), data_key="records", allow_none=True)
    r""" The records field of the performance_svm. """

    @property
    def resource(self):
        return PerformanceSvm

    gettable_fields = [
        "links",
        "num_records",
        "records.links",
        "records.duration",
        "records.iops",
        "records.latency",
        "records.status",
        "records.throughput",
        "records.timestamp",
    ]
    """links,num_records,records.links,records.duration,records.iops,records.latency,records.status,records.throughput,records.timestamp,"""

    patchable_fields = [
        "num_records",
        "records.iops",
        "records.latency",
        "records.throughput",
    ]
    """num_records,records.iops,records.latency,records.throughput,"""

    postable_fields = [
        "num_records",
        "records.iops",
        "records.latency",
        "records.throughput",
    ]
    """num_records,records.iops,records.latency,records.throughput,"""


class PerformanceSvm(Resource):

    _schema = PerformanceSvmSchema
