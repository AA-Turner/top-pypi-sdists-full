r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeSubsystemHostRecords", "NvmeSubsystemHostRecordsSchema"]
__pdoc__ = {
    "NvmeSubsystemHostRecordsSchema.resource": False,
    "NvmeSubsystemHostRecordsSchema.opts": False,
    "NvmeSubsystemHostRecords": False,
}


class NvmeSubsystemHostRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeSubsystemHostRecords object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the nvme_subsystem_host_records. """

    dh_hmac_chap = marshmallow_fields.Nested("netapp_ontap.models.nvme_dh_hmac_chap_authentication.NvmeDhHmacChapAuthenticationSchema", unknown=EXCLUDE, data_key="dh_hmac_chap", allow_none=True)
    r""" A container for the configuration of NVMe in-band authentication using the DH-HMAC-CHAP protocol for a host. """

    io_queue = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_host_records_io_queue.NvmeSubsystemHostRecordsIoQueueSchema", unknown=EXCLUDE, data_key="io_queue", allow_none=True)
    r""" The properties of the submission queue used to submit I/O commands for execution by the NVMe controller. """

    nqn = marshmallow_fields.Str(data_key="nqn", allow_none=True)
    r""" The NVMe qualified name (NQN) used to identify the NVMe storage target. Not allowed in POST when the `records` property is used.


Example: nqn.1992-01.example.com:string """

    subsystem = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_host_records_subsystem.NvmeSubsystemHostRecordsSubsystemSchema", unknown=EXCLUDE, data_key="subsystem", allow_none=True)
    r""" The NVMe subsystem to which the NVMe host has been provisioned. """

    tls = marshmallow_fields.Nested("netapp_ontap.models.nvme_tcp_tls.NvmeTcpTlsSchema", unknown=EXCLUDE, data_key="tls", allow_none=True)
    r""" A container for the configuration for NVMe/TCP-TLS transport session for the host. """

    @property
    def resource(self):
        return NvmeSubsystemHostRecords

    gettable_fields = [
        "links",
        "dh_hmac_chap",
        "io_queue",
        "nqn",
        "subsystem",
        "tls",
    ]
    """links,dh_hmac_chap,io_queue,nqn,subsystem,tls,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "dh_hmac_chap",
        "nqn",
        "tls",
    ]
    """dh_hmac_chap,nqn,tls,"""


class NvmeSubsystemHostRecords(Resource):

    _schema = NvmeSubsystemHostRecordsSchema
