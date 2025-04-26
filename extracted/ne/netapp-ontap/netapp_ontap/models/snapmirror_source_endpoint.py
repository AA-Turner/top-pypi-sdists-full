r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SnapmirrorSourceEndpoint", "SnapmirrorSourceEndpointSchema"]
__pdoc__ = {
    "SnapmirrorSourceEndpointSchema.resource": False,
    "SnapmirrorSourceEndpointSchema.opts": False,
    "SnapmirrorSourceEndpoint": False,
}


class SnapmirrorSourceEndpointSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnapmirrorSourceEndpoint object"""

    cluster = marshmallow_fields.Nested("netapp_ontap.resources.cluster.ClusterSchema", unknown=EXCLUDE, data_key="cluster", allow_none=True)
    r""" The cluster field of the snapmirror_source_endpoint. """

    consistency_group_volumes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.snapmirror_endpoint_consistency_group_volumes.SnapmirrorEndpointConsistencyGroupVolumesSchema", unknown=EXCLUDE, allow_none=True), data_key="consistency_group_volumes", allow_none=True)
    r""" This property specifies the list of FlexVol volumes or LUNs of a Consistency Group. Optional on the ASA r2 platform. Mandatory for all other platforms. """

    luns = marshmallow_fields.Nested("netapp_ontap.resources.lun.LunSchema", unknown=EXCLUDE, data_key="luns", allow_none=True)
    r""" The luns field of the snapmirror_source_endpoint. """

    path = marshmallow_fields.Str(data_key="path", allow_none=True)
    r""" ONTAP FlexVol/FlexGroup - svm1:volume1
ONTAP SVM               - svm1:
ONTAP Consistency Group - svm1:/cg/cg_name
ONTAP S3                - svm1:/bucket/bucket1
NON-ONTAP               - objstore1:/objstore


Example: svm1:volume1 """

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", unknown=EXCLUDE, data_key="svm", allow_none=True)
    r""" The svm field of the snapmirror_source_endpoint. """

    @property
    def resource(self):
        return SnapmirrorSourceEndpoint

    gettable_fields = [
        "cluster.links",
        "cluster.name",
        "cluster.uuid",
        "consistency_group_volumes",
        "luns.links",
        "luns.name",
        "luns.uuid",
        "path",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """cluster.links,cluster.name,cluster.uuid,consistency_group_volumes,luns.links,luns.name,luns.uuid,path,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "cluster.name",
        "cluster.uuid",
        "luns.name",
        "luns.uuid",
        "path",
    ]
    """cluster.name,cluster.uuid,luns.name,luns.uuid,path,"""

    postable_fields = [
        "cluster.name",
        "cluster.uuid",
        "consistency_group_volumes",
        "luns.name",
        "luns.uuid",
        "path",
    ]
    """cluster.name,cluster.uuid,consistency_group_volumes,luns.name,luns.uuid,path,"""


class SnapmirrorSourceEndpoint(Resource):

    _schema = SnapmirrorSourceEndpointSchema
