r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Nis", "NisSchema"]
__pdoc__ = {
    "NisSchema.resource": False,
    "NisSchema.opts": False,
    "Nis": False,
}


class NisSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Nis object"""

    mapentry = marshmallow_fields.Str(data_key="mapentry", allow_none=True)
    r""" RFC 2307 nisMapEntry attribute.

Example: msSFU30NisMapEntry """

    mapname = marshmallow_fields.Str(data_key="mapname", allow_none=True)
    r""" RFC 2307 nisMapName attribute.

Example: msSFU30NisMapName """

    netgroup = marshmallow_fields.Str(data_key="netgroup", allow_none=True)
    r""" RFC 2307 nisNetgroup object class.

Example: msSFU30NisNetGroup """

    netgroup_triple = marshmallow_fields.Str(data_key="netgroup_triple", allow_none=True)
    r""" RFC 2307 nisNetgroupTriple attribute.

Example: msSFU30MemberOfNisNetgroup """

    object = marshmallow_fields.Str(data_key="object", allow_none=True)
    r""" RFC 2307 nisObject object class.

Example: msSFU30NisObject """

    @property
    def resource(self):
        return Nis

    gettable_fields = [
        "mapentry",
        "mapname",
        "netgroup",
        "netgroup_triple",
        "object",
    ]
    """mapentry,mapname,netgroup,netgroup_triple,object,"""

    patchable_fields = [
        "mapentry",
        "mapname",
        "netgroup",
        "netgroup_triple",
        "object",
    ]
    """mapentry,mapname,netgroup,netgroup_triple,object,"""

    postable_fields = [
        "mapentry",
        "mapname",
        "netgroup",
        "netgroup_triple",
        "object",
    ]
    """mapentry,mapname,netgroup,netgroup_triple,object,"""


class Nis(Resource):

    _schema = NisSchema
