r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Share", "ShareSchema"]
__pdoc__ = {
    "ShareSchema.resource": False,
    "ShareSchema.opts": False,
    "Share": False,
}


class ShareSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Share object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Displays the file or directory effective permission for the mentioned user, only for files and directories contained where the
specified path is relative to the root of the specified share. If this parameter is not specified, the SVM root volume is
taken as the default. If this parameter is specified, the effective share permission of the user is also displayed.
Wildcard query characters are not supported. """

    path = marshmallow_fields.Str(data_key="path", allow_none=True)
    r""" Displays the CIFS share path. """

    @property
    def resource(self):
        return Share

    gettable_fields = [
        "name",
        "path",
    ]
    """name,path,"""

    patchable_fields = [
        "name",
        "path",
    ]
    """name,path,"""

    postable_fields = [
        "name",
        "path",
    ]
    """name,path,"""


class Share(Resource):

    _schema = ShareSchema
