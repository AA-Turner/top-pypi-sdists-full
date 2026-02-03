r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["WorkspaceVersionWorkspace", "WorkspaceVersionWorkspaceSchema"]
__pdoc__ = {
    "WorkspaceVersionWorkspaceSchema.resource": False,
    "WorkspaceVersionWorkspaceSchema.opts": False,
    "WorkspaceVersionWorkspace": False,
}

class WorkspaceVersionWorkspaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WorkspaceVersionWorkspace object"""

    create_time = ImpreciseDateTime(data_key="create_time", allow_none=True)
    r""" The creation time of the workspace version.

Example: 2018-06-04T19:00:00.000+0000 """

    data_collection_count = Size(data_key="data_collection_count", allow_none=True)
    r""" The count of data collection in a workspace.

Example: 20 """

    description = marshmallow_fields.Str(data_key="description", allow_none=True)
    r""" The description of the workspace.

Example: Example workspace """

    entity_count = Size(data_key="entity_count", allow_none=True)
    r""" The count of entities in a workspace.

Example: 1000 """

    errors = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_engine_entity_errors", "DataEngineEntityErrorsSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="errors",
                allow_none=True
                )
    r""" The errors field of the workspace_version_workspace. """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" The message associated with the current state of the workspace.

Example: creating workspace """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the workspace.

Example: Doc workspace """

    owner = marshmallow_fields.Str(data_key="owner", allow_none=True)
    r""" The owner of the workspace.

Example: SAL """

    policies = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.workspace_version_workspace_policies", "WorkspaceVersionWorkspacePoliciesSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="policies",
                allow_none=True
                )
    r""" The policies field of the workspace_version_workspace. """

    refresh_interval = marshmallow_fields.Str(data_key="refresh_interval", allow_none=True)
    r""" The workspace refresh time interval in ISO-8601 format.

Example: PT1H """

    space = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.workspace_version_workspace_space", "WorkspaceVersionWorkspaceSpaceSchema"),
                unknown=EXCLUDE,
                data_key="space",
                allow_none=True
            )
    r""" The space detail of a workspace. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" State of the workspace version:

* <i>processing</i> - The workspace is being processed after creation.
* <i>ready</i> - The workspace is ready for use.
* <i>failed</i> - The workspace has a failure.
* <i>outdated</i> - The workspace is outdated.
* Valid in GET.


Valid choices:

* processing
* ready
* failed
* outdated """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the workspace.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    version = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.workspace_version_workspace_version", "WorkspaceVersionWorkspaceVersionSchema"),
                unknown=EXCLUDE,
                data_key="version",
                allow_none=True
            )
    r""" The version information of a workspace. """

    @property
    def resource(self):
        return WorkspaceVersionWorkspace

    gettable_fields = [
        "create_time",
        "data_collection_count",
        "description",
        "entity_count",
        "errors",
        "message",
        "name",
        "owner",
        "policies",
        "refresh_interval",
        "space",
        "state",
        "uuid",
        "version",
    ]
    """create_time,data_collection_count,description,entity_count,errors,message,name,owner,policies,refresh_interval,space,state,uuid,version,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class WorkspaceVersionWorkspace(Resource):

    _schema = WorkspaceVersionWorkspaceSchema
