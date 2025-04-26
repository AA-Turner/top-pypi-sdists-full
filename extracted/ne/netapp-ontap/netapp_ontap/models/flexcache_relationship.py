r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FlexcacheRelationship", "FlexcacheRelationshipSchema"]
__pdoc__ = {
    "FlexcacheRelationshipSchema.resource": False,
    "FlexcacheRelationshipSchema.opts": False,
    "FlexcacheRelationship": False,
}


class FlexcacheRelationshipSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FlexcacheRelationship object"""

    cluster = marshmallow_fields.Nested("netapp_ontap.resources.cluster.ClusterSchema", unknown=EXCLUDE, data_key="cluster", allow_none=True)
    r""" The cluster field of the flexcache_relationship. """

    create_time = ImpreciseDateTime(data_key="create_time", allow_none=True)
    r""" Creation time of the relationship.

Example: 2018-06-04T19:00:00.000+0000 """

    ip_address = marshmallow_fields.Str(data_key="ip_address", allow_none=True)
    r""" Cluster management IP of the remote cluster.

Example: 10.10.10.7 """

    size = Size(data_key="size", allow_none=True)
    r""" Size of the remote volume. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Volume state

Valid choices:

* error
* mixed
* offline
* online """

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", unknown=EXCLUDE, data_key="svm", allow_none=True)
    r""" The svm field of the flexcache_relationship. """

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", unknown=EXCLUDE, data_key="volume", allow_none=True)
    r""" The volume field of the flexcache_relationship. """

    @property
    def resource(self):
        return FlexcacheRelationship

    gettable_fields = [
        "cluster.links",
        "cluster.name",
        "cluster.uuid",
        "create_time",
        "ip_address",
        "size",
        "state",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """cluster.links,cluster.name,cluster.uuid,create_time,ip_address,size,state,svm.links,svm.name,svm.uuid,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "volume.name",
        "volume.uuid",
    ]
    """volume.name,volume.uuid,"""

    postable_fields = [
        "svm.name",
        "svm.uuid",
        "volume.name",
        "volume.uuid",
    ]
    """svm.name,svm.uuid,volume.name,volume.uuid,"""


class FlexcacheRelationship(Resource):

    _schema = FlexcacheRelationshipSchema
