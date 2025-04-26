r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SnaplockLitigationGetOperations", "SnaplockLitigationGetOperationsSchema"]
__pdoc__ = {
    "SnaplockLitigationGetOperationsSchema.resource": False,
    "SnaplockLitigationGetOperationsSchema.opts": False,
    "SnaplockLitigationGetOperations": False,
}


class SnaplockLitigationGetOperationsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnaplockLitigationGetOperations object"""

    id = Size(data_key="id", allow_none=True)
    r""" Operation ID.

Example: 16842759 """

    @property
    def resource(self):
        return SnaplockLitigationGetOperations

    gettable_fields = [
        "id",
    ]
    """id,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class SnaplockLitigationGetOperations(Resource):

    _schema = SnaplockLitigationGetOperationsSchema
