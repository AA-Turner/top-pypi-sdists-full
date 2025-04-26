r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NfsServiceWindows", "NfsServiceWindowsSchema"]
__pdoc__ = {
    "NfsServiceWindowsSchema.resource": False,
    "NfsServiceWindowsSchema.opts": False,
    "NfsServiceWindows": False,
}


class NfsServiceWindowsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NfsServiceWindows object"""

    default_user = marshmallow_fields.Str(data_key="default_user", allow_none=True)
    r""" Specifies the default Windows user for the NFS server. """

    map_unknown_uid_to_default_user = marshmallow_fields.Boolean(data_key="map_unknown_uid_to_default_user", allow_none=True)
    r""" Specifies whether or not the mapping of an unknown UID to the default Windows user is enabled. """

    v3_ms_dos_client_enabled = marshmallow_fields.Boolean(data_key="v3_ms_dos_client_enabled", allow_none=True)
    r""" Specifies whether NFSv3 MS-DOS client support is enabled. """

    @property
    def resource(self):
        return NfsServiceWindows

    gettable_fields = [
        "default_user",
        "map_unknown_uid_to_default_user",
        "v3_ms_dos_client_enabled",
    ]
    """default_user,map_unknown_uid_to_default_user,v3_ms_dos_client_enabled,"""

    patchable_fields = [
        "default_user",
        "map_unknown_uid_to_default_user",
        "v3_ms_dos_client_enabled",
    ]
    """default_user,map_unknown_uid_to_default_user,v3_ms_dos_client_enabled,"""

    postable_fields = [
        "default_user",
        "map_unknown_uid_to_default_user",
        "v3_ms_dos_client_enabled",
    ]
    """default_user,map_unknown_uid_to_default_user,v3_ms_dos_client_enabled,"""


class NfsServiceWindows(Resource):

    _schema = NfsServiceWindowsSchema
