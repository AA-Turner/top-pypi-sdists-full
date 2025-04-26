r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LunConvertNamespace", "LunConvertNamespaceSchema"]
__pdoc__ = {
    "LunConvertNamespaceSchema.resource": False,
    "LunConvertNamespaceSchema.opts": False,
    "LunConvertNamespace": False,
}


class LunConvertNamespaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LunConvertNamespace object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the source NVMe namespace. Valid in POST.
### Platform Specifics

* **Unified ONTAP**:
An NVMe namespace is located within a volume. Optionally, it can be located within a qtree in a volume.<br/>
NVMe namespace names are paths of the form "/vol/\<volume>[/\<qtree>]/\<NVMe namespace>" where the qtree name is optional.

* **ASA r2**:
NVMe namespace names are simple names that share a namespace with LUNs within the same SVM. The name must begin with a letter or "\_" and contain only "\_" and alphanumeric characters. In specific cases, an optional snapshot-name can be used of the form "\<name>[@\<snapshot-name>]". The snapshot name must not begin or end with whitespace.


Example: /vol/volume1/namespace1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the source NVMe namespace. Valid in POST.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return LunConvertNamespace

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


class LunConvertNamespace(Resource):

    _schema = LunConvertNamespaceSchema
