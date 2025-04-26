r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupNamespaceSubsystemMap", "ConsistencyGroupNamespaceSubsystemMapSchema"]
__pdoc__ = {
    "ConsistencyGroupNamespaceSubsystemMapSchema.resource": False,
    "ConsistencyGroupNamespaceSubsystemMapSchema.opts": False,
    "ConsistencyGroupNamespaceSubsystemMap": False,
}


class ConsistencyGroupNamespaceSubsystemMapSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupNamespaceSubsystemMap object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the consistency_group_namespace_subsystem_map. """

    anagrpid = marshmallow_fields.Str(data_key="anagrpid", allow_none=True)
    r""" The Asymmetric Namespace Access Group ID (ANAGRPID) of the NVMe namespace.<br/>
The format for an ANAGRPID is 8 hexadecimal digits (zero-filled) followed by a lower case "h".<br/>
There is an added computational cost to retrieving this property's value. It is not populated for either a collection GET or an instance GET unless it is explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.


Example: 00103050h """

    nsid = marshmallow_fields.Str(data_key="nsid", allow_none=True)
    r""" The NVMe namespace identifier. This is an identifier used by an NVMe controller to provide access to the NVMe namespace.<br/>
The format for an NVMe namespace identifier is 8 hexadecimal digits (zero-filled) followed by a lower case "h".


Example: 00000001h """

    subsystem = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_nvme_subsystem.ConsistencyGroupNvmeSubsystemSchema", unknown=EXCLUDE, data_key="subsystem", allow_none=True)
    r""" The NVMe subsystem to which the NVMe namespace is mapped. """

    @property
    def resource(self):
        return ConsistencyGroupNamespaceSubsystemMap

    gettable_fields = [
        "links",
        "anagrpid",
        "nsid",
        "subsystem",
    ]
    """links,anagrpid,nsid,subsystem,"""

    patchable_fields = [
        "subsystem",
    ]
    """subsystem,"""

    postable_fields = [
        "subsystem",
    ]
    """subsystem,"""


class ConsistencyGroupNamespaceSubsystemMap(Resource):

    _schema = ConsistencyGroupNamespaceSubsystemMapSchema
