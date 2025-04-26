r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["EmsCertificate", "EmsCertificateSchema"]
__pdoc__ = {
    "EmsCertificateSchema.resource": False,
    "EmsCertificateSchema.opts": False,
    "EmsCertificate": False,
}


class EmsCertificateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsCertificate object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the ems_certificate. """

    ca = marshmallow_fields.Str(data_key="ca", allow_none=True)
    r""" Client certificate issuing CA

Example: VeriSign """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Certificate name """

    serial_number = marshmallow_fields.Str(data_key="serial_number", allow_none=True)
    r""" Client certificate serial number

Example: 1234567890 """

    @property
    def resource(self):
        return EmsCertificate

    gettable_fields = [
        "links",
        "ca",
        "name",
        "serial_number",
    ]
    """links,ca,name,serial_number,"""

    patchable_fields = [
        "ca",
        "serial_number",
    ]
    """ca,serial_number,"""

    postable_fields = [
        "ca",
        "serial_number",
    ]
    """ca,serial_number,"""


class EmsCertificate(Resource):

    _schema = EmsCertificateSchema
