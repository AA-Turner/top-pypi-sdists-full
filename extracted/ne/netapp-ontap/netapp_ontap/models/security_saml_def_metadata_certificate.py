r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SecuritySamlDefMetadataCertificate", "SecuritySamlDefMetadataCertificateSchema"]
__pdoc__ = {
    "SecuritySamlDefMetadataCertificateSchema.resource": False,
    "SecuritySamlDefMetadataCertificateSchema.opts": False,
    "SecuritySamlDefMetadataCertificate": False,
}


class SecuritySamlDefMetadataCertificateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecuritySamlDefMetadataCertificate object"""

    ca = marshmallow_fields.Str(data_key="ca", allow_none=True)
    r""" Server certificate issuing certificate authority (CA).  This cannot be used with the server certificate common name. """

    common_name = marshmallow_fields.Str(data_key="common_name", allow_none=True)
    r""" Server certificate common name.  This cannot be used with the certificate authority (CA) or serial_number.

Example: cluster1 """

    serial_number = marshmallow_fields.Str(data_key="serial_number", allow_none=True)
    r""" Server certificate serial number.  This cannot be used with the server certificate common name.

Example: 1506B24A94F566BA """

    @property
    def resource(self):
        return SecuritySamlDefMetadataCertificate

    gettable_fields = [
        "ca",
        "common_name",
        "serial_number",
    ]
    """ca,common_name,serial_number,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "ca",
        "common_name",
        "serial_number",
    ]
    """ca,common_name,serial_number,"""


class SecuritySamlDefMetadataCertificate(Resource):

    _schema = SecuritySamlDefMetadataCertificateSchema
