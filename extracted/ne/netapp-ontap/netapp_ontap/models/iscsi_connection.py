r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IscsiConnection", "IscsiConnectionSchema"]
__pdoc__ = {
    "IscsiConnectionSchema.resource": False,
    "IscsiConnectionSchema.opts": False,
    "IscsiConnection": False,
}


class IscsiConnectionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IscsiConnection object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.collection_links.CollectionLinksSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the iscsi_connection. """

    authentication_type = marshmallow_fields.Str(data_key="authentication_type", allow_none=True)
    r""" The iSCSI authentication type used to establish the connection.


Valid choices:

* chap
* none """

    cid = Size(data_key="cid", allow_none=True)
    r""" The identifier of the connection within the session. """

    initiator_address = marshmallow_fields.Nested("netapp_ontap.models.iscsi_connection_initiator_address.IscsiConnectionInitiatorAddressSchema", unknown=EXCLUDE, data_key="initiator_address", allow_none=True)
    r""" The TCP socket information for the initiator end of the connection. This is useful for network packet debugging. """

    interface = marshmallow_fields.Nested("netapp_ontap.models.iscsi_connection_interface.IscsiConnectionInterfaceSchema", unknown=EXCLUDE, data_key="interface", allow_none=True)
    r""" The network interface information for the target end of the connection. """

    @property
    def resource(self):
        return IscsiConnection

    gettable_fields = [
        "links",
        "authentication_type",
        "cid",
        "initiator_address",
        "interface",
    ]
    """links,authentication_type,cid,initiator_address,interface,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class IscsiConnection(Resource):

    _schema = IscsiConnectionSchema
