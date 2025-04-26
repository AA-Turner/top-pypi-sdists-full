r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Rfc2307", "Rfc2307Schema"]
__pdoc__ = {
    "Rfc2307Schema.resource": False,
    "Rfc2307Schema.opts": False,
    "Rfc2307": False,
}


class Rfc2307Schema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Rfc2307 object"""

    attribute = marshmallow_fields.Nested("netapp_ontap.models.rfc2307_attribute.Rfc2307AttributeSchema", unknown=EXCLUDE, data_key="attribute", allow_none=True)
    r""" The attribute field of the rfc2307. """

    cn = marshmallow_fields.Nested("netapp_ontap.models.cn.CnSchema", unknown=EXCLUDE, data_key="cn", allow_none=True)
    r""" The cn field of the rfc2307. """

    member = marshmallow_fields.Nested("netapp_ontap.models.member.MemberSchema", unknown=EXCLUDE, data_key="member", allow_none=True)
    r""" The member field of the rfc2307. """

    nis = marshmallow_fields.Nested("netapp_ontap.models.nis.NisSchema", unknown=EXCLUDE, data_key="nis", allow_none=True)
    r""" The nis field of the rfc2307. """

    posix = marshmallow_fields.Nested("netapp_ontap.models.posix.PosixSchema", unknown=EXCLUDE, data_key="posix", allow_none=True)
    r""" The posix field of the rfc2307. """

    @property
    def resource(self):
        return Rfc2307

    gettable_fields = [
        "attribute",
        "cn",
        "member",
        "nis",
        "posix",
    ]
    """attribute,cn,member,nis,posix,"""

    patchable_fields = [
        "attribute",
        "cn",
        "member",
        "nis",
        "posix",
    ]
    """attribute,cn,member,nis,posix,"""

    postable_fields = [
    ]
    """"""


class Rfc2307(Resource):

    _schema = Rfc2307Schema
