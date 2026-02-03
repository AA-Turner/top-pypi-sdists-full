r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["EntityWorkspaceVersion", "EntityWorkspaceVersionSchema"]
__pdoc__ = {
    "EntityWorkspaceVersionSchema.resource": False,
    "EntityWorkspaceVersionSchema.opts": False,
    "EntityWorkspaceVersion": False,
}

class EntityWorkspaceVersionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EntityWorkspaceVersion object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                unknown=EXCLUDE,
                data_key="_links",
                allow_none=True
            )
    r""" The links field of the entity_workspace_version. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the workspace.


Example: Doc workspace v1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the workspace.


Example: 02c9e252-41be-11e9-81d5-00a0986138f7 """

    version = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.entity_workspace_version_version", "EntityWorkspaceVersionVersionSchema"),
                unknown=EXCLUDE,
                data_key="version",
                allow_none=True
            )
    r""" The version information of a workspace. Defaults to the current version. """

    @property
    def resource(self):
        return EntityWorkspaceVersion

    gettable_fields = [
        "links",
        "name",
        "uuid",
        "version",
    ]
    """links,name,uuid,version,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class EntityWorkspaceVersion(Resource):

    _schema = EntityWorkspaceVersionSchema
