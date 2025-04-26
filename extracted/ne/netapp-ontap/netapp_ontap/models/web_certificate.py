r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["WebCertificate", "WebCertificateSchema"]
__pdoc__ = {
    "WebCertificateSchema.resource": False,
    "WebCertificateSchema.opts": False,
    "WebCertificate": False,
}


class WebCertificateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WebCertificate object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the web_certificate. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Certificate name

Example: cert1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Certificate UUID

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return WebCertificate

    gettable_fields = [
        "links",
        "name",
        "uuid",
    ]
    """links,name,uuid,"""

    patchable_fields = [
        "uuid",
    ]
    """uuid,"""

    postable_fields = [
        "uuid",
    ]
    """uuid,"""


class WebCertificate(Resource):

    _schema = WebCertificateSchema
