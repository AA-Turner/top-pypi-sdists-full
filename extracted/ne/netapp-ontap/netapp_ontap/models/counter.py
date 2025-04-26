r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Counter", "CounterSchema"]
__pdoc__ = {
    "CounterSchema.resource": False,
    "CounterSchema.opts": False,
    "Counter": False,
}


class CounterSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Counter object"""

    counters = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.counter2d.Counter2dSchema", unknown=EXCLUDE, allow_none=True), data_key="counters", allow_none=True)
    r""" List of labels and values for the second dimension. """

    labels = marshmallow_fields.List(marshmallow_fields.Str, data_key="labels", allow_none=True)
    r""" List of labels for the first dimension. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Counter name. """

    value = Size(data_key="value", allow_none=True)
    r""" Scalar value. """

    values = marshmallow_fields.List(Size, data_key="values", allow_none=True)
    r""" List of values in a one-dimensional counter. """

    @property
    def resource(self):
        return Counter

    gettable_fields = [
        "counters",
        "labels",
        "name",
        "value",
        "values",
    ]
    """counters,labels,name,value,values,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class Counter(Resource):

    _schema = CounterSchema
