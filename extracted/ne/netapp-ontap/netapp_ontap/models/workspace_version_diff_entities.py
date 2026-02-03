r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["WorkspaceVersionDiffEntities", "WorkspaceVersionDiffEntitiesSchema"]
__pdoc__ = {
    "WorkspaceVersionDiffEntitiesSchema.resource": False,
    "WorkspaceVersionDiffEntitiesSchema.opts": False,
    "WorkspaceVersionDiffEntities": False,
}

class WorkspaceVersionDiffEntitiesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WorkspaceVersionDiffEntities object"""

    entity_type = marshmallow_fields.Str(data_key="entity_type", allow_none=True)
    r""" The type of the entity.

Valid choices:

* file
* object """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the entity. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the entity.

Example: 123e4567-e89b-12d3-a456-426614174000 """

    @property
    def resource(self):
        return WorkspaceVersionDiffEntities

    gettable_fields = [
        "entity_type",
        "name",
        "uuid",
    ]
    """entity_type,name,uuid,"""

    patchable_fields = [
        "entity_type",
        "name",
        "uuid",
    ]
    """entity_type,name,uuid,"""

    postable_fields = [
        "entity_type",
        "name",
        "uuid",
    ]
    """entity_type,name,uuid,"""


class WorkspaceVersionDiffEntities(Resource):

    _schema = WorkspaceVersionDiffEntitiesSchema
