r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["PerformanceReducedThroughput", "PerformanceReducedThroughputSchema"]
__pdoc__ = {
    "PerformanceReducedThroughputSchema.resource": False,
    "PerformanceReducedThroughputSchema.opts": False,
    "PerformanceReducedThroughput": False,
}


class PerformanceReducedThroughputSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the PerformanceReducedThroughput object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.collection_links.CollectionLinksSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the performance_reduced_throughput. """

    num_records = Size(data_key="num_records", allow_none=True)
    r""" Number of records

Example: 1 """

    records = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.performance_metric_reduced_throughput.PerformanceMetricReducedThroughputSchema", unknown=EXCLUDE, allow_none=True), data_key="records", allow_none=True)
    r""" Performance numbers, such as IOPS latency and throughput """

    @property
    def resource(self):
        return PerformanceReducedThroughput

    gettable_fields = [
        "links",
        "num_records",
        "records",
    ]
    """links,num_records,records,"""

    patchable_fields = [
        "num_records",
    ]
    """num_records,"""

    postable_fields = [
        "num_records",
    ]
    """num_records,"""


class PerformanceReducedThroughput(Resource):

    _schema = PerformanceReducedThroughputSchema
