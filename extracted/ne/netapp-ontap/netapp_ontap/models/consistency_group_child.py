r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupChild", "ConsistencyGroupChildSchema"]
__pdoc__ = {
    "ConsistencyGroupChildSchema.resource": False,
    "ConsistencyGroupChildSchema.opts": False,
    "ConsistencyGroupChild": False,
}


class ConsistencyGroupChildSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupChild object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the consistency_group_child. """

    tags = marshmallow_fields.List(marshmallow_fields.Str, data_key="_tags", allow_none=True)
    r""" Tags are an optional way to track the uses of a resource. Tag values must be formatted as key:value strings.

Example: ["team:csi","environment:test"] """

    application = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_application.ConsistencyGroupApplicationSchema", unknown=EXCLUDE, data_key="application", allow_none=True)
    r""" The application field of the consistency_group_child. """

    luns = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_lun.ConsistencyGroupLunSchema", unknown=EXCLUDE, allow_none=True), data_key="luns", allow_none=True)
    r""" The LUNs array can be used to create or modify LUNs in a consistency group on a new or existing volume that is a member of the consistency group. LUNs are considered members of a consistency group if they are located on a volume that is a member of the consistency group. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the consistency group. The consistency group name must be unique within an SVM.<br/> """

    namespaces = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_namespaces.ConsistencyGroupNamespacesSchema", unknown=EXCLUDE, allow_none=True), data_key="namespaces", allow_none=True)
    r""" An NVMe namespace is a collection of addressable logical blocks presented to hosts connected to the SVM using the NVMe over Fabrics protocol.
In ONTAP, an NVMe namespace is located within a volume. Optionally, it can be located within a qtree in a volume.<br/>
An NVMe namespace is created to a specified size using thin or thick provisioning as determined by the volume on which it is created. NVMe namespaces support being cloned. An NVMe namespace cannot be renamed, resized, or moved to a different volume. NVMe namespaces do not support the assignment of a QoS policy for performance management, but a QoS policy can be assigned to the volume containing the namespace. See the NVMe namespace object model to learn more about each of the properties supported by the NVMe namespace REST API.<br/>
An NVMe namespace must be mapped to an NVMe subsystem to grant access to the subsystem's hosts. Hosts can then access the NVMe namespace and perform I/O using the NVMe over Fabrics protocol. """

    parent_consistency_group = marshmallow_fields.Nested("netapp_ontap.resources.consistency_group.ConsistencyGroupSchema", unknown=EXCLUDE, data_key="parent_consistency_group", allow_none=True)
    r""" The parent_consistency_group field of the consistency_group_child. """

    provisioning_options = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_provisioning_options.ConsistencyGroupProvisioningOptionsSchema", unknown=EXCLUDE, data_key="provisioning_options", allow_none=True)
    r""" Options that are applied to the operation. """

    qos = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_qos.ConsistencyGroupQosSchema", unknown=EXCLUDE, data_key="qos", allow_none=True)
    r""" The qos field of the consistency_group_child. """

    restore_to = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_consistency_groups_restore_to.ConsistencyGroupConsistencyGroupsRestoreToSchema", unknown=EXCLUDE, data_key="restore_to", allow_none=True)
    r""" Use to restore a consistency group to a previous snapshot """

    snapshot_policy = marshmallow_fields.Nested("netapp_ontap.resources.snapshot_policy.SnapshotPolicySchema", unknown=EXCLUDE, data_key="snapshot_policy", allow_none=True)
    r""" The snapshot policy of the consistency group.<br/>
This is the dedicated consistency group snapshot policy, not an aggregation of the volume granular snapshot policy. """

    space = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_space.ConsistencyGroupSpaceSchema", unknown=EXCLUDE, data_key="space", allow_none=True)
    r""" The space field of the consistency_group_child. """

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", unknown=EXCLUDE, data_key="svm", allow_none=True)
    r""" The svm field of the consistency_group_child. """

    tiering = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_tiering.ConsistencyGroupTieringSchema", unknown=EXCLUDE, data_key="tiering", allow_none=True)
    r""" The tiering field of the consistency_group_child. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the consistency group. The UUID is generated by ONTAP when the consistency group is created.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    volumes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_volumes.ConsistencyGroupVolumesSchema", unknown=EXCLUDE, allow_none=True), data_key="volumes", allow_none=True)
    r""" A consistency group is a mutually exclusive aggregation of volumes or other consistency groups. A volume can only be associated with one direct parent consistency group.<br/>

The total number of volumes across all child consistency groups contained in a consistency group is constrained by the same limit. """

    @property
    def resource(self):
        return ConsistencyGroupChild

    gettable_fields = [
        "links",
        "tags",
        "application",
        "luns",
        "name",
        "namespaces",
        "parent_consistency_group.links",
        "parent_consistency_group.name",
        "parent_consistency_group.uuid",
        "qos",
        "snapshot_policy.links",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "space",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "tiering",
        "uuid",
        "volumes",
    ]
    """links,tags,application,luns,name,namespaces,parent_consistency_group.links,parent_consistency_group.name,parent_consistency_group.uuid,qos,snapshot_policy.links,snapshot_policy.name,snapshot_policy.uuid,space,svm.links,svm.name,svm.uuid,tiering,uuid,volumes,"""

    patchable_fields = [
        "tags",
        "application",
        "luns",
        "namespaces",
        "provisioning_options",
        "qos",
        "restore_to",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "volumes",
    ]
    """tags,application,luns,namespaces,provisioning_options,qos,restore_to,snapshot_policy.name,snapshot_policy.uuid,volumes,"""

    postable_fields = [
        "tags",
        "application",
        "luns",
        "name",
        "namespaces",
        "provisioning_options",
        "qos",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "svm.name",
        "svm.uuid",
        "tiering",
        "volumes",
    ]
    """tags,application,luns,name,namespaces,provisioning_options,qos,snapshot_policy.name,snapshot_policy.uuid,svm.name,svm.uuid,tiering,volumes,"""


class ConsistencyGroupChild(Resource):

    _schema = ConsistencyGroupChildSchema
