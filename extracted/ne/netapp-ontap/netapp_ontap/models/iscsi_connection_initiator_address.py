r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IscsiConnectionInitiatorAddress", "IscsiConnectionInitiatorAddressSchema"]
__pdoc__ = {
    "IscsiConnectionInitiatorAddressSchema.resource": False,
    "IscsiConnectionInitiatorAddressSchema.opts": False,
    "IscsiConnectionInitiatorAddress": False,
}


class IscsiConnectionInitiatorAddressSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IscsiConnectionInitiatorAddress object"""

    address = marshmallow_fields.Str(data_key="address", allow_none=True)
    r""" The TCP IPv4 or IPv6 address of the initiator end of the iSCSI connection.


Example: 10.10.10.7 """

    port = Size(data_key="port", allow_none=True)
    r""" The TCP port number of the initiator end of the iSCSI connection.


Example: 55432 """

    @property
    def resource(self):
        return IscsiConnectionInitiatorAddress

    gettable_fields = [
        "address",
        "port",
    ]
    """address,port,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class IscsiConnectionInitiatorAddress(Resource):

    _schema = IscsiConnectionInitiatorAddressSchema
