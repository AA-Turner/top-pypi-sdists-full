r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ShelfAcpsError", "ShelfAcpsErrorSchema"]
__pdoc__ = {
    "ShelfAcpsErrorSchema.resource": False,
    "ShelfAcpsErrorSchema.opts": False,
    "ShelfAcpsError": False,
}


class ShelfAcpsErrorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ShelfAcpsError object"""

    reason = marshmallow_fields.Nested("netapp_ontap.models.error.ErrorSchema", unknown=EXCLUDE, data_key="reason", allow_none=True)
    r""" The reason field of the shelf_acps_error. """

    severity = marshmallow_fields.Str(data_key="severity", allow_none=True)
    r""" The severity field of the shelf_acps_error.

Valid choices:

* unknown
* notice
* warning
* error
* critical """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The type field of the shelf_acps_error.

Valid choices:

* not_applicable
* connection_issue
* connection_activity
* module_error
* shelf_error """

    @property
    def resource(self):
        return ShelfAcpsError

    gettable_fields = [
        "reason",
        "severity",
        "type",
    ]
    """reason,severity,type,"""

    patchable_fields = [
        "severity",
        "type",
    ]
    """severity,type,"""

    postable_fields = [
        "severity",
        "type",
    ]
    """severity,type,"""


class ShelfAcpsError(Resource):

    _schema = ShelfAcpsErrorSchema
