r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["ContainerVolumesStorageService", "ContainerVolumesStorageServiceSchema"]
__pdoc__ = {
    "ContainerVolumesStorageServiceSchema.resource": False,
    "ContainerVolumesStorageServiceSchema.opts": False,
    "ContainerVolumesStorageService": False,
}

class ContainerVolumesStorageServiceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ContainerVolumesStorageService object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Storage service name. If not specified, the default value is the most performant for the platform.


Valid choices:

* extreme
* performance
* value """

    @property
    def resource(self):
        return ContainerVolumesStorageService

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


class ContainerVolumesStorageService(Resource):

    _schema = ContainerVolumesStorageServiceSchema
