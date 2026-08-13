r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["ContainerVolumes", "ContainerVolumesSchema"]
__pdoc__ = {
    "ContainerVolumesSchema.resource": False,
    "ContainerVolumesSchema.opts": False,
    "ContainerVolumes": False,
}

class ContainerVolumesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ContainerVolumes object"""

    comment = marshmallow_fields.Str(data_key="comment", allow_none=True)
    r""" A comment for the container volume. """

    encryption = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.container_volumes_encryption", "ContainerVolumesEncryptionSchema"),
                unknown=EXCLUDE,
                data_key="encryption",
                allow_none=True
            )
    r""" The encryption field of the container_volumes. """

    exclude_aggregates = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.resources.aggregate", "AggregateSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="exclude_aggregates",
                allow_none=True
                )
    r""" A list of aggregates to exclude when determining the placement of the volume. <br/> """

    flexcache = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.container_volumes_flexcache", "ContainerVolumesFlexcacheSchema"),
                unknown=EXCLUDE,
                data_key="flexcache",
                allow_none=True
            )
    r""" The FlexCache origin volume. """

    guarantee = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.container_volumes_guarantee", "ContainerVolumesGuaranteeSchema"),
                unknown=EXCLUDE,
                data_key="guarantee",
                allow_none=True
            )
    r""" The guarantee field of the container_volumes. """

    is_s3_arbitrary_part_size_enabled = marshmallow_fields.Boolean(data_key="is_s3_arbitrary_part_size_enabled", allow_none=True)
    r""" Specifies whether the volume should allow Amazon S3 multipart uploads with arbitrary part lengths. This is only supported for FlexGroup volumes with advanced granular data. The default value is `false`. When set to `true`, it cannot be reverted to `false`. Clusters with any volumes where this is `true` cannot be reverted to a release that does not support this feature. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Volume name. The name of volume must start with an alphabetic character (a to z or A to Z) or an underscore (_). The name must be 197 or fewer characters in length for FlexGroup volumes, and 203 or fewer characters in length for all other types of volumes. Volume names must be unique within an SVM. Required on POST.

Example: vol_cs_dept """

    nas = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.consistency_group_nas", "ConsistencyGroupNasSchema"),
                unknown=EXCLUDE,
                data_key="nas",
                allow_none=True
            )
    r""" The nas field of the container_volumes. """

    qos = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.consistency_group_qos", "ConsistencyGroupQosSchema"),
                unknown=EXCLUDE,
                data_key="qos",
                allow_none=True
            )
    r""" The qos field of the container_volumes. """

    s3_bucket = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.container_volumes_s3_bucket", "ContainerVolumesS3BucketSchema"),
                unknown=EXCLUDE,
                data_key="s3_bucket",
                allow_none=True
            )
    r""" The S3 bucket """

    scale_out = marshmallow_fields.Boolean(data_key="scale_out", allow_none=True)
    r""" Denotes a Flexgroup. """

    smas_protection = marshmallow_fields.Str(data_key="smas_protection", allow_none=True)
    r""" Specifies whether the volume should be protected by SnapMirror active sync for NAS.

Valid choices:

* protected
* unprotected """

    snaplock = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.container_volume_snaplock", "ContainerVolumeSnaplockSchema"),
                unknown=EXCLUDE,
                data_key="snaplock",
                allow_none=True
            )
    r""" The snaplock field of the container_volumes. """

    snapshot_directory_access_enabled = marshmallow_fields.Boolean(data_key="snapshot_directory_access_enabled", allow_none=True)
    r""" If set to true, this field enables the visible ".snapshot" directory from the client. The ".snapshot" directory will be available in every directory on the volume. """

    snapshot_locking_enabled = marshmallow_fields.Boolean(data_key="snapshot_locking_enabled", allow_none=True)
    r""" Specifies whether or not snapshot copy locking is enabled on the volume. """

    snapshot_policy = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.snapshot_policy", "SnapshotPolicySchema"),
                unknown=EXCLUDE,
                data_key="snapshot_policy",
                allow_none=True
            )
    r""" The snapshot_policy field of the container_volumes. """

    space = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.container_volumes_space", "ContainerVolumesSpaceSchema"),
                unknown=EXCLUDE,
                data_key="space",
                allow_none=True
            )
    r""" The space field of the container_volumes. """

    storage_service = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.container_volumes_storage_service", "ContainerVolumesStorageServiceSchema"),
                unknown=EXCLUDE,
                data_key="storage_service",
                allow_none=True
            )
    r""" Determines the placement of the volume that is to be provisioned. """

    tiering = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.container_tiering", "ContainerTieringSchema"),
                unknown=EXCLUDE,
                data_key="tiering",
                allow_none=True
            )
    r""" The tiering field of the container_volumes. """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Type of the volume.<br>rw &dash; read-write volume.<br>dp &dash; data-protection volume.<br>

Valid choices:

* rw
* dp """

    use_mirrored_aggregates = marshmallow_fields.Boolean(data_key="use_mirrored_aggregates", allow_none=True)
    r""" Specifies whether mirrored aggregates are selected when provisioning the volume. Only mirrored aggregates are used if this parameter is set to _true_ and only unmirrored aggregates are used if this parameter is set to _false_. The default value is _true_ for a MetroCluster configuration and is _false_ for a non-MetroCluster configuration. """

    @property
    def resource(self):
        return ContainerVolumes

    gettable_fields = [
        "encryption",
        "exclude_aggregates.links",
        "exclude_aggregates.name",
        "exclude_aggregates.uuid",
        "flexcache",
        "is_s3_arbitrary_part_size_enabled",
        "name",
        "nas",
        "s3_bucket",
        "snapshot_directory_access_enabled",
        "snapshot_locking_enabled",
        "snapshot_policy.links",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "storage_service",
        "type",
    ]
    """encryption,exclude_aggregates.links,exclude_aggregates.name,exclude_aggregates.uuid,flexcache,is_s3_arbitrary_part_size_enabled,name,nas,s3_bucket,snapshot_directory_access_enabled,snapshot_locking_enabled,snapshot_policy.links,snapshot_policy.name,snapshot_policy.uuid,storage_service,type,"""

    patchable_fields = [
        "encryption",
        "exclude_aggregates.name",
        "exclude_aggregates.uuid",
        "flexcache",
        "is_s3_arbitrary_part_size_enabled",
        "name",
        "nas",
        "s3_bucket",
        "snapshot_directory_access_enabled",
        "snapshot_locking_enabled",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "storage_service",
    ]
    """encryption,exclude_aggregates.name,exclude_aggregates.uuid,flexcache,is_s3_arbitrary_part_size_enabled,name,nas,s3_bucket,snapshot_directory_access_enabled,snapshot_locking_enabled,snapshot_policy.name,snapshot_policy.uuid,storage_service,"""

    postable_fields = [
        "comment",
        "encryption",
        "exclude_aggregates.name",
        "exclude_aggregates.uuid",
        "flexcache",
        "guarantee",
        "is_s3_arbitrary_part_size_enabled",
        "name",
        "nas",
        "qos",
        "s3_bucket",
        "scale_out",
        "smas_protection",
        "snaplock",
        "snapshot_directory_access_enabled",
        "snapshot_locking_enabled",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "space",
        "storage_service",
        "tiering",
        "type",
        "use_mirrored_aggregates",
    ]
    """comment,encryption,exclude_aggregates.name,exclude_aggregates.uuid,flexcache,guarantee,is_s3_arbitrary_part_size_enabled,name,nas,qos,s3_bucket,scale_out,smas_protection,snaplock,snapshot_directory_access_enabled,snapshot_locking_enabled,snapshot_policy.name,snapshot_policy.uuid,space,storage_service,tiering,type,use_mirrored_aggregates,"""


class ContainerVolumes(Resource):

    _schema = ContainerVolumesSchema
