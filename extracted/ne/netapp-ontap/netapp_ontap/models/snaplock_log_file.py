r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SnaplockLogFile", "SnaplockLogFileSchema"]
__pdoc__ = {
    "SnaplockLogFileSchema.resource": False,
    "SnaplockLogFileSchema.opts": False,
    "SnaplockLogFile": False,
}


class SnaplockLogFileSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnaplockLogFile object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the snaplock_log_file. """

    base_name = marshmallow_fields.Str(data_key="base_name", allow_none=True)
    r""" Base name of log file

Valid choices:

* legal_hold
* privileged_delete
* system """

    expiry_time = ImpreciseDateTime(data_key="expiry_time", allow_none=True)
    r""" Expiry time of the log file in date-time format. Value '9999-12-31T00:00:00Z' indicates infinite expiry time.

Example: 2058-06-04T19:00:00.000+0000 """

    path = marshmallow_fields.Str(data_key="path", allow_none=True)
    r""" Absolute path of the log file in the volume

Example: /snaplock_log/system_logs/20180822_005947_GMT-present """

    size = Size(data_key="size", allow_none=True)
    r""" Size of the log file in bytes

Example: 20000 """

    @property
    def resource(self):
        return SnaplockLogFile

    gettable_fields = [
        "links",
        "base_name",
        "expiry_time",
        "path",
        "size",
    ]
    """links,base_name,expiry_time,path,size,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class SnaplockLogFile(Resource):

    _schema = SnaplockLogFileSchema
