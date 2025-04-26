r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupMapTo", "ConsistencyGroupMapToSchema"]
__pdoc__ = {
    "ConsistencyGroupMapToSchema.resource": False,
    "ConsistencyGroupMapToSchema.opts": False,
    "ConsistencyGroupMapTo": False,
}


class ConsistencyGroupMapToSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupMapTo object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the igroup or subsystem.

Example: igroup1 """

    @property
    def resource(self):
        return ConsistencyGroupMapTo

    gettable_fields = [
        "name",
    ]
    """name,"""

    patchable_fields = [
        "name",
    ]
    """name,"""

    postable_fields = [
        "name",
    ]
    """name,"""


class ConsistencyGroupMapTo(Resource):

    _schema = ConsistencyGroupMapToSchema
