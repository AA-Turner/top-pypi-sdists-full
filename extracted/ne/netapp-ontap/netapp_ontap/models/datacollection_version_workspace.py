r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DatacollectionVersionWorkspace", "DatacollectionVersionWorkspaceSchema"]
__pdoc__ = {
    "DatacollectionVersionWorkspaceSchema.resource": False,
    "DatacollectionVersionWorkspaceSchema.opts": False,
    "DatacollectionVersionWorkspace": False,
}

class DatacollectionVersionWorkspaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DatacollectionVersionWorkspace object"""

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Unique identifier of the workspace.

Example: 123e4567-e89b-12d3-a456-426614174000 """

    @property
    def resource(self):
        return DatacollectionVersionWorkspace

    gettable_fields = [
        "uuid",
    ]
    """uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DatacollectionVersionWorkspace(Resource):

    _schema = DatacollectionVersionWorkspaceSchema
