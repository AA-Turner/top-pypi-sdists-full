r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DcnFru", "DcnFruSchema"]
__pdoc__ = {
    "DcnFruSchema.resource": False,
    "DcnFruSchema.opts": False,
    "DcnFru": False,
}

class DcnFruSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnFru object"""

    count = Size(data_key="count", allow_none=True)
    r""" Number count of the FRUs.

Example: 1 """

    fru_type = marshmallow_fields.Str(data_key="fru_type", allow_none=True)
    r""" The fru_type field of the dcn_fru.

Valid choices:

* fan
* psu
* pcie
* dimm """

    id = marshmallow_fields.Str(data_key="id", allow_none=True)
    r""" The id field of the dcn_fru. """

    @property
    def resource(self):
        return DcnFru

    gettable_fields = [
        "count",
        "fru_type",
        "id",
    ]
    """count,fru_type,id,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DcnFru(Resource):

    _schema = DcnFruSchema
