r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupResponseRecords", "ConsistencyGroupResponseRecordsSchema"]
__pdoc__ = {
    "ConsistencyGroupResponseRecordsSchema.resource": False,
    "ConsistencyGroupResponseRecordsSchema.opts": False,
    "ConsistencyGroupResponseRecords": False,
}


class ConsistencyGroupResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupResponseRecords object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the consistency_group_response_records. """

    tags = marshmallow_fields.List(marshmallow_fields.Str, data_key="_tags", allow_none=True)
    r""" Tags are an optional way to track the uses of a resource. Tag values must be formatted as key:value strings.

Example: ["team:csi","environment:test"] """

    application = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_application.ConsistencyGroupApplicationSchema", unknown=EXCLUDE, data_key="application", allow_none=True)
    r""" The application field of the consistency_group_response_records. """

    clone = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_clone.ConsistencyGroupCloneSchema", unknown=EXCLUDE, data_key="clone", allow_none=True)
    r""" The clone field of the consistency_group_response_records. """

    consistency_groups = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_child.ConsistencyGroupChildSchema", unknown=EXCLUDE, allow_none=True), data_key="consistency_groups", allow_none=True)
    r""" A consistency group is a mutually exclusive aggregation of volumes or other consistency groups. A consistency group can only be associated with one direct parent consistency group. """

    luns = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_lun.ConsistencyGroupLunSchema", unknown=EXCLUDE, allow_none=True), data_key="luns", allow_none=True)
    r""" The LUNs array can be used to create or modify LUNs in a consistency group on a new or existing volume that is a member of the consistency group. LUNs are considered members of a consistency group if they are located on a volume that is a member of the consistency group. """

    map_to = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_map_to.ConsistencyGroupMapToSchema", unknown=EXCLUDE, data_key="map_to", allow_none=True)
    r""" Specifies the igroup or subsystem to map the LUNs or namespaces within the consistency group. This parameter can only be used if all the storage objects within the consistency groups are either LUNs or namespaces. """

    metric = marshmallow_fields.Nested("netapp_ontap.resources.consistency_group_metrics.ConsistencyGroupMetricsSchema", unknown=EXCLUDE, data_key="metric", allow_none=True)
    r""" Performance and capacity numbers, such as, IOPS, latency, throughput, used space, and available space. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the consistency group. The consistency group name must be unique within an SVM.<br/> """

    namespaces = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_response_records_consistency_groups_namespaces.ConsistencyGroupResponseRecordsConsistencyGroupsNamespacesSchema", unknown=EXCLUDE, allow_none=True), data_key="namespaces", allow_none=True)
    r""" An NVMe namespace is a collection of addressable logical blocks presented to hosts connected to the SVM using the NVMe over Fabrics protocol.
In ONTAP, an NVMe namespace is located within a volume. Optionally, it can be located within a qtree in a volume.<br/>
An NVMe namespace is created to a specified size using thin or thick provisioning as determined by the volume on which it is created. NVMe namespaces support being cloned. An NVMe namespace cannot be renamed, resized, or moved to a different volume. NVMe namespaces do not support the assignment of a QoS policy for performance management, but a QoS policy can be assigned to the volume containing the namespace. See the NVMe namespace object model to learn more about each of the properties supported by the NVMe namespace REST API.<br/>
An NVMe namespace must be mapped to an NVMe subsystem to grant access to the subsystem's hosts. Hosts can then access the NVMe namespace and perform I/O using the NVMe over Fabrics protocol. """

    parent_consistency_group = marshmallow_fields.Nested("netapp_ontap.resources.consistency_group.ConsistencyGroupSchema", unknown=EXCLUDE, data_key="parent_consistency_group", allow_none=True)
    r""" The parent_consistency_group field of the consistency_group_response_records. """

    provisioning_options = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_provisioning_options.ConsistencyGroupProvisioningOptionsSchema", unknown=EXCLUDE, data_key="provisioning_options", allow_none=True)
    r""" Options that are applied to the operation. """

    qos = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_qos.ConsistencyGroupQosSchema", unknown=EXCLUDE, data_key="qos", allow_none=True)
    r""" The qos field of the consistency_group_response_records. """

    replicated = marshmallow_fields.Boolean(data_key="replicated", allow_none=True)
    r""" Indicates whether or not replication has been enabled on this consistency group. """

    replication_relationships = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_replication_relationships1.ConsistencyGroupReplicationRelationships1Schema", unknown=EXCLUDE, allow_none=True), data_key="replication_relationships", allow_none=True)
    r""" Indicates the SnapMirror relationship of this consistency group. """

    replication_source = marshmallow_fields.Boolean(data_key="replication_source", allow_none=True)
    r""" Since support for this field is to be removed in the next release, use replication_relationships.is_source instead. """

    restore_to = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_consistency_groups_restore_to.ConsistencyGroupConsistencyGroupsRestoreToSchema", unknown=EXCLUDE, data_key="restore_to", allow_none=True)
    r""" Use to restore a consistency group to a previous snapshot """

    snaplock = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_snaplock.ConsistencyGroupSnaplockSchema", unknown=EXCLUDE, data_key="snaplock", allow_none=True)
    r""" The snaplock field of the consistency_group_response_records. """

    snapshot_policy = marshmallow_fields.Nested("netapp_ontap.resources.snapshot_policy.SnapshotPolicySchema", unknown=EXCLUDE, data_key="snapshot_policy", allow_none=True)
    r""" The snapshot policy of the consistency group.<br/>
This is the dedicated consistency group snapshot policy, not an aggregation of the volume granular snapshot policy. """

    space = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_space.ConsistencyGroupSpaceSchema", unknown=EXCLUDE, data_key="space", allow_none=True)
    r""" The space field of the consistency_group_response_records. """

    statistics = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_statistics.ConsistencyGroupStatisticsSchema", unknown=EXCLUDE, data_key="statistics", allow_none=True)
    r""" These are raw performance and space numbers, such as, IOPS, latency, throughput, used space, and available space. These numbers are aggregated across all nodes in the cluster and increase with the uptime of the cluster. """

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", unknown=EXCLUDE, data_key="svm", allow_none=True)
    r""" The svm field of the consistency_group_response_records. """

    tiering = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_tiering.ConsistencyGroupTieringSchema", unknown=EXCLUDE, data_key="tiering", allow_none=True)
    r""" The tiering field of the consistency_group_response_records. """

    unmap_from = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_unmap_from.ConsistencyGroupUnmapFromSchema", unknown=EXCLUDE, data_key="unmap_from", allow_none=True)
    r""" Specify the igroup or subsystem within the consistency group from which the LUNs or namespaces will be unmapped. This parameter can only be used if all the storage objects within the consistency groups are either LUNs or namespaces. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the consistency group. The UUID is generated by ONTAP when the consistency group is created.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    vdisk_type = marshmallow_fields.Str(data_key="vdisk_type", allow_none=True)
    r""" Type of objects in the consistency group.

Valid choices:

* luns
* namespaces
* mixed """

    volumes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_response_records_consistency_groups_volumes.ConsistencyGroupResponseRecordsConsistencyGroupsVolumesSchema", unknown=EXCLUDE, allow_none=True), data_key="volumes", allow_none=True)
    r""" A consistency group is a mutually exclusive aggregation of volumes or other consistency groups. A volume can only be associated with one direct parent consistency group.<br/>

The total number of volumes across all child consistency groups contained in a consistency group is constrained by the same limit. """

    @property
    def resource(self):
        return ConsistencyGroupResponseRecords

    gettable_fields = [
        "links",
        "tags",
        "application",
        "clone",
        "consistency_groups",
        "luns",
        "metric",
        "name",
        "namespaces",
        "parent_consistency_group.links",
        "parent_consistency_group.name",
        "parent_consistency_group.uuid",
        "qos",
        "replicated",
        "replication_relationships",
        "replication_source",
        "snaplock",
        "snapshot_policy.links",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "space",
        "statistics",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "tiering",
        "uuid",
        "vdisk_type",
        "volumes",
    ]
    """links,tags,application,clone,consistency_groups,luns,metric,name,namespaces,parent_consistency_group.links,parent_consistency_group.name,parent_consistency_group.uuid,qos,replicated,replication_relationships,replication_source,snaplock,snapshot_policy.links,snapshot_policy.name,snapshot_policy.uuid,space,statistics,svm.links,svm.name,svm.uuid,tiering,uuid,vdisk_type,volumes,"""

    patchable_fields = [
        "tags",
        "application",
        "clone",
        "consistency_groups",
        "luns",
        "map_to",
        "namespaces",
        "provisioning_options",
        "qos",
        "restore_to",
        "snaplock",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "unmap_from",
        "vdisk_type",
        "volumes",
    ]
    """tags,application,clone,consistency_groups,luns,map_to,namespaces,provisioning_options,qos,restore_to,snaplock,snapshot_policy.name,snapshot_policy.uuid,unmap_from,vdisk_type,volumes,"""

    postable_fields = [
        "tags",
        "application",
        "clone",
        "consistency_groups",
        "luns",
        "name",
        "namespaces",
        "provisioning_options",
        "qos",
        "snaplock",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "svm.name",
        "svm.uuid",
        "tiering",
        "vdisk_type",
        "volumes",
    ]
    """tags,application,clone,consistency_groups,luns,name,namespaces,provisioning_options,qos,snaplock,snapshot_policy.name,snapshot_policy.uuid,svm.name,svm.uuid,tiering,vdisk_type,volumes,"""


class ConsistencyGroupResponseRecords(Resource):

    _schema = ConsistencyGroupResponseRecordsSchema
