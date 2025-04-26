r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationSanAccessIscsiEndpoint", "ApplicationSanAccessIscsiEndpointSchema"]
__pdoc__ = {
    "ApplicationSanAccessIscsiEndpointSchema.resource": False,
    "ApplicationSanAccessIscsiEndpointSchema.opts": False,
    "ApplicationSanAccessIscsiEndpoint": False,
}


class ApplicationSanAccessIscsiEndpointSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationSanAccessIscsiEndpoint object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the application_san_access_iscsi_endpoint. """

    interface = marshmallow_fields.Nested("netapp_ontap.resources.ip_interface.IpInterfaceSchema", unknown=EXCLUDE, data_key="interface", allow_none=True)
    r""" The interface field of the application_san_access_iscsi_endpoint. """

    port = Size(data_key="port", allow_none=True)
    r""" The TCP port number of the iSCSI access endpoint.

Example: 3260 """

    @property
    def resource(self):
        return ApplicationSanAccessIscsiEndpoint

    gettable_fields = [
        "links",
        "interface.links",
        "interface.ip",
        "interface.name",
        "interface.uuid",
        "port",
    ]
    """links,interface.links,interface.ip,interface.name,interface.uuid,port,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ApplicationSanAccessIscsiEndpoint(Resource):

    _schema = ApplicationSanAccessIscsiEndpointSchema
