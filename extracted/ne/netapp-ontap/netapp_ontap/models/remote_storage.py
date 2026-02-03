r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["RemoteStorage", "RemoteStorageSchema"]
__pdoc__ = {
    "RemoteStorageSchema.resource": False,
    "RemoteStorageSchema.opts": False,
    "RemoteStorage": False,
}

class RemoteStorageSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the RemoteStorage object"""

    cluster = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.cluster", "ClusterSchema"),
                unknown=EXCLUDE,
                data_key="cluster",
                allow_none=True
            )
    r""" The cluster field of the remote_storage. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the remote storage.

Example: vol1 """

    svm = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.svm", "SvmSchema"),
                unknown=EXCLUDE,
                data_key="svm",
                allow_none=True
            )
    r""" The svm field of the remote_storage. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the remote storage volume or bucket. Required on POST requests.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return RemoteStorage

    gettable_fields = [
        "cluster.links",
        "cluster.name",
        "cluster.uuid",
        "name",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """cluster.links,cluster.name,cluster.uuid,name,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
        "cluster.name",
        "cluster.uuid",
        "name",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """cluster.name,cluster.uuid,name,svm.name,svm.uuid,uuid,"""

    postable_fields = [
        "cluster.name",
        "cluster.uuid",
        "name",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """cluster.name,cluster.uuid,name,svm.name,svm.uuid,uuid,"""


class RemoteStorage(Resource):

    _schema = RemoteStorageSchema
