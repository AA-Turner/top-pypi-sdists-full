r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeNamespaceSubsystemMapSubsystem", "NvmeNamespaceSubsystemMapSubsystemSchema"]
__pdoc__ = {
    "NvmeNamespaceSubsystemMapSubsystemSchema.resource": False,
    "NvmeNamespaceSubsystemMapSubsystemSchema.opts": False,
    "NvmeNamespaceSubsystemMapSubsystem": False,
}


class NvmeNamespaceSubsystemMapSubsystemSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeNamespaceSubsystemMapSubsystem object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the nvme_namespace_subsystem_map_subsystem. """

    comment = marshmallow_fields.Str(data_key="comment", allow_none=True)
    r""" A configurable comment for the NVMe subsystem. Optional in POST. """

    hosts = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_nvme_host.ConsistencyGroupNvmeHostSchema", unknown=EXCLUDE, allow_none=True), data_key="hosts", allow_none=True)
    r""" The NVMe hosts configured for access to the NVMe subsystem.
Optional in POST. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the NVMe subsystem. Once created, an NVMe subsystem cannot be renamed. Optional in POST.


Example: subsystem1 """

    os_type = marshmallow_fields.Str(data_key="os_type", allow_none=True)
    r""" The host operating system of the NVMe subsystem's hosts. Optional in POST.


Valid choices:

* aix
* linux
* vmware
* windows """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the NVMe subsystem.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return NvmeNamespaceSubsystemMapSubsystem

    gettable_fields = [
        "links",
        "comment",
        "hosts",
        "name",
        "os_type",
        "uuid",
    ]
    """links,comment,hosts,name,os_type,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "comment",
        "hosts",
        "name",
        "os_type",
        "uuid",
    ]
    """comment,hosts,name,os_type,uuid,"""


class NvmeNamespaceSubsystemMapSubsystem(Resource):

    _schema = NvmeNamespaceSubsystemMapSubsystemSchema
