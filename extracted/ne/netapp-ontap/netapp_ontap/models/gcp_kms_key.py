r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["GcpKmsKey", "GcpKmsKeySchema"]
__pdoc__ = {
    "GcpKmsKeySchema.resource": False,
    "GcpKmsKeySchema.opts": False,
    "GcpKmsKey": False,
}

class GcpKmsKeySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the GcpKmsKey object"""

    key_name = marshmallow_fields.Str(data_key="key_name", allow_none=True)
    r""" Google Cloud KMS key name.

Example: cryptokey1 """

    key_ring_location = marshmallow_fields.Str(data_key="key_ring_location", allow_none=True)
    r""" Google Cloud KMS key ring location.

Example: location1 """

    key_ring_name = marshmallow_fields.Str(data_key="key_ring_name", allow_none=True)
    r""" Google Cloud KMS key ring name.

Example: keyring1 """

    project_id = marshmallow_fields.Str(data_key="project_id", allow_none=True)
    r""" Google Cloud KMS project ID.

Example: project1 """

    @property
    def resource(self):
        return GcpKmsKey

    gettable_fields = [
        "key_name",
        "key_ring_location",
        "key_ring_name",
        "project_id",
    ]
    """key_name,key_ring_location,key_ring_name,project_id,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "key_name",
        "key_ring_location",
        "key_ring_name",
        "project_id",
    ]
    """key_name,key_ring_location,key_ring_name,project_id,"""


class GcpKmsKey(Resource):

    _schema = GcpKmsKeySchema
