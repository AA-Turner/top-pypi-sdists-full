r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationSanAccessIscsiEndpointInterfaceIp", "ApplicationSanAccessIscsiEndpointInterfaceIpSchema"]
__pdoc__ = {
    "ApplicationSanAccessIscsiEndpointInterfaceIpSchema.resource": False,
    "ApplicationSanAccessIscsiEndpointInterfaceIpSchema.opts": False,
    "ApplicationSanAccessIscsiEndpointInterfaceIp": False,
}


class ApplicationSanAccessIscsiEndpointInterfaceIpSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationSanAccessIscsiEndpointInterfaceIp object"""

    address = marshmallow_fields.Str(data_key="address", allow_none=True)
    r""" The address field of the application_san_access_iscsi_endpoint_interface_ip. """

    @property
    def resource(self):
        return ApplicationSanAccessIscsiEndpointInterfaceIp

    gettable_fields = [
        "address",
    ]
    """address,"""

    patchable_fields = [
        "address",
    ]
    """address,"""

    postable_fields = [
        "address",
    ]
    """address,"""


class ApplicationSanAccessIscsiEndpointInterfaceIp(Resource):

    _schema = ApplicationSanAccessIscsiEndpointInterfaceIpSchema
