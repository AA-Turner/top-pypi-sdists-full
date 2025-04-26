r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["RaidGroupReconstruct", "RaidGroupReconstructSchema"]
__pdoc__ = {
    "RaidGroupReconstructSchema.resource": False,
    "RaidGroupReconstructSchema.opts": False,
    "RaidGroupReconstruct": False,
}


class RaidGroupReconstructSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the RaidGroupReconstruct object"""

    active = marshmallow_fields.Boolean(data_key="active", allow_none=True)
    r""" One or more disks in this RAID group are being reconstructed. """

    percent = Size(data_key="percent", allow_none=True)
    r""" Reconstruct percentage

Example: 10 """

    @property
    def resource(self):
        return RaidGroupReconstruct

    gettable_fields = [
        "active",
        "percent",
    ]
    """active,percent,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class RaidGroupReconstruct(Resource):

    _schema = RaidGroupReconstructSchema
