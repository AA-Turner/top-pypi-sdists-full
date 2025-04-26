r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmNsswitch", "SvmNsswitchSchema"]
__pdoc__ = {
    "SvmNsswitchSchema.resource": False,
    "SvmNsswitchSchema.opts": False,
    "SvmNsswitch": False,
}


class SvmNsswitchSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmNsswitch object"""

    group = marshmallow_fields.List(marshmallow_fields.Str, data_key="group", allow_none=True)
    r""" Group sources """

    hosts = marshmallow_fields.List(marshmallow_fields.Str, data_key="hosts", allow_none=True)
    r""" Host sources """

    namemap = marshmallow_fields.List(marshmallow_fields.Str, data_key="namemap", allow_none=True)
    r""" NameMap sources """

    netgroup = marshmallow_fields.List(marshmallow_fields.Str, data_key="netgroup", allow_none=True)
    r""" NetGroup sources """

    passwd = marshmallow_fields.List(marshmallow_fields.Str, data_key="passwd", allow_none=True)
    r""" Password sources """

    @property
    def resource(self):
        return SvmNsswitch

    gettable_fields = [
        "group",
        "hosts",
        "namemap",
        "netgroup",
        "passwd",
    ]
    """group,hosts,namemap,netgroup,passwd,"""

    patchable_fields = [
        "group",
        "hosts",
        "namemap",
        "netgroup",
        "passwd",
    ]
    """group,hosts,namemap,netgroup,passwd,"""

    postable_fields = [
        "group",
        "hosts",
        "namemap",
        "netgroup",
        "passwd",
    ]
    """group,hosts,namemap,netgroup,passwd,"""


class SvmNsswitch(Resource):

    _schema = SvmNsswitchSchema
