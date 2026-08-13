r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["ContainerVolumesGuarantee", "ContainerVolumesGuaranteeSchema"]
__pdoc__ = {
    "ContainerVolumesGuaranteeSchema.resource": False,
    "ContainerVolumesGuaranteeSchema.opts": False,
    "ContainerVolumesGuarantee": False,
}

class ContainerVolumesGuaranteeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ContainerVolumesGuarantee object"""

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The type of space guarantee of this volume.

Valid choices:

* volume
* none """

    @property
    def resource(self):
        return ContainerVolumesGuarantee

    gettable_fields = [
        "type",
    ]
    """type,"""

    patchable_fields = [
        "type",
    ]
    """type,"""

    postable_fields = [
        "type",
    ]
    """type,"""


class ContainerVolumesGuarantee(Resource):

    _schema = ContainerVolumesGuaranteeSchema
