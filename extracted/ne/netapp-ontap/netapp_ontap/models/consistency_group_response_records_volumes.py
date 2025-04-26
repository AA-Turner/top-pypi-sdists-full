r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupResponseRecordsVolumes", "ConsistencyGroupResponseRecordsVolumesSchema"]
__pdoc__ = {
    "ConsistencyGroupResponseRecordsVolumesSchema.resource": False,
    "ConsistencyGroupResponseRecordsVolumesSchema.opts": False,
    "ConsistencyGroupResponseRecordsVolumes": False,
}


class ConsistencyGroupResponseRecordsVolumesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupResponseRecordsVolumes object"""

    comment = marshmallow_fields.Str(data_key="comment", allow_none=True)
    r""" A comment for the volume. Valid in POST or PATCH. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Volume name. The name of volume must start with an alphabetic character (a to z or A to Z) or an underscore (_). The name must be 197 or fewer characters in length for FlexGroup volumes, and 203 or fewer characters in length for all other types of volumes. Volume names must be unique within an SVM. Required on POST.

Example: vol_cs_dept """

    nas = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_nas.ConsistencyGroupNasSchema", unknown=EXCLUDE, data_key="nas", allow_none=True)
    r""" The nas field of the consistency_group_response_records_volumes. """

    provisioning_options = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_volume_provisioning_options.ConsistencyGroupVolumeProvisioningOptionsSchema", unknown=EXCLUDE, data_key="provisioning_options", allow_none=True)
    r""" Options that are applied to the operation. """

    qos = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_qos.ConsistencyGroupQosSchema", unknown=EXCLUDE, data_key="qos", allow_none=True)
    r""" The qos field of the consistency_group_response_records_volumes. """

    snapshot_policy = marshmallow_fields.Nested("netapp_ontap.resources.snapshot_policy.SnapshotPolicySchema", unknown=EXCLUDE, data_key="snapshot_policy", allow_none=True)
    r""" The snapshot policy for this volume. """

    space = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_volume_space.ConsistencyGroupVolumeSpaceSchema", unknown=EXCLUDE, data_key="space", allow_none=True)
    r""" The space field of the consistency_group_response_records_volumes. """

    tiering = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_tiering.ConsistencyGroupTieringSchema", unknown=EXCLUDE, data_key="tiering", allow_none=True)
    r""" The tiering field of the consistency_group_response_records_volumes. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Unique identifier for the volume. This corresponds to the instance-uuid that is exposed in the CLI and ONTAPI. It does not change due to a volume move.

Example: 028baa66-41bd-11e9-81d5-00a0986138f7 """

    @property
    def resource(self):
        return ConsistencyGroupResponseRecordsVolumes

    gettable_fields = [
        "comment",
        "name",
        "nas",
        "qos",
        "snapshot_policy.links",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "space",
        "tiering",
        "uuid",
    ]
    """comment,name,nas,qos,snapshot_policy.links,snapshot_policy.name,snapshot_policy.uuid,space,tiering,uuid,"""

    patchable_fields = [
        "comment",
        "name",
        "nas",
        "provisioning_options",
        "qos",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "space",
        "tiering",
    ]
    """comment,name,nas,provisioning_options,qos,snapshot_policy.name,snapshot_policy.uuid,space,tiering,"""

    postable_fields = [
        "comment",
        "name",
        "nas",
        "provisioning_options",
        "qos",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "space",
        "tiering",
    ]
    """comment,name,nas,provisioning_options,qos,snapshot_policy.name,snapshot_policy.uuid,space,tiering,"""


class ConsistencyGroupResponseRecordsVolumes(Resource):

    _schema = ConsistencyGroupResponseRecordsVolumesSchema
