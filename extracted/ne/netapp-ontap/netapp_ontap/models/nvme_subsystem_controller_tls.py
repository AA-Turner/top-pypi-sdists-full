r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeSubsystemControllerTls", "NvmeSubsystemControllerTlsSchema"]
__pdoc__ = {
    "NvmeSubsystemControllerTlsSchema.resource": False,
    "NvmeSubsystemControllerTlsSchema.opts": False,
    "NvmeSubsystemControllerTls": False,
}


class NvmeSubsystemControllerTlsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeSubsystemControllerTls object"""

    cipher = marshmallow_fields.Str(data_key="cipher", allow_none=True)
    r""" The cipher suite used for the transport by the encrypted NVMe/TCP transport connection between the host and the NVMe subsystem. This property is populated only when encryption is in use for the transport connection.


Valid choices:

* tls_aes_128_gcm_sha256
* tls_aes_256_gcm_sha384 """

    key_type = marshmallow_fields.Str(data_key="key_type", allow_none=True)
    r""" The method by which the TLS pre-shared key (PSK) was obtained when establishing the encrypted NVMe/TCP transport connection between the host and the NVMe subsystem.
Possible values:
  - `none` - TLS encryption is not configured for the host connection.
  - `configured` - A user supplied PSK was used for the encrypted NVMe/TCP-TLS transport connection between the host and the NVMe subsystem.


Valid choices:

* none
* configured """

    psk_identity = marshmallow_fields.Str(data_key="psk_identity", allow_none=True)
    r""" The TLS PSK identity supplied by the host when establishing the encrypted NVMe/TCP transport connection between the host and the NVMe subsystem. This property is populated only when encryption is in use for the transport connection.


Example: NVMe1R01 nqn.2014-08.org.nvmexpress:uuid:713b3816-f9bf-ba43-b95a-5e4bf8c726e9 nqn.1992-08.com.netapp:sn.76f9d9bfb96511eea95e005056bb72b2:subsystem.ss1 mS1A7nrooevA9ZqAM09fQzWQlB2UZRt0BE1X4vINjY0=: """

    @property
    def resource(self):
        return NvmeSubsystemControllerTls

    gettable_fields = [
        "cipher",
        "key_type",
        "psk_identity",
    ]
    """cipher,key_type,psk_identity,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class NvmeSubsystemControllerTls(Resource):

    _schema = NvmeSubsystemControllerTlsSchema
