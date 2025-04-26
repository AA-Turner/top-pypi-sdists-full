r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["BgpPeerGroupPeer", "BgpPeerGroupPeerSchema"]
__pdoc__ = {
    "BgpPeerGroupPeerSchema.resource": False,
    "BgpPeerGroupPeerSchema.opts": False,
    "BgpPeerGroupPeer": False,
}


class BgpPeerGroupPeerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the BgpPeerGroupPeer object"""

    address = marshmallow_fields.Str(data_key="address", allow_none=True)
    r""" Peer router address

Example: 10.10.10.7 """

    asn = Size(data_key="asn", allow_none=True)
    r""" Autonomous system number of peer """

    is_next_hop = marshmallow_fields.Boolean(data_key="is_next_hop", allow_none=True)
    r""" Use peer address as next hop. """

    md5_enabled = marshmallow_fields.Boolean(data_key="md5_enabled", allow_none=True)
    r""" Enable or disable TCP MD5 signatures per RFC 2385.

Example: true """

    md5_secret = marshmallow_fields.Str(data_key="md5_secret", allow_none=True)
    r""" The shared TCP MD5 secret key. This can either be given as a password or hexadecimal key.

Example: SECRET_WORD """

    @property
    def resource(self):
        return BgpPeerGroupPeer

    gettable_fields = [
        "address",
        "asn",
        "is_next_hop",
        "md5_enabled",
        "md5_secret",
    ]
    """address,asn,is_next_hop,md5_enabled,md5_secret,"""

    patchable_fields = [
        "address",
        "is_next_hop",
        "md5_enabled",
        "md5_secret",
    ]
    """address,is_next_hop,md5_enabled,md5_secret,"""

    postable_fields = [
        "address",
        "asn",
        "is_next_hop",
        "md5_enabled",
        "md5_secret",
    ]
    """address,asn,is_next_hop,md5_enabled,md5_secret,"""


class BgpPeerGroupPeer(Resource):

    _schema = BgpPeerGroupPeerSchema
