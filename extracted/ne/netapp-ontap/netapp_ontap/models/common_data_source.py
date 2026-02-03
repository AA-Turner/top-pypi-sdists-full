r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["CommonDataSource", "CommonDataSourceSchema"]
__pdoc__ = {
    "CommonDataSourceSchema.resource": False,
    "CommonDataSourceSchema.opts": False,
    "CommonDataSource": False,
}

class CommonDataSourceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CommonDataSource object"""

    cluster = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.cluster", "ClusterSchema"),
                unknown=EXCLUDE,
                data_key="cluster",
                allow_none=True
            )
    r""" The cluster field of the common_data_source. """

    is_remote = marshmallow_fields.Boolean(data_key="is_remote", allow_none=True)
    r""" The property that specifies if the data source is local or remote. Required in a POST request. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the volume or bucket, whether it is local or remote storage.

Example: workspace """

    peer_svm = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.svm", "SvmSchema"),
                unknown=EXCLUDE,
                data_key="peer_svm",
                allow_none=True
            )
    r""" The peer_svm field of the common_data_source. """

    svm = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.svm", "SvmSchema"),
                unknown=EXCLUDE,
                data_key="svm",
                allow_none=True
            )
    r""" The svm field of the common_data_source. """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The type field of the common_data_source. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of a volume or bucket, whether it is local or remote storage. Required in a POST request.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return CommonDataSource

    gettable_fields = [
        "cluster.links",
        "cluster.name",
        "cluster.uuid",
        "is_remote",
        "name",
        "peer_svm.links",
        "peer_svm.name",
        "peer_svm.uuid",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "type",
        "uuid",
    ]
    """cluster.links,cluster.name,cluster.uuid,is_remote,name,peer_svm.links,peer_svm.name,peer_svm.uuid,svm.links,svm.name,svm.uuid,type,uuid,"""

    patchable_fields = [
        "cluster.name",
        "cluster.uuid",
        "is_remote",
        "name",
        "peer_svm.name",
        "peer_svm.uuid",
        "svm.name",
        "svm.uuid",
        "type",
        "uuid",
    ]
    """cluster.name,cluster.uuid,is_remote,name,peer_svm.name,peer_svm.uuid,svm.name,svm.uuid,type,uuid,"""

    postable_fields = [
        "cluster.name",
        "cluster.uuid",
        "is_remote",
        "name",
        "peer_svm.name",
        "peer_svm.uuid",
        "svm.name",
        "svm.uuid",
        "type",
        "uuid",
    ]
    """cluster.name,cluster.uuid,is_remote,name,peer_svm.name,peer_svm.uuid,svm.name,svm.uuid,type,uuid,"""


class CommonDataSource(Resource):

    _schema = CommonDataSourceSchema
