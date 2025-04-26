r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeNamespaceSubsystemMapSubsystemHosts", "NvmeNamespaceSubsystemMapSubsystemHostsSchema"]
__pdoc__ = {
    "NvmeNamespaceSubsystemMapSubsystemHostsSchema.resource": False,
    "NvmeNamespaceSubsystemMapSubsystemHostsSchema.opts": False,
    "NvmeNamespaceSubsystemMapSubsystemHosts": False,
}


class NvmeNamespaceSubsystemMapSubsystemHostsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeNamespaceSubsystemMapSubsystemHosts object"""

    dh_hmac_chap = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_nvme_host_dh_hmac_chap.ConsistencyGroupNvmeHostDhHmacChapSchema", unknown=EXCLUDE, data_key="dh_hmac_chap", allow_none=True)
    r""" A container for the configuration of NVMe in-band authentication using the DH-HMAC-CHAP protocol for a host. """

    nqn = marshmallow_fields.Str(data_key="nqn", allow_none=True)
    r""" The NVMe qualified name (NQN) used to identify the NVMe storage target.


Example: nqn.1992-01.example.com:string """

    priority = marshmallow_fields.Str(data_key="priority", allow_none=True)
    r""" The host priority setting allocates appropriate NVMe I/O queues (count and depth) for the host to submit I/O commands. Absence of this property in GET implies io_queue count and I/O queue depth are being used.


Valid choices:

* regular
* high """

    tls = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_nvme_host_tls.ConsistencyGroupNvmeHostTlsSchema", unknown=EXCLUDE, data_key="tls", allow_none=True)
    r""" A container for the configuration for NVMe/TCP-TLS transport session for the host. """

    @property
    def resource(self):
        return NvmeNamespaceSubsystemMapSubsystemHosts

    gettable_fields = [
        "dh_hmac_chap",
        "nqn",
        "priority",
        "tls",
    ]
    """dh_hmac_chap,nqn,priority,tls,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "dh_hmac_chap",
        "nqn",
        "priority",
        "tls",
    ]
    """dh_hmac_chap,nqn,priority,tls,"""


class NvmeNamespaceSubsystemMapSubsystemHosts(Resource):

    _schema = NvmeNamespaceSubsystemMapSubsystemHostsSchema
