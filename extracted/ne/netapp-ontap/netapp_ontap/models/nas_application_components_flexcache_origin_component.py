r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NasApplicationComponentsFlexcacheOriginComponent", "NasApplicationComponentsFlexcacheOriginComponentSchema"]
__pdoc__ = {
    "NasApplicationComponentsFlexcacheOriginComponentSchema.resource": False,
    "NasApplicationComponentsFlexcacheOriginComponentSchema.opts": False,
    "NasApplicationComponentsFlexcacheOriginComponent": False,
}


class NasApplicationComponentsFlexcacheOriginComponentSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NasApplicationComponentsFlexcacheOriginComponent object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the source component. """

    @property
    def resource(self):
        return NasApplicationComponentsFlexcacheOriginComponent

    gettable_fields = [
        "name",
    ]
    """name,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "name",
    ]
    """name,"""


class NasApplicationComponentsFlexcacheOriginComponent(Resource):

    _schema = NasApplicationComponentsFlexcacheOriginComponentSchema
