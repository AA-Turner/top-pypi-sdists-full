r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataCollectionMetrics", "DataCollectionMetricsSchema"]
__pdoc__ = {
    "DataCollectionMetricsSchema.resource": False,
    "DataCollectionMetricsSchema.opts": False,
    "DataCollectionMetrics": False,
}

class DataCollectionMetricsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataCollectionMetrics object"""

    counts_by_state = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_collection_metrics_counts_by_state", "DataCollectionMetricsCountsByStateSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="counts_by_state",
                allow_none=True
                )
    r""" The number of data collections per state. """

    space_percent = Size(data_key="space_percent", allow_none=True)
    r""" The percentage of the total cluster size occupied by the data collections.

Example: 25 """

    total_count = Size(data_key="total_count", allow_none=True)
    r""" The total number of data collections.

Example: 100 """

    total_size = Size(data_key="total_size", allow_none=True)
    r""" The total size of all data collections, in bytes.

Example: 121314 """

    @property
    def resource(self):
        return DataCollectionMetrics

    gettable_fields = [
        "counts_by_state",
        "space_percent",
        "total_count",
        "total_size",
    ]
    """counts_by_state,space_percent,total_count,total_size,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DataCollectionMetrics(Resource):

    _schema = DataCollectionMetricsSchema
