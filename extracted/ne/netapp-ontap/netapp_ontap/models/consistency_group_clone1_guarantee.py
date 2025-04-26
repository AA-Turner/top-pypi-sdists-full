r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupClone1Guarantee", "ConsistencyGroupClone1GuaranteeSchema"]
__pdoc__ = {
    "ConsistencyGroupClone1GuaranteeSchema.resource": False,
    "ConsistencyGroupClone1GuaranteeSchema.opts": False,
    "ConsistencyGroupClone1Guarantee": False,
}


class ConsistencyGroupClone1GuaranteeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupClone1Guarantee object"""

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The type of space guarantee of this volume in the aggregate.

Valid choices:

* volume
* none """

    @property
    def resource(self):
        return ConsistencyGroupClone1Guarantee

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


class ConsistencyGroupClone1Guarantee(Resource):

    _schema = ConsistencyGroupClone1GuaranteeSchema
