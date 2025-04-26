r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["GcpKmsKey", "GcpKmsKeySchema"]
__pdoc__ = {
    "GcpKmsKeySchema.resource": False,
    "GcpKmsKeySchema.opts": False,
    "GcpKmsKey": False,
}


class GcpKmsKeySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the GcpKmsKey object"""

    key_name = marshmallow_fields.Str(data_key="key_name", allow_none=True)
    r""" Key identifier of the Google Cloud KMS key encryption key.

Example: cryptokey1 """

    @property
    def resource(self):
        return GcpKmsKey

    gettable_fields = [
        "key_name",
    ]
    """key_name,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "key_name",
    ]
    """key_name,"""


class GcpKmsKey(Resource):

    _schema = GcpKmsKeySchema
