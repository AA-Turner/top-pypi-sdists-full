r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["NfsServiceCredentialCache", "NfsServiceCredentialCacheSchema"]
__pdoc__ = {
    "NfsServiceCredentialCacheSchema.resource": False,
    "NfsServiceCredentialCacheSchema.opts": False,
    "NfsServiceCredentialCache": False,
}

class NfsServiceCredentialCacheSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NfsServiceCredentialCache object"""

    harvest_timeout = Size(data_key="harvest_timeout", allow_none=True)
    r""" Specifies the age of the unused cached entries, in milliseconds, after which they are cleared from the cache.

Example: 86400000 """

    negative_ttl = Size(data_key="negative_ttl", allow_none=True)
    r""" Specifies the age in milliseconds, of the negative cached credentials after which they are cleared from the cache.

Example: 3600000 """

    positive_ttl = Size(data_key="positive_ttl", allow_none=True)
    r""" Specifies the age in milliseconds, of the positive cached credentials after which they are cleared from the cache.

Example: 3600000 """

    transient_error_ttl = Size(data_key="transient_error_ttl", allow_none=True)
    r""" Specifies the age in milliseconds, of the cached entries during a transient error situation.

Example: 30000 """

    @property
    def resource(self):
        return NfsServiceCredentialCache

    gettable_fields = [
        "harvest_timeout",
        "negative_ttl",
        "positive_ttl",
        "transient_error_ttl",
    ]
    """harvest_timeout,negative_ttl,positive_ttl,transient_error_ttl,"""

    patchable_fields = [
        "harvest_timeout",
        "negative_ttl",
        "positive_ttl",
        "transient_error_ttl",
    ]
    """harvest_timeout,negative_ttl,positive_ttl,transient_error_ttl,"""

    postable_fields = [
        "harvest_timeout",
        "negative_ttl",
        "positive_ttl",
        "transient_error_ttl",
    ]
    """harvest_timeout,negative_ttl,positive_ttl,transient_error_ttl,"""


class NfsServiceCredentialCache(Resource):

    _schema = NfsServiceCredentialCacheSchema
