r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterSpaceCloudStorage", "ClusterSpaceCloudStorageSchema"]
__pdoc__ = {
    "ClusterSpaceCloudStorageSchema.resource": False,
    "ClusterSpaceCloudStorageSchema.opts": False,
    "ClusterSpaceCloudStorage": False,
}


class ClusterSpaceCloudStorageSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterSpaceCloudStorage object"""

    used = Size(data_key="used", allow_none=True)
    r""" Total space used in cloud. """

    @property
    def resource(self):
        return ClusterSpaceCloudStorage

    gettable_fields = [
        "used",
    ]
    """used,"""

    patchable_fields = [
        "used",
    ]
    """used,"""

    postable_fields = [
        "used",
    ]
    """used,"""


class ClusterSpaceCloudStorage(Resource):

    _schema = ClusterSpaceCloudStorageSchema
