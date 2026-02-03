r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["WorkspaceMetrics", "WorkspaceMetricsSchema"]
__pdoc__ = {
    "WorkspaceMetricsSchema.resource": False,
    "WorkspaceMetricsSchema.opts": False,
    "WorkspaceMetrics": False,
}

class WorkspaceMetricsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WorkspaceMetrics object"""

    counts_by_state = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.workspace_metrics_counts_by_state", "WorkspaceMetricsCountsByStateSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="counts_by_state",
                allow_none=True
                )
    r""" The number of workspaces per state. """

    metadata_size = Size(data_key="metadata_size", allow_none=True)
    r""" The total size of all metadata, in bytes.

Example: 121314 """

    space_percent = Size(data_key="space_percent", allow_none=True)
    r""" The percentage of the total cluster size occupied by the workspaces.

Example: 25 """

    total_count = Size(data_key="total_count", allow_none=True)
    r""" The total number of workspaces.

Example: 100 """

    total_size = Size(data_key="total_size", allow_none=True)
    r""" The total size of all workspaces, in bytes.

Example: 121314 """

    vector_size = Size(data_key="vector_size", allow_none=True)
    r""" The total size of all vector database, in bytes.

Example: 121314 """

    @property
    def resource(self):
        return WorkspaceMetrics

    gettable_fields = [
        "counts_by_state",
        "metadata_size",
        "space_percent",
        "total_count",
        "total_size",
        "vector_size",
    ]
    """counts_by_state,metadata_size,space_percent,total_count,total_size,vector_size,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class WorkspaceMetrics(Resource):

    _schema = WorkspaceMetricsSchema
