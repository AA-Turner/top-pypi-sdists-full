r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeNamespaceCloneSource", "NvmeNamespaceCloneSourceSchema"]
__pdoc__ = {
    "NvmeNamespaceCloneSourceSchema.resource": False,
    "NvmeNamespaceCloneSourceSchema.opts": False,
    "NvmeNamespaceCloneSource": False,
}


class NvmeNamespaceCloneSourceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeNamespaceCloneSource object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the clone source NVMe namespace.
### Platform Specifics

* **Unified ONTAP**:
An NVMe namespace is located within a volume. Optionally, it can be located within a qtree in a volume.<br/>
NVMe namespace names are paths of the form "/vol/\<volume>[/\<qtree>]/\<namespace>" where the qtree name is optional.<br/>
Valid in POST and PATCH.

* **ASA r2**:
This property is not supported. Cloning is supported through the /ap/storage/storage-units endpoint. See the [`POST /ap/storage/storage-units`](#/SAN/storage_unit_create) to learn more about cloning NVMe namespaces.


Example: /vol/volume1/namespace1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the clone source NVMe namespace.
### Platform Specifics

* **Unified ONTAP**:
Valid in POST and PATCH.

* **ASA r2**:
This property is not supported. Cloning is supported through the /ap/storage/storage-units endpoint. See the [`POST /ap/storage/storage-units`](#/SAN/storage_unit_create) to learn more about cloning NVMe namespaces.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return NvmeNamespaceCloneSource

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class NvmeNamespaceCloneSource(Resource):

    _schema = NvmeNamespaceCloneSourceSchema
