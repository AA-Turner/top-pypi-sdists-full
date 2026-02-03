r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DcnNodeError", "DcnNodeErrorSchema"]
__pdoc__ = {
    "DcnNodeErrorSchema.resource": False,
    "DcnNodeErrorSchema.opts": False,
    "DcnNodeError": False,
}

class DcnNodeErrorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnNodeError object"""

    count = Size(data_key="count", allow_none=True)
    r""" Number count of failed units.

Example: 1 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Error code describing the current condition.

Example: 111411208 """

    unit_type = marshmallow_fields.Str(data_key="unit_type", allow_none=True)
    r""" The unit_type field of the dcn_node_error.

Valid choices:

* over_temperature
* fan
* psu
* cpu
* gpu
* pcie
* dimm
* file_system
* disk
* system
* memory
* network """

    @property
    def resource(self):
        return DcnNodeError

    gettable_fields = [
        "count",
        "message",
        "unit_type",
    ]
    """count,message,unit_type,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DcnNodeError(Resource):

    _schema = DcnNodeErrorSchema
