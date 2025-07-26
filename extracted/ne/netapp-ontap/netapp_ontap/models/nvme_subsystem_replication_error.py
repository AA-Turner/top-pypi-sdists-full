r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeSubsystemReplicationError", "NvmeSubsystemReplicationErrorSchema"]
__pdoc__ = {
    "NvmeSubsystemReplicationErrorSchema.resource": False,
    "NvmeSubsystemReplicationErrorSchema.opts": False,
    "NvmeSubsystemReplicationError": False,
}


class NvmeSubsystemReplicationErrorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeSubsystemReplicationError object"""

    subsystem = marshmallow_fields.Nested("netapp_ontap.models.replication_error_subsystem.ReplicationErrorSubsystemSchema", unknown=EXCLUDE, data_key="subsystem", allow_none=True)
    r""" An NVMe subsystem maintains configuration state and NVMe namespace access control for a set of NVMe-connected hosts. """

    summary = marshmallow_fields.Nested("netapp_ontap.models.error.ErrorSchema", unknown=EXCLUDE, data_key="summary", allow_none=True)
    r""" The summary field of the nvme_subsystem_replication_error. """

    @property
    def resource(self):
        return NvmeSubsystemReplicationError

    gettable_fields = [
        "subsystem",
        "summary",
    ]
    """subsystem,summary,"""

    patchable_fields = [
        "subsystem",
    ]
    """subsystem,"""

    postable_fields = [
        "subsystem",
    ]
    """subsystem,"""


class NvmeSubsystemReplicationError(Resource):

    _schema = NvmeSubsystemReplicationErrorSchema
