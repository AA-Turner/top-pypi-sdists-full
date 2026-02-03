r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["RecentWorkspacesInner", "RecentWorkspacesInnerSchema"]
__pdoc__ = {
    "RecentWorkspacesInnerSchema.resource": False,
    "RecentWorkspacesInnerSchema.opts": False,
    "RecentWorkspacesInner": False,
}

class RecentWorkspacesInnerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the RecentWorkspacesInner object"""

    data_collection_count = Size(data_key="data_collection_count", allow_none=True)
    r""" Number of data collections in the workspace.

Example: 3 """

    entity_count = Size(data_key="entity_count", allow_none=True)
    r""" Number of entities in the workspace.

Example: 1000 """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the workspace.

Example: Finance """

    scanned_size = Size(data_key="scanned_size", allow_none=True)
    r""" Scanned size of the workspace.

Example: 7663353 """

    sensitive_entity_count = Size(data_key="sensitive_entity_count", allow_none=True)
    r""" Number of sensitive entities in the workspace.

Example: 10 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" UUID of the workspace.

Example: 02c9e252-41be-11e9-81d5-00a0986138f7 """

    @property
    def resource(self):
        return RecentWorkspacesInner

    gettable_fields = [
        "data_collection_count",
        "entity_count",
        "name",
        "scanned_size",
        "sensitive_entity_count",
        "uuid",
    ]
    """data_collection_count,entity_count,name,scanned_size,sensitive_entity_count,uuid,"""

    patchable_fields = [
        "data_collection_count",
        "entity_count",
        "name",
        "scanned_size",
        "sensitive_entity_count",
        "uuid",
    ]
    """data_collection_count,entity_count,name,scanned_size,sensitive_entity_count,uuid,"""

    postable_fields = [
        "data_collection_count",
        "entity_count",
        "name",
        "scanned_size",
        "sensitive_entity_count",
        "uuid",
    ]
    """data_collection_count,entity_count,name,scanned_size,sensitive_entity_count,uuid,"""


class RecentWorkspacesInner(Resource):

    _schema = RecentWorkspacesInnerSchema
