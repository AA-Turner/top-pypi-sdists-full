r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["WorkspaceDataSources", "WorkspaceDataSourcesSchema"]
__pdoc__ = {
    "WorkspaceDataSourcesSchema.resource": False,
    "WorkspaceDataSourcesSchema.opts": False,
    "WorkspaceDataSources": False,
}

class WorkspaceDataSourcesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WorkspaceDataSources object"""

    data_source = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.common_data_source", "CommonDataSourceSchema"),
                unknown=EXCLUDE,
                data_key="data_source",
                allow_none=True
            )
    r""" Data source information. Required in a POST request. """

    @property
    def resource(self):
        return WorkspaceDataSources

    gettable_fields = [
        "data_source",
    ]
    """data_source,"""

    patchable_fields = [
        "data_source",
    ]
    """data_source,"""

    postable_fields = [
        "data_source",
    ]
    """data_source,"""


class WorkspaceDataSources(Resource):

    _schema = WorkspaceDataSourcesSchema
