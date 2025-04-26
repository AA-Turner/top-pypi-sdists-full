r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["CertificateSigningRequest", "CertificateSigningRequestSchema"]
__pdoc__ = {
    "CertificateSigningRequestSchema.resource": False,
    "CertificateSigningRequestSchema.opts": False,
    "CertificateSigningRequest": False,
}


class CertificateSigningRequestSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CertificateSigningRequest object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the certificate_signing_request. """

    algorithm = marshmallow_fields.Str(data_key="algorithm", allow_none=True)
    r""" Asymmetric Encryption Algorithm.

Valid choices:

* rsa
* ec """

    csr = marshmallow_fields.Str(data_key="csr", allow_none=True)
    r""" A Certificate Signing Request (CSR) provided to a CA for obtaining a CA-signed certificate. """

    extended_key_usages = marshmallow_fields.List(marshmallow_fields.Str, data_key="extended_key_usages", allow_none=True)
    r""" A list of extended key usage extensions. """

    generated_private_key = marshmallow_fields.Str(data_key="generated_private_key", allow_none=True)
    r""" Private key generated for the CSR. """

    hash_function = marshmallow_fields.Str(data_key="hash_function", allow_none=True)
    r""" Hashing function.

Valid choices:

* sha256
* sha224
* sha384
* sha512 """

    key_usages = marshmallow_fields.List(marshmallow_fields.Str, data_key="key_usages", allow_none=True)
    r""" A list of key usage extensions. """

    security_strength = Size(data_key="security_strength", allow_none=True)
    r""" Security strength of the certificate in bits. """

    subject_alternatives = marshmallow_fields.Nested("netapp_ontap.models.subject_alternate_name.SubjectAlternateNameSchema", unknown=EXCLUDE, data_key="subject_alternatives", allow_none=True)
    r""" The subject_alternatives field of the certificate_signing_request. """

    subject_name = marshmallow_fields.Str(data_key="subject_name", allow_none=True)
    r""" Subject name details of the certificate. The format is a list of comma separated key=value pairs.

Example: C=US,O=NTAP,CN=test.domain.com """

    @property
    def resource(self):
        return CertificateSigningRequest

    gettable_fields = [
        "links",
        "algorithm",
        "csr",
        "extended_key_usages",
        "generated_private_key",
        "hash_function",
        "key_usages",
        "security_strength",
        "subject_alternatives",
        "subject_name",
    ]
    """links,algorithm,csr,extended_key_usages,generated_private_key,hash_function,key_usages,security_strength,subject_alternatives,subject_name,"""

    patchable_fields = [
        "extended_key_usages",
        "key_usages",
    ]
    """extended_key_usages,key_usages,"""

    postable_fields = [
        "algorithm",
        "extended_key_usages",
        "hash_function",
        "key_usages",
        "security_strength",
        "subject_alternatives",
        "subject_name",
    ]
    """algorithm,extended_key_usages,hash_function,key_usages,security_strength,subject_alternatives,subject_name,"""


class CertificateSigningRequest(Resource):

    _schema = CertificateSigningRequestSchema
