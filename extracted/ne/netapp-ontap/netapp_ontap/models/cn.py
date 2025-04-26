r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Cn", "CnSchema"]
__pdoc__ = {
    "CnSchema.resource": False,
    "CnSchema.opts": False,
    "Cn": False,
}


class CnSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Cn object"""

    group = marshmallow_fields.Str(data_key="group", allow_none=True)
    r""" RFC 2256 cn attribute used by RFC 2307 when working with groups.

Example: cn """

    netgroup = marshmallow_fields.Str(data_key="netgroup", allow_none=True)
    r""" RFC 2256 cn attribute used by RFC 2307 when working with netgroups.

Example: name """

    @property
    def resource(self):
        return Cn

    gettable_fields = [
        "group",
        "netgroup",
    ]
    """group,netgroup,"""

    patchable_fields = [
        "group",
        "netgroup",
    ]
    """group,netgroup,"""

    postable_fields = [
        "group",
        "netgroup",
    ]
    """group,netgroup,"""


class Cn(Resource):

    _schema = CnSchema
