r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["S3UserKeys", "S3UserKeysSchema"]
__pdoc__ = {
    "S3UserKeysSchema.resource": False,
    "S3UserKeysSchema.opts": False,
    "S3UserKeys": False,
}

class S3UserKeysSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3UserKeys object"""

    access_key = marshmallow_fields.Str(data_key="access_key", allow_none=True)
    r""" Specifies the access key for the user.

Example: <AWS-ACCESS-KEY-ID> """

    expiry_time = ImpreciseDateTime(data_key="expiry_time", allow_none=True)
    r""" Specifies the date and time after which keys expire and are no longer valid.

Example: 2024-01-01T00:00:00.000+0000 """

    id = Size(data_key="id", allow_none=True)
    r""" Specifies an S3 user key identifier. Each user can only have a maximum of two keys. The key_id can either be '1' or '2'.

Example: 1 """

    time_to_live = marshmallow_fields.Str(data_key="time_to_live", allow_none=True)
    r""" Indicates the time period from when this parameter is specified:

* when creating or modifying a user or
* when the user keys were last regenerated, after which the user keys expire and are no longer valid.
* Valid format is: 'PnDTnHnMnS|PnW'. For example, P2DT6H3M10S specifies a time period of 2 days, 6 hours, 3 minutes, and 10 seconds.
* If the value specified is '0' seconds, then the keys do not expire.


Example: PT6H3M """

    @property
    def resource(self):
        return S3UserKeys

    gettable_fields = [
        "access_key",
        "expiry_time",
        "id",
        "time_to_live",
    ]
    """access_key,expiry_time,id,time_to_live,"""

    patchable_fields = [
        "access_key",
        "expiry_time",
        "id",
        "time_to_live",
    ]
    """access_key,expiry_time,id,time_to_live,"""

    postable_fields = [
        "access_key",
        "expiry_time",
        "id",
        "time_to_live",
    ]
    """access_key,expiry_time,id,time_to_live,"""


class S3UserKeys(Resource):

    _schema = S3UserKeysSchema
