r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupSnapshotResponseRecordsMissingNamespaces", "ConsistencyGroupSnapshotResponseRecordsMissingNamespacesSchema"]
__pdoc__ = {
    "ConsistencyGroupSnapshotResponseRecordsMissingNamespacesSchema.resource": False,
    "ConsistencyGroupSnapshotResponseRecordsMissingNamespacesSchema.opts": False,
    "ConsistencyGroupSnapshotResponseRecordsMissingNamespaces": False,
}


class ConsistencyGroupSnapshotResponseRecordsMissingNamespacesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupSnapshotResponseRecordsMissingNamespaces object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the consistency_group_snapshot_response_records_missing_namespaces. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of an NVMe namespace.
### Platform Specifics

* **Unified ONTAP**:
An NVMe namespace is located within a volume. Optionally, it can be located within a qtree in a volume.<br/>
NVMe namespace names are paths of the form "/vol/\<volume>[/\<qtree>]/\<namespace>" where the qtree name is optional.

* **ASA r2**:
NVMe namespace names are simple names that share a namespace with LUNs within the same SVM. The name must begin with a letter or "\_" and contain only "\_" and alphanumeric characters. In specific cases, an optional snapshot-name can be used of the form "\<name>[@\<snapshot-name>]". The snapshot name must not begin or end with whitespace.


Example: /vol/volume1/namespace1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the NVMe namespace.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return ConsistencyGroupSnapshotResponseRecordsMissingNamespaces

    gettable_fields = [
        "links",
        "name",
        "uuid",
    ]
    """links,name,uuid,"""

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


class ConsistencyGroupSnapshotResponseRecordsMissingNamespaces(Resource):

    _schema = ConsistencyGroupSnapshotResponseRecordsMissingNamespacesSchema
