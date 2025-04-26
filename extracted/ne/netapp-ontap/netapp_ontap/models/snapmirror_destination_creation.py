r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SnapmirrorDestinationCreation", "SnapmirrorDestinationCreationSchema"]
__pdoc__ = {
    "SnapmirrorDestinationCreationSchema.resource": False,
    "SnapmirrorDestinationCreationSchema.opts": False,
    "SnapmirrorDestinationCreation": False,
}


class SnapmirrorDestinationCreationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnapmirrorDestinationCreation object"""

    bucket_retention = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_retention.S3BucketRetentionSchema", unknown=EXCLUDE, data_key="bucket_retention", allow_none=True)
    r""" Information about the retention-mode and default-retention-period configured on the bucket. """

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Optional property to create the destination endpoint when establishing a SnapMirror relationship. It is assumed to be "false" if no other property is set and assumed to be "true" if any other property is set. """

    size = Size(data_key="size", allow_none=True)
    r""" Optional property to specify the size of destination endpoint in bytes. This property is applicable only to ONTAP S3 Bucket endpoints. The minimum size for S3 bucket is 80MB and maximum size is 64TB. If not specified, system will create destination with default size of 800GB. """

    snapshot_locking_enabled = marshmallow_fields.Boolean(data_key="snapshot_locking_enabled", allow_none=True)
    r""" Optional property to create the destination endpoint with snapshot locking enabled when establishing a SnapMirror relationship. This property is applicable to FlexVol volumes and FlexGroup volumes. """

    storage_service = marshmallow_fields.Nested("netapp_ontap.models.snapmirror_destination_creation_storage_service.SnapmirrorDestinationCreationStorageServiceSchema", unknown=EXCLUDE, data_key="storage_service", allow_none=True)
    r""" The storage_service field of the snapmirror_destination_creation. """

    tiering = marshmallow_fields.Nested("netapp_ontap.models.snapmirror_destination_creation_tiering.SnapmirrorDestinationCreationTieringSchema", unknown=EXCLUDE, data_key="tiering", allow_none=True)
    r""" The tiering field of the snapmirror_destination_creation. """

    @property
    def resource(self):
        return SnapmirrorDestinationCreation

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "bucket_retention",
        "enabled",
        "size",
        "snapshot_locking_enabled",
        "storage_service",
        "tiering",
    ]
    """bucket_retention,enabled,size,snapshot_locking_enabled,storage_service,tiering,"""


class SnapmirrorDestinationCreation(Resource):

    _schema = SnapmirrorDestinationCreationSchema
