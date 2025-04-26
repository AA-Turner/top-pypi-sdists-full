r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FlexcacheGuarantee", "FlexcacheGuaranteeSchema"]
__pdoc__ = {
    "FlexcacheGuaranteeSchema.resource": False,
    "FlexcacheGuaranteeSchema.opts": False,
    "FlexcacheGuarantee": False,
}


class FlexcacheGuaranteeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FlexcacheGuarantee object"""

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The type of space guarantee of this volume in the aggregate.

Valid choices:

* volume
* none """

    @property
    def resource(self):
        return FlexcacheGuarantee

    gettable_fields = [
        "type",
    ]
    """type,"""

    patchable_fields = [
        "type",
    ]
    """type,"""

    postable_fields = [
        "type",
    ]
    """type,"""


class FlexcacheGuarantee(Resource):

    _schema = FlexcacheGuaranteeSchema
