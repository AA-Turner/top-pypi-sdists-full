r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["WorkspaceVersionWorkspacePoliciesVersion", "WorkspaceVersionWorkspacePoliciesVersionSchema"]
__pdoc__ = {
    "WorkspaceVersionWorkspacePoliciesVersionSchema.resource": False,
    "WorkspaceVersionWorkspacePoliciesVersionSchema.opts": False,
    "WorkspaceVersionWorkspacePoliciesVersion": False,
}

class WorkspaceVersionWorkspacePoliciesVersionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WorkspaceVersionWorkspacePoliciesVersion object"""

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the version.

Example: 123e4567-e89b-12d3-a456-426614174000 """

    @property
    def resource(self):
        return WorkspaceVersionWorkspacePoliciesVersion

    gettable_fields = [
        "uuid",
    ]
    """uuid,"""

    patchable_fields = [
        "uuid",
    ]
    """uuid,"""

    postable_fields = [
        "uuid",
    ]
    """uuid,"""


class WorkspaceVersionWorkspacePoliciesVersion(Resource):

    _schema = WorkspaceVersionWorkspacePoliciesVersionSchema
