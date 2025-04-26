r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupSnapshotResponseRecords", "ConsistencyGroupSnapshotResponseRecordsSchema"]
__pdoc__ = {
    "ConsistencyGroupSnapshotResponseRecordsSchema.resource": False,
    "ConsistencyGroupSnapshotResponseRecordsSchema.opts": False,
    "ConsistencyGroupSnapshotResponseRecords": False,
}


class ConsistencyGroupSnapshotResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupSnapshotResponseRecords object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the consistency_group_snapshot_response_records. """

    comment = marshmallow_fields.Str(data_key="comment", allow_none=True)
    r""" Comment for the snapshot.


Example: My snapshot comment """

    consistency_group = marshmallow_fields.Nested("netapp_ontap.resources.consistency_group.ConsistencyGroupSchema", unknown=EXCLUDE, data_key="consistency_group", allow_none=True)
    r""" The consistency_group field of the consistency_group_snapshot_response_records. """

    consistency_type = marshmallow_fields.Str(data_key="consistency_type", allow_none=True)
    r""" Consistency type. This is for categorization purposes only. A snapshot should not be set to 'application consistent' unless the host application is quiesced for the snapshot. Valid in POST.


Valid choices:

* crash
* application """

    create_time = ImpreciseDateTime(data_key="create_time", allow_none=True)
    r""" Time the snapshot copy was created


Example: 2020-10-25T11:20:00.000+0000 """

    is_partial = marshmallow_fields.Boolean(data_key="is_partial", allow_none=True)
    r""" Indicates whether the snapshot taken is partial or not.


Example: false """

    luns = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_snapshot_luns.ConsistencyGroupSnapshotLunsSchema", unknown=EXCLUDE, allow_none=True), data_key="luns", allow_none=True)
    r""" The list of LUNs in this snapshot. """

    missing_luns = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.lun.LunSchema", unknown=EXCLUDE, allow_none=True), data_key="missing_luns", allow_none=True)
    r""" List of LUNs that are not in the snapshot. """

    missing_namespaces = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_snapshot_missing_namespaces.ConsistencyGroupSnapshotMissingNamespacesSchema", unknown=EXCLUDE, allow_none=True), data_key="missing_namespaces", allow_none=True)
    r""" List of NVMe namespaces that are not in the snapshot. """

    missing_volumes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", unknown=EXCLUDE, allow_none=True), data_key="missing_volumes", allow_none=True)
    r""" List of volumes which are not in the snapshot. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the snapshot. """

    namespaces = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_snapshot_missing_namespaces.ConsistencyGroupSnapshotMissingNamespacesSchema", unknown=EXCLUDE, allow_none=True), data_key="namespaces", allow_none=True)
    r""" The list of NVMe namespaces in this snapshot. """

    reclaimable_space = Size(data_key="reclaimable_space", allow_none=True)
    r""" Space reclaimed when the snapshot is deleted, in bytes. """

    restore_size = Size(data_key="restore_size", allow_none=True)
    r""" Size of the consistency group if this snapshot is restored.

Example: 4096 """

    snaplock = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_snapshot_snaplock.ConsistencyGroupSnapshotSnaplockSchema", unknown=EXCLUDE, data_key="snaplock", allow_none=True)
    r""" SnapLock Snapshot attributes. """

    snapmirror_label = marshmallow_fields.Str(data_key="snapmirror_label", allow_none=True)
    r""" Snapmirror Label for the snapshot.


Example: sm_label """

    snapshot_volumes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_volume_snapshot.ConsistencyGroupVolumeSnapshotSchema", unknown=EXCLUDE, allow_none=True), data_key="snapshot_volumes", allow_none=True)
    r""" List of volume and snapshot identifiers for each volume in the snapshot. """

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", unknown=EXCLUDE, data_key="svm", allow_none=True)
    r""" The SVM in which the consistency group is located. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the snapshot. The UUID is generated
by ONTAP when the snapshot is created.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    write_fence = marshmallow_fields.Boolean(data_key="write_fence", allow_none=True)
    r""" Specifies whether a write fence will be taken when creating the snapshot. The default is false if there is only one volume in the consistency group, otherwise the default is true. """

    @property
    def resource(self):
        return ConsistencyGroupSnapshotResponseRecords

    gettable_fields = [
        "links",
        "comment",
        "consistency_group.links",
        "consistency_group.name",
        "consistency_group.uuid",
        "consistency_type",
        "create_time",
        "is_partial",
        "luns.links",
        "luns.name",
        "luns.uuid",
        "missing_luns",
        "missing_namespaces.links",
        "missing_namespaces.name",
        "missing_namespaces.uuid",
        "missing_volumes",
        "name",
        "namespaces.links",
        "namespaces.name",
        "namespaces.uuid",
        "reclaimable_space",
        "restore_size",
        "snaplock",
        "snapmirror_label",
        "snapshot_volumes",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
        "write_fence",
    ]
    """links,comment,consistency_group.links,consistency_group.name,consistency_group.uuid,consistency_type,create_time,is_partial,luns.links,luns.name,luns.uuid,missing_luns,missing_namespaces.links,missing_namespaces.name,missing_namespaces.uuid,missing_volumes,name,namespaces.links,namespaces.name,namespaces.uuid,reclaimable_space,restore_size,snaplock,snapmirror_label,snapshot_volumes,svm.links,svm.name,svm.uuid,uuid,write_fence,"""

    patchable_fields = [
        "consistency_type",
        "name",
        "snaplock",
        "svm.name",
        "svm.uuid",
        "write_fence",
    ]
    """consistency_type,name,snaplock,svm.name,svm.uuid,write_fence,"""

    postable_fields = [
        "comment",
        "consistency_type",
        "name",
        "snaplock",
        "snapmirror_label",
        "svm.name",
        "svm.uuid",
        "write_fence",
    ]
    """comment,consistency_type,name,snaplock,snapmirror_label,svm.name,svm.uuid,write_fence,"""


class ConsistencyGroupSnapshotResponseRecords(Resource):

    _schema = ConsistencyGroupSnapshotResponseRecordsSchema
