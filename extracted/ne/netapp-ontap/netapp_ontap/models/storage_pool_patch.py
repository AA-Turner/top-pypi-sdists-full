r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StoragePoolPatch", "StoragePoolPatchSchema"]
__pdoc__ = {
    "StoragePoolPatchSchema.resource": False,
    "StoragePoolPatchSchema.opts": False,
    "StoragePoolPatch": False,
}


class StoragePoolPatchSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StoragePoolPatch object"""

    job = marshmallow_fields.Nested("netapp_ontap.models.job_link.JobLinkSchema", unknown=EXCLUDE, data_key="job", allow_none=True)
    r""" The job field of the storage_pool_patch. """

    num_records = Size(data_key="num_records", allow_none=True)
    r""" Number of shared storage pools in the cluster.

Example: 1 """

    records = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.storage_pool.StoragePoolSchema", unknown=EXCLUDE, allow_none=True), data_key="records", allow_none=True)
    r""" The records field of the storage_pool_patch. """

    @property
    def resource(self):
        return StoragePoolPatch

    gettable_fields = [
        "job",
        "num_records",
        "records",
    ]
    """job,num_records,records,"""

    patchable_fields = [
        "job",
        "num_records",
        "records",
    ]
    """job,num_records,records,"""

    postable_fields = [
        "job",
        "num_records",
        "records",
    ]
    """job,num_records,records,"""


class StoragePoolPatch(Resource):

    _schema = StoragePoolPatchSchema
