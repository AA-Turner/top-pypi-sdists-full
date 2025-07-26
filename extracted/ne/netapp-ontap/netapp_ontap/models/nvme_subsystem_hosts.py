r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeSubsystemHosts", "NvmeSubsystemHostsSchema"]
__pdoc__ = {
    "NvmeSubsystemHostsSchema.resource": False,
    "NvmeSubsystemHostsSchema.opts": False,
    "NvmeSubsystemHosts": False,
}


class NvmeSubsystemHostsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeSubsystemHosts object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the nvme_subsystem_hosts. """

    dh_hmac_chap = marshmallow_fields.Nested("netapp_ontap.models.nvme_dh_hmac_chap_authentication.NvmeDhHmacChapAuthenticationSchema", unknown=EXCLUDE, data_key="dh_hmac_chap", allow_none=True)
    r""" A container for the configuration of NVMe in-band authentication using the DH-HMAC-CHAP protocol for a host. """

    nqn = marshmallow_fields.Str(data_key="nqn", allow_none=True)
    r""" The NVMe qualified name (NQN) used to identify the NVMe storage target.


Example: nqn.1992-01.example.com:string """

    priority = marshmallow_fields.Str(data_key="priority", allow_none=True)
    r""" The host priority setting allocates appropriate NVMe I/O queues (count and depth) for the host to submit I/O commands. Absence of this property in GET implies user configured values of I/O queue count and I/O queue depth are being used.


Valid choices:

* regular
* high """

    proximity = marshmallow_fields.Nested("netapp_ontap.models.nvme_host_proximity.NvmeHostProximitySchema", unknown=EXCLUDE, data_key="proximity", allow_none=True)
    r""" Properties that define the SVMs to which the host is proximal. This information is used to properly report active optimized and active non-optimized network paths using an NVMe controller. If no configuration has been specified for the host, the sub-object is not present in GET requests.<br/>
These properties apply to all instances of the host in the NVMe subsystem in the SVM and its peers. """

    tls = marshmallow_fields.Nested("netapp_ontap.models.nvme_tcp_tls.NvmeTcpTlsSchema", unknown=EXCLUDE, data_key="tls", allow_none=True)
    r""" A container for the configuration for NVMe/TCP-TLS transport session for the host. """

    @property
    def resource(self):
        return NvmeSubsystemHosts

    gettable_fields = [
        "links",
        "dh_hmac_chap",
        "nqn",
        "priority",
        "proximity",
        "tls",
    ]
    """links,dh_hmac_chap,nqn,priority,proximity,tls,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "dh_hmac_chap",
        "nqn",
        "priority",
        "proximity",
        "tls",
    ]
    """dh_hmac_chap,nqn,priority,proximity,tls,"""


class NvmeSubsystemHosts(Resource):

    _schema = NvmeSubsystemHostsSchema
