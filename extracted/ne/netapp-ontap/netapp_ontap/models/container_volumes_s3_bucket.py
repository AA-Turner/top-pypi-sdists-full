r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ContainerVolumesS3Bucket", "ContainerVolumesS3BucketSchema"]
__pdoc__ = {
    "ContainerVolumesS3BucketSchema.resource": False,
    "ContainerVolumesS3BucketSchema.opts": False,
    "ContainerVolumesS3Bucket": False,
}


class ContainerVolumesS3BucketSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ContainerVolumesS3Bucket object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Specifies the name of the bucket. Bucket name is a string that can only contain the following combination of ASCII-range alphanumeric characters 0-9, a-z, ".", and "-".

Example: bucket1 """

    nas_path = marshmallow_fields.Str(data_key="nas_path", allow_none=True)
    r""" Specifies the NAS path that corresponds with the NAS bucket.

Example: / """

    policy = marshmallow_fields.Nested("netapp_ontap.models.container_volumes_s3_bucket_policy.ContainerVolumesS3BucketPolicySchema", unknown=EXCLUDE, data_key="policy", allow_none=True)
    r""" A policy is an object associated with a bucket. It defines resource (bucket, folder, or object) permissions. These policies are evaluated when an S3 user makes a request by executing a specific command. The user must be part of the principal (user or group) specified in the policy. Permissions in the policies determine whether the request is allowed or denied. """

    @property
    def resource(self):
        return ContainerVolumesS3Bucket

    gettable_fields = [
        "nas_path",
        "policy",
    ]
    """nas_path,policy,"""

    patchable_fields = [
        "nas_path",
        "policy",
    ]
    """nas_path,policy,"""

    postable_fields = [
        "name",
        "nas_path",
        "policy",
    ]
    """name,nas_path,policy,"""


class ContainerVolumesS3Bucket(Resource):

    _schema = ContainerVolumesS3BucketSchema
