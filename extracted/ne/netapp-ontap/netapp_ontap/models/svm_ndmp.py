r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmNdmp", "SvmNdmpSchema"]
__pdoc__ = {
    "SvmNdmpSchema.resource": False,
    "SvmNdmpSchema.opts": False,
    "SvmNdmp": False,
}


class SvmNdmpSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmNdmp object"""

    allowed = marshmallow_fields.Boolean(data_key="allowed", allow_none=True)
    r""" If this is set to true, an SVM administrator can manage the NDMP service. If it is false, only the cluster administrator can manage the service. """

    @property
    def resource(self):
        return SvmNdmp

    gettable_fields = [
        "allowed",
    ]
    """allowed,"""

    patchable_fields = [
        "allowed",
    ]
    """allowed,"""

    postable_fields = [
        "allowed",
    ]
    """allowed,"""


class SvmNdmp(Resource):

    _schema = SvmNdmpSchema
