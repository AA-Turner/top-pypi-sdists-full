r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FabricCache", "FabricCacheSchema"]
__pdoc__ = {
    "FabricCacheSchema.resource": False,
    "FabricCacheSchema.opts": False,
    "FabricCache": False,
}


class FabricCacheSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FabricCache object"""

    age = marshmallow_fields.Str(data_key="age", allow_none=True)
    r""" The age of the Fibre Channel fabric data cache retrieved. If the FC fabric data cache has not been fully updated for a newly discovered fabric, or a fabric that has been re-discovered after being purged, a value for this property will not be retrieved. The value is in ISO 8601 duration format.


Example: PT3M30S """

    is_current = marshmallow_fields.Boolean(data_key="is_current", allow_none=True)
    r""" A boolean that indicates if the retrieved data is current relative to the `cache.maximum_age` value of the request. A value of `true` indicates that the data is no older than the requested maximum age. A value of `false` indicates that the data is older than the requested maximum age; if more current data is required, the caller should wait for some time for the cache update to complete and query the data again. """

    update_time = ImpreciseDateTime(data_key="update_time", allow_none=True)
    r""" The date and time at which the Fibre Channel fabric data cache retrieved was last updated. If the FC fabric data cache has not been fully updated for a newly discovered fabric, or a fabric that has been re-discovered after being purged, a value for this property will not be retrieved. """

    @property
    def resource(self):
        return FabricCache

    gettable_fields = [
        "age",
        "is_current",
        "update_time",
    ]
    """age,is_current,update_time,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class FabricCache(Resource):

    _schema = FabricCacheSchema
