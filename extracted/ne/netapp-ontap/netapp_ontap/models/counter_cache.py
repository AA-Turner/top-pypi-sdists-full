r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["CounterCache", "CounterCacheSchema"]
__pdoc__ = {
    "CounterCacheSchema.resource": False,
    "CounterCacheSchema.opts": False,
    "CounterCache": False,
}

class CounterCacheSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CounterCache object"""

    checksum_path = marshmallow_fields.Str(data_key="checksum_path", allow_none=True)
    r""" The filepath of the MD5 checksum.

Example: https://<mgmt-ip>/spi/<node-name>/etc/counter_cache/000001_000060_1762292287050_workload.md5 """

    node = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.node", "NodeSchema"),
                unknown=EXCLUDE,
                data_key="node",
                allow_none=True
            )
    r""" The node field of the counter_cache. """

    object = marshmallow_fields.Str(data_key="object", allow_none=True)
    r""" The name of the CM object.

Example: workload """

    path = marshmallow_fields.Str(data_key="path", allow_none=True)
    r""" The filepath of the available protobuf file.

Example: https://<mgmt-ip>/spi/<node-name>/etc/counter_cache/000001_000060_1762292287050_workload.pb """

    sample_period = marshmallow_fields.Str(data_key="sample_period", allow_none=True)
    r""" The frequency at which CM objects and counters will be retrieved.

Valid choices:

* 1m
* 5m
* 10m
* 30m
* 1h """

    size = marshmallow_fields.Str(data_key="size", allow_none=True)
    r""" The size of the available protobuf file, in bytes.

Example: 24000000 """

    timestamp = ImpreciseDateTime(data_key="timestamp", allow_none=True)
    r""" The time the data was copied over.

Example: 2025-12-12T15:00:00.000+0000 """

    @property
    def resource(self):
        return CounterCache

    gettable_fields = [
        "checksum_path",
        "node.links",
        "node.name",
        "node.uuid",
        "object",
        "path",
        "sample_period",
        "size",
        "timestamp",
    ]
    """checksum_path,node.links,node.name,node.uuid,object,path,sample_period,size,timestamp,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class CounterCache(Resource):

    _schema = CounterCacheSchema
