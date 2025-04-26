r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeNamespaceConvertLun", "NvmeNamespaceConvertLunSchema"]
__pdoc__ = {
    "NvmeNamespaceConvertLunSchema.resource": False,
    "NvmeNamespaceConvertLunSchema.opts": False,
    "NvmeNamespaceConvertLun": False,
}


class NvmeNamespaceConvertLunSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeNamespaceConvertLun object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the source LUN. Valid in POST.
### Platform Specifics

* **Unified ONTAP**:
A LUN is located within a volume. Optionally, it can be located within a qtree in a volume.<br/>
LUN names are paths of the form "/vol/\<volume>[/\<qtree>]/\<lun>" where the qtree name is optional.

* **ASA r2**:
LUN names are simple names that share a namespace with NVMe namespaces within the same SVM. The name must begin with a letter or "\_" and contain only "\_" and alphanumeric characters. In specific cases, an optional snapshot-name can be used of the form "\<name>[@\<snapshot-name>]". The snapshot name must not begin or end with whitespace.


Example: /vol/volume1/lun1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the source LUN. Valid in POST.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return NvmeNamespaceConvertLun

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class NvmeNamespaceConvertLun(Resource):

    _schema = NvmeNamespaceConvertLunSchema
