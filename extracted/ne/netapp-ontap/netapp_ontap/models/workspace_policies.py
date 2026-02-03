r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["WorkspacePolicies", "WorkspacePoliciesSchema"]
__pdoc__ = {
    "WorkspacePoliciesSchema.resource": False,
    "WorkspacePoliciesSchema.opts": False,
    "WorkspacePolicies": False,
}

class WorkspacePoliciesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WorkspacePolicies object"""

    attached_time = ImpreciseDateTime(data_key="attached_time", allow_none=True)
    r""" The time when the policy was attached to the workspace.

Example: 2018-06-04T19:00:00.000+0000 """

    description = marshmallow_fields.Str(data_key="description", allow_none=True)
    r""" The description field of the workspace_policies.

Example: Description of Policy """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name field of the workspace_policies.

Example: Example Policy """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the policy.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return WorkspacePolicies

    gettable_fields = [
        "attached_time",
        "description",
        "name",
        "uuid",
    ]
    """attached_time,description,name,uuid,"""

    patchable_fields = [
        "description",
        "name",
        "uuid",
    ]
    """description,name,uuid,"""

    postable_fields = [
        "description",
        "name",
        "uuid",
    ]
    """description,name,uuid,"""


class WorkspacePolicies(Resource):

    _schema = WorkspacePoliciesSchema
