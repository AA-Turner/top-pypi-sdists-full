r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationLunObject", "ApplicationLunObjectSchema"]
__pdoc__ = {
    "ApplicationLunObjectSchema.resource": False,
    "ApplicationLunObjectSchema.opts": False,
    "ApplicationLunObject": False,
}


class ApplicationLunObjectSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationLunObject object"""

    creation_timestamp = ImpreciseDateTime(data_key="creation_timestamp", allow_none=True)
    r""" LUN creation time """

    path = marshmallow_fields.Str(data_key="path", allow_none=True)
    r""" LUN path """

    size = Size(data_key="size", allow_none=True)
    r""" LUN size """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" LUN UUID """

    @property
    def resource(self):
        return ApplicationLunObject

    gettable_fields = [
        "creation_timestamp",
        "path",
        "size",
        "uuid",
    ]
    """creation_timestamp,path,size,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ApplicationLunObject(Resource):

    _schema = ApplicationLunObjectSchema
