r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeTcpTls", "NvmeTcpTlsSchema"]
__pdoc__ = {
    "NvmeTcpTlsSchema.resource": False,
    "NvmeTcpTlsSchema.opts": False,
    "NvmeTcpTls": False,
}


class NvmeTcpTlsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeTcpTls object"""

    configured_psk = marshmallow_fields.Str(data_key="configured_psk", allow_none=True)
    r""" A user supplied pre-shared key (PSK) value in PSK Interchange Format. Optional in POST.</br>
The values for property `key_type` and property `configured_psk` must logically agree. This property is only allowed when `key_type` is `configured`. If `configured_psk` is supplied and `key_type` is unset, `key_type` defaults to `configured`.</br>
This property is write-only. The `key_type` property can be used to identify if a configured PSK has been set for the host, but the PSK value cannot be read. To change the value, the host must be deleted from the subsystem and re-added.


Example: NVMeTLSkey-1:01:VRLbtnN9AQb2WXW3c9+wEf/DRLz0QuLdbYvEhwtdWwNf9LrZ: """

    key_type = marshmallow_fields.Str(data_key="key_type", allow_none=True)
    r""" The method by which the TLS pre-shared key (PSK) is configured for the host. Optional in POST.</br>
The values for property `key_type` and property `configured_psk` must logically agree.</br>
Possible values:
- `none` - TLS is not configured for the host connection. No value is allowed for property `configured_psk`.
- `configured` - A user supplied PSK is configured for the NVMe/TCP-TLS transport connection between the host and the NVMe subsystem. A valid value for property `configured_psk` is required.
</br>
This property defaults to `none` unless a value is supplied for `configured_psk` in which case it defaults to `configured`.


Valid choices:

* none
* configured """

    @property
    def resource(self):
        return NvmeTcpTls

    gettable_fields = [
        "key_type",
    ]
    """key_type,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "configured_psk",
        "key_type",
    ]
    """configured_psk,key_type,"""


class NvmeTcpTls(Resource):

    _schema = NvmeTcpTlsSchema
