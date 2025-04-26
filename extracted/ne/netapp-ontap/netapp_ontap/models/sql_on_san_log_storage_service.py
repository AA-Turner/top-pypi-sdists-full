r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SqlOnSanLogStorageService", "SqlOnSanLogStorageServiceSchema"]
__pdoc__ = {
    "SqlOnSanLogStorageServiceSchema.resource": False,
    "SqlOnSanLogStorageServiceSchema.opts": False,
    "SqlOnSanLogStorageService": False,
}


class SqlOnSanLogStorageServiceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SqlOnSanLogStorageService object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The storage service of the log DB.

Valid choices:

* extreme
* performance
* value """

    @property
    def resource(self):
        return SqlOnSanLogStorageService

    gettable_fields = [
        "name",
    ]
    """name,"""

    patchable_fields = [
        "name",
    ]
    """name,"""

    postable_fields = [
        "name",
    ]
    """name,"""


class SqlOnSanLogStorageService(Resource):

    _schema = SqlOnSanLogStorageServiceSchema
