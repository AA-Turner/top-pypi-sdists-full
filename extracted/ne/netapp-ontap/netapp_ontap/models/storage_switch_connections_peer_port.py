r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageSwitchConnectionsPeerPort", "StorageSwitchConnectionsPeerPortSchema"]
__pdoc__ = {
    "StorageSwitchConnectionsPeerPortSchema.resource": False,
    "StorageSwitchConnectionsPeerPortSchema.opts": False,
    "StorageSwitchConnectionsPeerPort": False,
}


class StorageSwitchConnectionsPeerPortSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageSwitchConnectionsPeerPort object"""

    connection = marshmallow_fields.Str(data_key="connection", allow_none=True)
    r""" Storage switch peer port host and name """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Storage switch peer type

Valid choices:

* unknown
* bridge
* switch
* fcp_adapter
* fcvi_adapter """

    unique_id = marshmallow_fields.Str(data_key="unique_id", allow_none=True)
    r""" Storage switch peer unique ID """

    wwn = marshmallow_fields.Str(data_key="wwn", allow_none=True)
    r""" Storage switch peer port world wide name """

    @property
    def resource(self):
        return StorageSwitchConnectionsPeerPort

    gettable_fields = [
        "connection",
        "type",
        "unique_id",
        "wwn",
    ]
    """connection,type,unique_id,wwn,"""

    patchable_fields = [
        "connection",
        "type",
        "unique_id",
        "wwn",
    ]
    """connection,type,unique_id,wwn,"""

    postable_fields = [
        "connection",
        "type",
        "unique_id",
        "wwn",
    ]
    """connection,type,unique_id,wwn,"""


class StorageSwitchConnectionsPeerPort(Resource):

    _schema = StorageSwitchConnectionsPeerPortSchema
