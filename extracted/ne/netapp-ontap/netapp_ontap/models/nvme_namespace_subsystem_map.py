r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeNamespaceSubsystemMap", "NvmeNamespaceSubsystemMapSchema"]
__pdoc__ = {
    "NvmeNamespaceSubsystemMapSchema.resource": False,
    "NvmeNamespaceSubsystemMapSchema.opts": False,
    "NvmeNamespaceSubsystemMap": False,
}


class NvmeNamespaceSubsystemMapSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeNamespaceSubsystemMap object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the nvme_namespace_subsystem_map. """

    anagrpid = marshmallow_fields.Str(data_key="anagrpid", allow_none=True)
    r""" The Asymmetric Namespace Access Group ID (ANAGRPID) of the NVMe namespace.<br/>
The format for an ANAGRPID is 8 hexadecimal digits (zero-filled) followed by a lower case "h".


Example: 00103050h """

    nsid = marshmallow_fields.Str(data_key="nsid", allow_none=True)
    r""" The NVMe namespace identifier. This is an identifier used by an NVMe controller to provide access to the NVMe namespace.<br/>
The format for an NVMe namespace identifier is 8 hexadecimal digits (zero-filled) followed by a lower case "h".


Example: 00000001h """

    subsystem = marshmallow_fields.Nested("netapp_ontap.models.nvme_namespace_subsystem_map_subsystem.NvmeNamespaceSubsystemMapSubsystemSchema", unknown=EXCLUDE, data_key="subsystem", allow_none=True)
    r""" The NVMe subsystem to which the NVMe namespace is mapped. """

    @property
    def resource(self):
        return NvmeNamespaceSubsystemMap

    gettable_fields = [
        "links",
        "anagrpid",
        "nsid",
        "subsystem",
    ]
    """links,anagrpid,nsid,subsystem,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "subsystem",
    ]
    """subsystem,"""


class NvmeNamespaceSubsystemMap(Resource):

    _schema = NvmeNamespaceSubsystemMapSchema
