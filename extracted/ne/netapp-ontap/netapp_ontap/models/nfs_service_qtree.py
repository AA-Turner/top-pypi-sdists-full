r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NfsServiceQtree", "NfsServiceQtreeSchema"]
__pdoc__ = {
    "NfsServiceQtreeSchema.resource": False,
    "NfsServiceQtreeSchema.opts": False,
    "NfsServiceQtree": False,
}


class NfsServiceQtreeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NfsServiceQtree object"""

    export_enabled = marshmallow_fields.Boolean(data_key="export_enabled", allow_none=True)
    r""" Specifies whether qtree export is enabled. """

    validate_export = marshmallow_fields.Boolean(data_key="validate_export", allow_none=True)
    r""" Specifies whether qtree export validation is enabled. """

    @property
    def resource(self):
        return NfsServiceQtree

    gettable_fields = [
        "export_enabled",
        "validate_export",
    ]
    """export_enabled,validate_export,"""

    patchable_fields = [
        "validate_export",
    ]
    """validate_export,"""

    postable_fields = [
        "validate_export",
    ]
    """validate_export,"""


class NfsServiceQtree(Resource):

    _schema = NfsServiceQtreeSchema
