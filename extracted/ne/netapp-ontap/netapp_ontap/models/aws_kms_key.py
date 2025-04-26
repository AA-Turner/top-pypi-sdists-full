r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AwsKmsKey", "AwsKmsKeySchema"]
__pdoc__ = {
    "AwsKmsKeySchema.resource": False,
    "AwsKmsKeySchema.opts": False,
    "AwsKmsKey": False,
}


class AwsKmsKeySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AwsKmsKey object"""

    key_id = marshmallow_fields.Str(data_key="key_id", allow_none=True)
    r""" Key identifier of the AWS KMS key encryption key.

Example: key01 """

    @property
    def resource(self):
        return AwsKmsKey

    gettable_fields = [
        "key_id",
    ]
    """key_id,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "key_id",
    ]
    """key_id,"""


class AwsKmsKey(Resource):

    _schema = AwsKmsKeySchema
