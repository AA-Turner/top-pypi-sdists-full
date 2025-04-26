r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NfsServiceAccessCacheConfig", "NfsServiceAccessCacheConfigSchema"]
__pdoc__ = {
    "NfsServiceAccessCacheConfigSchema.resource": False,
    "NfsServiceAccessCacheConfigSchema.opts": False,
    "NfsServiceAccessCacheConfig": False,
}


class NfsServiceAccessCacheConfigSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NfsServiceAccessCacheConfig object"""

    harvest_timeout = Size(data_key="harvest_timeout", allow_none=True)
    r""" Specifies the time after which an entry is deleted from the access cache, if unused.

Example: 3600 """

    is_dns_ttl_enabled = marshmallow_fields.Boolean(data_key="isDnsTTLEnabled", allow_none=True)
    r""" Specifies whether Dns TTL is enabled. """

    ttl_failure = Size(data_key="ttl_failure", allow_none=True)
    r""" Specifies the time to live value for entries for which a failure was encountered, in seconds.

Example: 1 """

    ttl_negative = Size(data_key="ttl_negative", allow_none=True)
    r""" Specifies the time to live value of a negative access cache, in seconds.

Example: 30 """

    ttl_positive = Size(data_key="ttl_positive", allow_none=True)
    r""" Specifies the time to live value of a positive access cache, in seconds.

Example: 60 """

    @property
    def resource(self):
        return NfsServiceAccessCacheConfig

    gettable_fields = [
        "harvest_timeout",
        "is_dns_ttl_enabled",
        "ttl_failure",
        "ttl_negative",
        "ttl_positive",
    ]
    """harvest_timeout,is_dns_ttl_enabled,ttl_failure,ttl_negative,ttl_positive,"""

    patchable_fields = [
        "harvest_timeout",
        "is_dns_ttl_enabled",
        "ttl_failure",
        "ttl_negative",
        "ttl_positive",
    ]
    """harvest_timeout,is_dns_ttl_enabled,ttl_failure,ttl_negative,ttl_positive,"""

    postable_fields = [
        "harvest_timeout",
        "is_dns_ttl_enabled",
        "ttl_failure",
        "ttl_negative",
        "ttl_positive",
    ]
    """harvest_timeout,is_dns_ttl_enabled,ttl_failure,ttl_negative,ttl_positive,"""


class NfsServiceAccessCacheConfig(Resource):

    _schema = NfsServiceAccessCacheConfigSchema
