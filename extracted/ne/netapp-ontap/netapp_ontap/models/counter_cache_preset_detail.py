r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["CounterCachePresetDetail", "CounterCachePresetDetailSchema"]
__pdoc__ = {
    "CounterCachePresetDetailSchema.resource": False,
    "CounterCachePresetDetailSchema.opts": False,
    "CounterCachePresetDetail": False,
}

class CounterCachePresetDetailSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CounterCachePresetDetail object"""

    counters = marshmallow_fields.List(marshmallow_fields.Str, data_key="counters", allow_none=True)
    r""" The set of performance counters.

Example: ["instance_name","instance_uuid","auto_aggregate_uuid","auto_aggregate_name"] """

    object = marshmallow_fields.Str(data_key="object", allow_none=True)
    r""" The name of the object.

Example: workload """

    sample_period = marshmallow_fields.Str(data_key="sample_period", allow_none=True)
    r""" The frequency at which CM objects and counters will be retrieved.

Valid choices:

* 1m
* 5m
* 10m
* 30m
* 1h """

    @property
    def resource(self):
        return CounterCachePresetDetail

    gettable_fields = [
        "counters",
        "object",
        "sample_period",
    ]
    """counters,object,sample_period,"""

    patchable_fields = [
        "counters",
        "object",
        "sample_period",
    ]
    """counters,object,sample_period,"""

    postable_fields = [
        "counters",
        "object",
        "sample_period",
    ]
    """counters,object,sample_period,"""


class CounterCachePresetDetail(Resource):

    _schema = CounterCachePresetDetailSchema
