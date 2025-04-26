r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IscsiCredentialsInitiatorAddress", "IscsiCredentialsInitiatorAddressSchema"]
__pdoc__ = {
    "IscsiCredentialsInitiatorAddressSchema.resource": False,
    "IscsiCredentialsInitiatorAddressSchema.opts": False,
    "IscsiCredentialsInitiatorAddress": False,
}


class IscsiCredentialsInitiatorAddressSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IscsiCredentialsInitiatorAddress object"""

    masks = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.ip_info.IpInfoSchema", unknown=EXCLUDE, allow_none=True), data_key="masks", allow_none=True)
    r""" IP information """

    ranges = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.ip_address_range.IpAddressRangeSchema", unknown=EXCLUDE, allow_none=True), data_key="ranges", allow_none=True)
    r""" IP address range """

    @property
    def resource(self):
        return IscsiCredentialsInitiatorAddress

    gettable_fields = [
        "masks",
        "ranges",
    ]
    """masks,ranges,"""

    patchable_fields = [
        "masks",
        "ranges",
    ]
    """masks,ranges,"""

    postable_fields = [
        "masks",
        "ranges",
    ]
    """masks,ranges,"""


class IscsiCredentialsInitiatorAddress(Resource):

    _schema = IscsiCredentialsInitiatorAddressSchema
