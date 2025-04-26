r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IgroupInitiatorsProximityPeerSvms", "IgroupInitiatorsProximityPeerSvmsSchema"]
__pdoc__ = {
    "IgroupInitiatorsProximityPeerSvmsSchema.resource": False,
    "IgroupInitiatorsProximityPeerSvmsSchema.opts": False,
    "IgroupInitiatorsProximityPeerSvms": False,
}


class IgroupInitiatorsProximityPeerSvmsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IgroupInitiatorsProximityPeerSvms object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the igroup_initiators_proximity_peer_svms. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The local name of the peer SVM. This name is unique among all local and peer SVMs.


Example: peer1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the SVM peer relationship. This is the UUID of the relationship, not the UUID of the peer SVM itself.


Example: 4204cf77-4c82-9bdb-5644-b5a841c097a9 """

    @property
    def resource(self):
        return IgroupInitiatorsProximityPeerSvms

    gettable_fields = [
        "links",
        "name",
        "uuid",
    ]
    """links,name,uuid,"""

    patchable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class IgroupInitiatorsProximityPeerSvms(Resource):

    _schema = IgroupInitiatorsProximityPeerSvmsSchema
