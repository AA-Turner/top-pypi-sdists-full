r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LunProvisioningOptions", "LunProvisioningOptionsSchema"]
__pdoc__ = {
    "LunProvisioningOptionsSchema.resource": False,
    "LunProvisioningOptionsSchema.opts": False,
    "LunProvisioningOptions": False,
}


class LunProvisioningOptionsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LunProvisioningOptions object"""

    auto = marshmallow_fields.Boolean(data_key="auto", allow_none=True)
    r""" If the volume specified in the request does not exist, automatically provision one of appropriate size. If the volume does exist, resize it to accommodate the new LUN.<br/>
This property is only supported on Unified ONTAP.<br/>
The following behavior is different from a traditional POST request:

* The operation is asynchronous.
* The `qos_policy` property is applied to the provisioned volume instead of the LUN. A default QoS policy is applied to the volume if one is not provided.
* The `provisioning_options.count` property is supported, provisioning _count_ LUNs on the volume using the specified properties.
* The `lun_maps` property is supported. If the specified initiator group does not exist, it is created. The LUN is mapped to this initiator group. If an initiator group is provisioned in this way, it is deleted after it is no longer mapped to any LUNs.
* The `clone`, `copy`, and `convert` properties are not supported.
* When performing `records` based operations, specifying this property in the query applies to the entire operation. Specifying it for an individual record within the request applies to only that record.
* Many other `provisioning_options` properties are supported to control the placement of the LUN and the properties of the volume containing the LUN. """

    count = Size(data_key="count", allow_none=True)
    r""" The number of LUNs to provision with these properties. Only POST requests based on `space.size` are supported. When provided, the name is considered a prefix, and a suffix of the form __&lt;N&gt;_ is generated where N is the next available numeric index, starting with 1. """

    qos_policy = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_qos_policy.ConsistencyGroupQosPolicySchema", unknown=EXCLUDE, data_key="qos_policy", allow_none=True)
    r""" When "min_throughput_iops", "min_throughput_mbps", "max_throughput_iops" or "max_throughput_mbps" attributes are specified, the storage object is assigned to an auto-generated QoS policy group. If the attributes are later modified, the auto-generated QoS policy-group attributes are modified. Attributes can be removed by specifying "0" and policy group by specifying "none". Upon deletion of the storage object or if the attributes are removed, then the QoS policy-group is also removed. """

    snapshot_policy = marshmallow_fields.Nested("netapp_ontap.resources.snapshot_policy.SnapshotPolicySchema", unknown=EXCLUDE, data_key="snapshot_policy", allow_none=True)
    r""" The snapshot policy for the volume provisioned to host the LUN. This property is only supported when the request provisions a new volume. """

    storage_service = marshmallow_fields.Nested("netapp_ontap.models.lun_provisioning_options_storage_service.LunProvisioningOptionsStorageServiceSchema", unknown=EXCLUDE, data_key="storage_service", allow_none=True)
    r""" Determines the placement of the volume provisioned to host the LUN. """

    tiering = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_tiering.ConsistencyGroupTieringSchema", unknown=EXCLUDE, data_key="tiering", allow_none=True)
    r""" The tiering field of the lun_provisioning_options. """

    use_mirrored_aggregates = marshmallow_fields.Boolean(data_key="use_mirrored_aggregates", allow_none=True)
    r""" Specifies whether mirrored aggregates are selected when provisioning the volume to host the LUN. Only mirrored aggregates are used if this parameter is set to _true_ and only unmirrored aggregates are used if this parameter is set to _false_. The default value is _true_ for a MetroCluster configuration and is _false_ for a non-MetroCluster configuration. """

    @property
    def resource(self):
        return LunProvisioningOptions

    gettable_fields = [
        "snapshot_policy.links",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "storage_service",
    ]
    """snapshot_policy.links,snapshot_policy.name,snapshot_policy.uuid,storage_service,"""

    patchable_fields = [
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "storage_service",
    ]
    """snapshot_policy.name,snapshot_policy.uuid,storage_service,"""

    postable_fields = [
        "auto",
        "count",
        "qos_policy",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "storage_service",
        "tiering",
        "use_mirrored_aggregates",
    ]
    """auto,count,qos_policy,snapshot_policy.name,snapshot_policy.uuid,storage_service,tiering,use_mirrored_aggregates,"""


class LunProvisioningOptions(Resource):

    _schema = LunProvisioningOptionsSchema
