r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["WorkspaceSpace", "WorkspaceSpaceSchema"]
__pdoc__ = {
    "WorkspaceSpaceSchema.resource": False,
    "WorkspaceSpaceSchema.opts": False,
    "WorkspaceSpace": False,
}

class WorkspaceSpaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WorkspaceSpace object"""

    available = Size(data_key="available", allow_none=True)
    r""" The available space of a workspace, in bytes. """

    total = Size(data_key="total", allow_none=True)
    r""" The total space of a workspace, in bytes. """

    used = Size(data_key="used", allow_none=True)
    r""" The used space of a workspace, in bytes. """

    @property
    def resource(self):
        return WorkspaceSpace

    gettable_fields = [
        "available",
        "total",
        "used",
    ]
    """available,total,used,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class WorkspaceSpace(Resource):

    _schema = WorkspaceSpaceSchema
