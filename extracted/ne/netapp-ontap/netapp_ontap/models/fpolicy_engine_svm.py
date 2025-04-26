r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FpolicyEngineSvm", "FpolicyEngineSvmSchema"]
__pdoc__ = {
    "FpolicyEngineSvmSchema.resource": False,
    "FpolicyEngineSvmSchema.opts": False,
    "FpolicyEngineSvm": False,
}


class FpolicyEngineSvmSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FpolicyEngineSvm object"""

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" SVM UUID """

    @property
    def resource(self):
        return FpolicyEngineSvm

    gettable_fields = [
        "uuid",
    ]
    """uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class FpolicyEngineSvm(Resource):

    _schema = FpolicyEngineSvmSchema
