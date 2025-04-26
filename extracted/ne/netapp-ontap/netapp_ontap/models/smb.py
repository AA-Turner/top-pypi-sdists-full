r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Smb", "SmbSchema"]
__pdoc__ = {
    "SmbSchema.resource": False,
    "SmbSchema.opts": False,
    "Smb": False,
}


class SmbSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Smb object"""

    connect_state = marshmallow_fields.Str(data_key="connect_state", allow_none=True)
    r""" SMB connection state.

Valid choices:

* connected
* disconnected
* reconnecting
* timedout """

    open_group_id = marshmallow_fields.Str(data_key="open_group_id", allow_none=True)
    r""" SMB open group ID. """

    open_type = marshmallow_fields.Str(data_key="open_type", allow_none=True)
    r""" SMB open type.

Valid choices:

* none
* durable
* persistent """

    @property
    def resource(self):
        return Smb

    gettable_fields = [
        "connect_state",
        "open_group_id",
        "open_type",
    ]
    """connect_state,open_group_id,open_type,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class Smb(Resource):

    _schema = SmbSchema
