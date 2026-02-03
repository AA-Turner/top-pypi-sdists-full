r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DcnBondPort", "DcnBondPortSchema"]
__pdoc__ = {
    "DcnBondPortSchema.resource": False,
    "DcnBondPortSchema.opts": False,
    "DcnBondPort": False,
}

class DcnBondPortSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnBondPort object"""

    actual_state = marshmallow_fields.Str(data_key="actual_state", allow_none=True)
    r""" The actual state of the physical network port, as read from the system. """

    configured_state = marshmallow_fields.Str(data_key="configured_state", allow_none=True)
    r""" The desired state of the physical network port. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the physical network port that is included in this bond interface.

Example: e2a """

    @property
    def resource(self):
        return DcnBondPort

    gettable_fields = [
        "actual_state",
        "configured_state",
        "name",
    ]
    """actual_state,configured_state,name,"""

    patchable_fields = [
        "configured_state",
    ]
    """configured_state,"""

    postable_fields = [
        "configured_state",
    ]
    """configured_state,"""


class DcnBondPort(Resource):

    _schema = DcnBondPortSchema
