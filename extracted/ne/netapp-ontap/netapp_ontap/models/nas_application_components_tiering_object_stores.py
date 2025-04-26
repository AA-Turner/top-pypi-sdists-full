r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NasApplicationComponentsTieringObjectStores", "NasApplicationComponentsTieringObjectStoresSchema"]
__pdoc__ = {
    "NasApplicationComponentsTieringObjectStoresSchema.resource": False,
    "NasApplicationComponentsTieringObjectStoresSchema.opts": False,
    "NasApplicationComponentsTieringObjectStores": False,
}


class NasApplicationComponentsTieringObjectStoresSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NasApplicationComponentsTieringObjectStores object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the object-store to use. """

    @property
    def resource(self):
        return NasApplicationComponentsTieringObjectStores

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "name",
    ]
    """name,"""


class NasApplicationComponentsTieringObjectStores(Resource):

    _schema = NasApplicationComponentsTieringObjectStoresSchema
