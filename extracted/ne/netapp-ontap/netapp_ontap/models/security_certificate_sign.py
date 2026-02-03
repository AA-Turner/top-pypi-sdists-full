r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["SecurityCertificateSign", "SecurityCertificateSignSchema"]
__pdoc__ = {
    "SecurityCertificateSignSchema.resource": False,
    "SecurityCertificateSignSchema.opts": False,
    "SecurityCertificateSign": False,
}

class SecurityCertificateSignSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityCertificateSign object"""

    expiry_time = marshmallow_fields.Str(data_key="expiry_time", allow_none=True)
    r""" Certificate expiration time, in ISO 8601 duration format or date and time format. The allowed expiration time range is between 1 day to 10 years.

Example: P1DT2H3M4S or '2030-01-25T11:20:13Z' """

    hash_function = marshmallow_fields.Str(data_key="hash_function", allow_none=True)
    r""" Hashing function

Valid choices:

* sha256
* sha224
* sha384
* sha512 """

    signing_request = marshmallow_fields.Str(data_key="signing_request", allow_none=True)
    r""" Certificate signing request to be signed by the given certificate authority. Request should be in X509 PEM format.

Example: <CERTIFICATE-CONTENT> """

    @property
    def resource(self):
        return SecurityCertificateSign

    gettable_fields = [
        "expiry_time",
        "hash_function",
        "signing_request",
    ]
    """expiry_time,hash_function,signing_request,"""

    patchable_fields = [
        "expiry_time",
        "hash_function",
        "signing_request",
    ]
    """expiry_time,hash_function,signing_request,"""

    postable_fields = [
        "expiry_time",
        "hash_function",
        "signing_request",
    ]
    """expiry_time,hash_function,signing_request,"""


class SecurityCertificateSign(Resource):

    _schema = SecurityCertificateSignSchema
