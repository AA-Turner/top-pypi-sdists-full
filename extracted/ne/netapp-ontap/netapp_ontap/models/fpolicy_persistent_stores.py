r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FpolicyPersistentStores", "FpolicyPersistentStoresSchema"]
__pdoc__ = {
    "FpolicyPersistentStoresSchema.resource": False,
    "FpolicyPersistentStoresSchema.opts": False,
    "FpolicyPersistentStores": False,
}


class FpolicyPersistentStoresSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FpolicyPersistentStores object"""

    autosize_mode = marshmallow_fields.Str(data_key="autosize_mode", allow_none=True)
    r""" Autosize mode for the volume.<br>grow &dash; Volume automatically grows in response to the amount of space used.<br>grow_shrink &dash; Volume grows or shrinks in response to the amount of space used.<br>off &dash; Autosizing of the volume is disabled.

Valid choices:

* grow
* grow_shrink
* off """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name specified for the FPolicy Persistent Store.

Example: ps1 """

    size = Size(data_key="size", allow_none=True)
    r""" The size of the Persistent Store volume, in bytes.

Example: 100M """

    volume = marshmallow_fields.Str(data_key="volume", allow_none=True)
    r""" The specified volume to store the events for the FPolicy Persistent Store.

Example: psvol """

    @property
    def resource(self):
        return FpolicyPersistentStores

    gettable_fields = [
        "autosize_mode",
        "name",
        "size",
        "volume",
    ]
    """autosize_mode,name,size,volume,"""

    patchable_fields = [
        "size",
        "volume",
    ]
    """size,volume,"""

    postable_fields = [
        "autosize_mode",
        "name",
        "size",
        "volume",
    ]
    """autosize_mode,name,size,volume,"""


class FpolicyPersistentStores(Resource):

    _schema = FpolicyPersistentStoresSchema
