r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union

from marshmallow import fields as marshmallow_fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["CounterRow", "CounterRowSchema"]
__pdoc__ = {
    "CounterRowSchema.resource": False,
    "CounterRowSchema.opts": False,
}


class CounterRowSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CounterRow object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the counter_row."""

    aggregation = marshmallow_fields.Nested("netapp_ontap.models.instance_counter_aggregation.InstanceCounterAggregationSchema", data_key="aggregation", unknown=EXCLUDE, allow_none=True)
    r""" Aggregation information about this counter."""

    counter_table = marshmallow_fields.Nested("netapp_ontap.resources.counter_table.CounterTableSchema", data_key="counter_table", unknown=EXCLUDE, allow_none=True)
    r""" The counter_table field of the counter_row."""

    counters = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.counter.CounterSchema", unknown=EXCLUDE, allow_none=True), data_key="counters", allow_none=True)
    r""" Array of counter name/value pairs."""

    id = marshmallow_fields.Str(
        data_key="id",
        allow_none=True,
    )
    r""" Unique row identifier."""

    properties = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.counter_property.CounterPropertySchema", unknown=EXCLUDE, allow_none=True), data_key="properties", allow_none=True)
    r""" Array of property name/value pairs."""

    @property
    def resource(self):
        return CounterRow

    gettable_fields = [
        "links",
        "aggregation",
        "counter_table.links",
        "counter_table.name",
        "counters",
        "id",
        "properties",
    ]
    """links,aggregation,counter_table.links,counter_table.name,counters,id,properties,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class CounterRow(Resource):
    r""" A single row of counter and property counter data. """

    _schema = CounterRowSchema
    _path = "/api/cluster/counter/tables/{counter_table[name]}/rows"
    _keys = ["counter_table.name", "id"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Returns a collection of counter rows."""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all CounterRow resources that match the provided query"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)


    @classmethod
    def fast_get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["RawResource"]:
        """Returns a list of RawResources that represent CounterRow resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Returns a collection of counter rows."""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Returns a single counter row."""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





