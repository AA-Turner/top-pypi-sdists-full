r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeNamespaceClone", "NvmeNamespaceCloneSchema"]
__pdoc__ = {
    "NvmeNamespaceCloneSchema.resource": False,
    "NvmeNamespaceCloneSchema.opts": False,
    "NvmeNamespaceClone": False,
}


class NvmeNamespaceCloneSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeNamespaceClone object"""

    source = marshmallow_fields.Nested("netapp_ontap.models.nvme_namespace_clone_source.NvmeNamespaceCloneSourceSchema", unknown=EXCLUDE, data_key="source", allow_none=True)
    r""" The source NVMe namespace for a namespace clone operation. This can be specified using property `clone.source.uuid` or `clone.source.name`. If both properties are supplied, they must refer to the same namespace.<br/>
Valid in POST to create a new NVMe namespace as a clone of the source.<br/>
Valid in PATCH to overwrite an existing NVMe namespace's data as a clone of another. """

    @property
    def resource(self):
        return NvmeNamespaceClone

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
        "source",
    ]
    """source,"""

    postable_fields = [
        "source",
    ]
    """source,"""


class NvmeNamespaceClone(Resource):

    _schema = NvmeNamespaceCloneSchema
