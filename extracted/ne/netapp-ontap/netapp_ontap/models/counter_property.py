r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["CounterProperty", "CounterPropertySchema"]
__pdoc__ = {
    "CounterPropertySchema.resource": False,
    "CounterPropertySchema.opts": False,
    "CounterProperty": False,
}


class CounterPropertySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CounterProperty object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Property name. """

    value = marshmallow_fields.Str(data_key="value", allow_none=True)
    r""" Property value. """

    @property
    def resource(self):
        return CounterProperty

    gettable_fields = [
        "name",
        "value",
    ]
    """name,value,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class CounterProperty(Resource):

    _schema = CounterPropertySchema
