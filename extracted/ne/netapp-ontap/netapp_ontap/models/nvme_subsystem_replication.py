r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeSubsystemReplication", "NvmeSubsystemReplicationSchema"]
__pdoc__ = {
    "NvmeSubsystemReplicationSchema.resource": False,
    "NvmeSubsystemReplicationSchema.opts": False,
    "NvmeSubsystemReplication": False,
}


class NvmeSubsystemReplicationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeSubsystemReplication object"""

    error = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_replication_error.NvmeSubsystemReplicationErrorSchema", unknown=EXCLUDE, data_key="error", allow_none=True)
    r""" Information about asynchronous errors encountered while replicating this subsystem. Subsystems within a peering relationship are replicated in the same stream, so the error reported here might be related to this subsystem or a prior replicated subsystem that is now blocking the replication of this subsystem. Both the error information and the subsystem encountering the error are reported. If the error is configuration related, it can be corrected on the referenced subsystem. The replication is retried using exponential backoff up to a maximum of one retry every 5 minutes. Every operation on the same stream triggers an immediate retry and restarts the exponential backoff starting with a 1 second delay. If the error is system related, the retries should correct the error when the system enters a healthy state. """

    peer_subsystem = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_replication_peer_subsystem.NvmeSubsystemReplicationPeerSubsystemSchema", unknown=EXCLUDE, data_key="peer_subsystem", allow_none=True)
    r""" The peer_subsystem field of the nvme_subsystem_replication. """

    peer_svm = marshmallow_fields.Nested("netapp_ontap.resources.svm_peer.SvmPeerSchema", unknown=EXCLUDE, data_key="peer_svm", allow_none=True)
    r""" The peer_svm field of the nvme_subsystem_replication. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state of the replication queue associated with this subsystem. If this subsystem is not in the replication queue, the state is reported as _ok_. If this subsystem is in the replication queue, but no errors have been encountered, the state is reported as _replicating_. If this subsystem is in the replication queue and the queue is blocked by an error, the state is reported as _error_. When in the _error_ state, additional context is provided by the `replication.error` property.


Valid choices:

* ok
* replicating
* error """

    @property
    def resource(self):
        return NvmeSubsystemReplication

    gettable_fields = [
        "error",
        "peer_subsystem",
        "peer_svm.links",
        "peer_svm.name",
        "peer_svm.uuid",
        "state",
    ]
    """error,peer_subsystem,peer_svm.links,peer_svm.name,peer_svm.uuid,state,"""

    patchable_fields = [
        "error",
        "peer_subsystem",
    ]
    """error,peer_subsystem,"""

    postable_fields = [
        "error",
        "peer_subsystem",
    ]
    """error,peer_subsystem,"""


class NvmeSubsystemReplication(Resource):

    _schema = NvmeSubsystemReplicationSchema
