r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ContainerResponseRecordsVolumes", "ContainerResponseRecordsVolumesSchema"]
__pdoc__ = {
    "ContainerResponseRecordsVolumesSchema.resource": False,
    "ContainerResponseRecordsVolumesSchema.opts": False,
    "ContainerResponseRecordsVolumes": False,
}


class ContainerResponseRecordsVolumesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ContainerResponseRecordsVolumes object"""

    flexcache = marshmallow_fields.Nested("netapp_ontap.models.container_volumes_flexcache.ContainerVolumesFlexcacheSchema", unknown=EXCLUDE, data_key="flexcache", allow_none=True)
    r""" The FlexCache origin volume. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Volume name. The name of volume must start with an alphabetic character (a to z or A to Z) or an underscore (_). The name must be 197 or fewer characters in length for FlexGroup volumes, and 203 or fewer characters in length for all other types of volumes. Volume names must be unique within an SVM. Required on POST.

Example: vol_cs_dept """

    nas = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_nas.ConsistencyGroupNasSchema", unknown=EXCLUDE, data_key="nas", allow_none=True)
    r""" The nas field of the container_response_records_volumes. """

    qos = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_qos.ConsistencyGroupQosSchema", unknown=EXCLUDE, data_key="qos", allow_none=True)
    r""" The qos field of the container_response_records_volumes. """

    s3_bucket = marshmallow_fields.Nested("netapp_ontap.models.container_response_records_volumes_s3_bucket.ContainerResponseRecordsVolumesS3BucketSchema", unknown=EXCLUDE, data_key="s3_bucket", allow_none=True)
    r""" The S3 bucket """

    scale_out = marshmallow_fields.Boolean(data_key="scale_out", allow_none=True)
    r""" Denotes a Flexgroup. """

    snaplock = marshmallow_fields.Nested("netapp_ontap.models.container_volume_snaplock.ContainerVolumeSnaplockSchema", unknown=EXCLUDE, data_key="snaplock", allow_none=True)
    r""" The snaplock field of the container_response_records_volumes. """

    snapshot_locking_enabled = marshmallow_fields.Boolean(data_key="snapshot_locking_enabled", allow_none=True)
    r""" Specifies whether or not snapshot copy locking is enabled on the volume. """

    snapshot_policy = marshmallow_fields.Nested("netapp_ontap.resources.snapshot_policy.SnapshotPolicySchema", unknown=EXCLUDE, data_key="snapshot_policy", allow_none=True)
    r""" The snapshot_policy field of the container_response_records_volumes. """

    space = marshmallow_fields.Nested("netapp_ontap.models.container_volumes_space.ContainerVolumesSpaceSchema", unknown=EXCLUDE, data_key="space", allow_none=True)
    r""" The space field of the container_response_records_volumes. """

    @property
    def resource(self):
        return ContainerResponseRecordsVolumes

    gettable_fields = [
        "flexcache",
        "name",
        "nas",
        "s3_bucket",
        "snapshot_locking_enabled",
        "snapshot_policy.links",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
    ]
    """flexcache,name,nas,s3_bucket,snapshot_locking_enabled,snapshot_policy.links,snapshot_policy.name,snapshot_policy.uuid,"""

    patchable_fields = [
        "flexcache",
        "name",
        "nas",
        "s3_bucket",
        "snapshot_locking_enabled",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
    ]
    """flexcache,name,nas,s3_bucket,snapshot_locking_enabled,snapshot_policy.name,snapshot_policy.uuid,"""

    postable_fields = [
        "flexcache",
        "name",
        "nas",
        "qos",
        "s3_bucket",
        "scale_out",
        "snaplock",
        "snapshot_locking_enabled",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "space",
    ]
    """flexcache,name,nas,qos,s3_bucket,scale_out,snaplock,snapshot_locking_enabled,snapshot_policy.name,snapshot_policy.uuid,space,"""


class ContainerResponseRecordsVolumes(Resource):

    _schema = ContainerResponseRecordsVolumesSchema
