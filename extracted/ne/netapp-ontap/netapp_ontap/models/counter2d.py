r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Counter2d", "Counter2dSchema"]
__pdoc__ = {
    "Counter2dSchema.resource": False,
    "Counter2dSchema.opts": False,
    "Counter2d": False,
}


class Counter2dSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Counter2d object"""

    label = marshmallow_fields.Str(data_key="label", allow_none=True)
    r""" Second dimension label. """

    values = marshmallow_fields.List(Size, data_key="values", allow_none=True)
    r""" List of values for the counter. """

    @property
    def resource(self):
        return Counter2d

    gettable_fields = [
        "label",
        "values",
    ]
    """label,values,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class Counter2d(Resource):

    _schema = Counter2dSchema
