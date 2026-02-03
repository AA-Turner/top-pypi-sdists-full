r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["WorkspaceVersionWorkspacePolicies", "WorkspaceVersionWorkspacePoliciesSchema"]
__pdoc__ = {
    "WorkspaceVersionWorkspacePoliciesSchema.resource": False,
    "WorkspaceVersionWorkspacePoliciesSchema.opts": False,
    "WorkspaceVersionWorkspacePolicies": False,
}

class WorkspaceVersionWorkspacePoliciesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WorkspaceVersionWorkspacePolicies object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name field of the workspace_version_workspace_policies.

Example: Example Policy """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the policy.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    version = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.workspace_version_workspace_policies_version", "WorkspaceVersionWorkspacePoliciesVersionSchema"),
                unknown=EXCLUDE,
                data_key="version",
                allow_none=True
            )
    r""" The version information of a policy. """

    @property
    def resource(self):
        return WorkspaceVersionWorkspacePolicies

    gettable_fields = [
        "name",
        "uuid",
        "version",
    ]
    """name,uuid,version,"""

    patchable_fields = [
        "name",
        "uuid",
        "version",
    ]
    """name,uuid,version,"""

    postable_fields = [
        "name",
        "uuid",
        "version",
    ]
    """name,uuid,version,"""


class WorkspaceVersionWorkspacePolicies(Resource):

    _schema = WorkspaceVersionWorkspacePoliciesSchema
