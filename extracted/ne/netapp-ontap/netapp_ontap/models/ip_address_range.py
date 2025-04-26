r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IpAddressRange", "IpAddressRangeSchema"]
__pdoc__ = {
    "IpAddressRangeSchema.resource": False,
    "IpAddressRangeSchema.opts": False,
    "IpAddressRange": False,
}


class IpAddressRangeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IpAddressRange object"""

    end = marshmallow_fields.Str(data_key="end", allow_none=True)
    r""" The end field of the ip_address_range. """

    family = marshmallow_fields.Str(data_key="family", allow_none=True)
    r""" The family field of the ip_address_range. """

    start = marshmallow_fields.Str(data_key="start", allow_none=True)
    r""" The start field of the ip_address_range. """

    @property
    def resource(self):
        return IpAddressRange

    gettable_fields = [
        "end",
        "family",
        "start",
    ]
    """end,family,start,"""

    patchable_fields = [
        "end",
        "family",
        "start",
    ]
    """end,family,start,"""

    postable_fields = [
        "end",
        "family",
        "start",
    ]
    """end,family,start,"""


class IpAddressRange(Resource):

    _schema = IpAddressRangeSchema
