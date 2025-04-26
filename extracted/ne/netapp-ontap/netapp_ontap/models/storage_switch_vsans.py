r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageSwitchVsans", "StorageSwitchVsansSchema"]
__pdoc__ = {
    "StorageSwitchVsansSchema.resource": False,
    "StorageSwitchVsansSchema.opts": False,
    "StorageSwitchVsans": False,
}


class StorageSwitchVsansSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageSwitchVsans object"""

    id = Size(data_key="id", allow_none=True)
    r""" Storage switch VSAN ID """

    iod = marshmallow_fields.Boolean(data_key="iod", allow_none=True)
    r""" Indicates whether in-order delivery is set for a zone. """

    load_balancing_types = marshmallow_fields.Str(data_key="load_balancing_types", allow_none=True)
    r""" Storage switch VSAN load balancing type """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Storage switch VSAN name """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Storage switch VSAN Port state

Valid choices:

* ok
* error """

    @property
    def resource(self):
        return StorageSwitchVsans

    gettable_fields = [
        "id",
        "iod",
        "load_balancing_types",
        "name",
        "state",
    ]
    """id,iod,load_balancing_types,name,state,"""

    patchable_fields = [
        "id",
        "iod",
        "load_balancing_types",
        "name",
        "state",
    ]
    """id,iod,load_balancing_types,name,state,"""

    postable_fields = [
        "id",
        "iod",
        "load_balancing_types",
        "name",
        "state",
    ]
    """id,iod,load_balancing_types,name,state,"""


class StorageSwitchVsans(Resource):

    _schema = StorageSwitchVsansSchema
