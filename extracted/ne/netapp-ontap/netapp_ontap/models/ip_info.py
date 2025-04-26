r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IpInfo", "IpInfoSchema"]
__pdoc__ = {
    "IpInfoSchema.resource": False,
    "IpInfoSchema.opts": False,
    "IpInfo": False,
}


class IpInfoSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IpInfo object"""

    address = marshmallow_fields.Str(data_key="address", allow_none=True)
    r""" The address field of the ip_info. """

    family = marshmallow_fields.Str(data_key="family", allow_none=True)
    r""" The family field of the ip_info. """

    netmask = marshmallow_fields.Str(data_key="netmask", allow_none=True)
    r""" The netmask field of the ip_info. """

    @property
    def resource(self):
        return IpInfo

    gettable_fields = [
        "address",
        "family",
        "netmask",
    ]
    """address,family,netmask,"""

    patchable_fields = [
        "address",
        "family",
        "netmask",
    ]
    """address,family,netmask,"""

    postable_fields = [
        "address",
        "family",
        "netmask",
    ]
    """address,family,netmask,"""


class IpInfo(Resource):

    _schema = IpInfoSchema
