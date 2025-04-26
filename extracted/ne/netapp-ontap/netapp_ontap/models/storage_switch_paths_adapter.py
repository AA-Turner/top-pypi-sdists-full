r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageSwitchPathsAdapter", "StorageSwitchPathsAdapterSchema"]
__pdoc__ = {
    "StorageSwitchPathsAdapterSchema.resource": False,
    "StorageSwitchPathsAdapterSchema.opts": False,
    "StorageSwitchPathsAdapter": False,
}


class StorageSwitchPathsAdapterSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageSwitchPathsAdapter object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Node adapter name """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Node adapter type

Valid choices:

* unknown
* fcp_initiator
* fc_vi
* fcp_target """

    wwn = marshmallow_fields.Str(data_key="wwn", allow_none=True)
    r""" Node adapter world wide name """

    @property
    def resource(self):
        return StorageSwitchPathsAdapter

    gettable_fields = [
        "name",
        "type",
        "wwn",
    ]
    """name,type,wwn,"""

    patchable_fields = [
        "name",
        "type",
        "wwn",
    ]
    """name,type,wwn,"""

    postable_fields = [
        "name",
        "type",
        "wwn",
    ]
    """name,type,wwn,"""


class StorageSwitchPathsAdapter(Resource):

    _schema = StorageSwitchPathsAdapterSchema
