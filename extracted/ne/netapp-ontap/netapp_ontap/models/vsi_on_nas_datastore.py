r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VsiOnNasDatastore", "VsiOnNasDatastoreSchema"]
__pdoc__ = {
    "VsiOnNasDatastoreSchema.resource": False,
    "VsiOnNasDatastoreSchema.opts": False,
    "VsiOnNasDatastore": False,
}


class VsiOnNasDatastoreSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VsiOnNasDatastore object"""

    count = Size(data_key="count", allow_none=True)
    r""" The number of datastores to support. """

    size = Size(data_key="size", allow_none=True)
    r""" The size of the datastore. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} """

    storage_service = marshmallow_fields.Nested("netapp_ontap.models.vsi_on_nas_datastore_storage_service.VsiOnNasDatastoreStorageServiceSchema", unknown=EXCLUDE, data_key="storage_service", allow_none=True)
    r""" The storage_service field of the vsi_on_nas_datastore. """

    @property
    def resource(self):
        return VsiOnNasDatastore

    gettable_fields = [
        "count",
        "size",
        "storage_service",
    ]
    """count,size,storage_service,"""

    patchable_fields = [
        "count",
        "storage_service",
    ]
    """count,storage_service,"""

    postable_fields = [
        "count",
        "size",
        "storage_service",
    ]
    """count,size,storage_service,"""


class VsiOnNasDatastore(Resource):

    _schema = VsiOnNasDatastoreSchema
