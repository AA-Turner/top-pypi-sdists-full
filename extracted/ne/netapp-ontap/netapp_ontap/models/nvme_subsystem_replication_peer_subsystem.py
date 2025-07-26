r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeSubsystemReplicationPeerSubsystem", "NvmeSubsystemReplicationPeerSubsystemSchema"]
__pdoc__ = {
    "NvmeSubsystemReplicationPeerSubsystemSchema.resource": False,
    "NvmeSubsystemReplicationPeerSubsystemSchema.opts": False,
    "NvmeSubsystemReplicationPeerSubsystem": False,
}


class NvmeSubsystemReplicationPeerSubsystemSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeSubsystemReplicationPeerSubsystem object"""

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the peer subsystem.


Example: 1cd8a443-86d2-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return NvmeSubsystemReplicationPeerSubsystem

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


class NvmeSubsystemReplicationPeerSubsystem(Resource):

    _schema = NvmeSubsystemReplicationPeerSubsystemSchema
