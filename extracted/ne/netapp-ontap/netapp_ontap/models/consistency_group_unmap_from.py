r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupUnmapFrom", "ConsistencyGroupUnmapFromSchema"]
__pdoc__ = {
    "ConsistencyGroupUnmapFromSchema.resource": False,
    "ConsistencyGroupUnmapFromSchema.opts": False,
    "ConsistencyGroupUnmapFrom": False,
}


class ConsistencyGroupUnmapFromSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupUnmapFrom object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the igroup or subsystem.

Example: subsystem1 """

    @property
    def resource(self):
        return ConsistencyGroupUnmapFrom

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


class ConsistencyGroupUnmapFrom(Resource):

    _schema = ConsistencyGroupUnmapFromSchema
