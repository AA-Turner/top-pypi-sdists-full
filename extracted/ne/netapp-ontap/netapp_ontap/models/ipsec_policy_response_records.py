r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IpsecPolicyResponseRecords", "IpsecPolicyResponseRecordsSchema"]
__pdoc__ = {
    "IpsecPolicyResponseRecordsSchema.resource": False,
    "IpsecPolicyResponseRecordsSchema.opts": False,
    "IpsecPolicyResponseRecords": False,
}


class IpsecPolicyResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IpsecPolicyResponseRecords object"""

    action = marshmallow_fields.Str(data_key="action", allow_none=True)
    r""" Action for the IPsec policy.

Valid choices:

* bypass
* discard
* esp_transport
* esp_udp """

    authentication_method = marshmallow_fields.Str(data_key="authentication_method", allow_none=True)
    r""" Authentication method for the IPsec policy.

Valid choices:

* none
* psk
* pki """

    certificate = marshmallow_fields.Nested("netapp_ontap.resources.security_certificate.SecurityCertificateSchema", unknown=EXCLUDE, data_key="certificate", allow_none=True)
    r""" The certificate field of the ipsec_policy_response_records. """

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Indicates whether or not the policy is enabled. """

    ipspace = marshmallow_fields.Nested("netapp_ontap.resources.ipspace.IpspaceSchema", unknown=EXCLUDE, data_key="ipspace", allow_none=True)
    r""" The ipspace field of the ipsec_policy_response_records. """

    local_endpoint = marshmallow_fields.Nested("netapp_ontap.models.ipsec_endpoint.IpsecEndpointSchema", unknown=EXCLUDE, data_key="local_endpoint", allow_none=True)
    r""" Endpoint specification for the IPsec policy """

    local_identity = marshmallow_fields.Str(data_key="local_identity", allow_none=True)
    r""" Local Identity """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" IPsec policy name. """

    protocol = marshmallow_fields.Str(data_key="protocol", allow_none=True)
    r""" Lower layer protocol to be covered by the IPsec policy.

Example: 17 """

    remote_endpoint = marshmallow_fields.Nested("netapp_ontap.models.ipsec_endpoint.IpsecEndpointSchema", unknown=EXCLUDE, data_key="remote_endpoint", allow_none=True)
    r""" Endpoint specification for the IPsec policy """

    remote_identity = marshmallow_fields.Str(data_key="remote_identity", allow_none=True)
    r""" Remote Identity """

    scope = marshmallow_fields.Str(data_key="scope", allow_none=True)
    r""" The scope field of the ipsec_policy_response_records. """

    secret_key = marshmallow_fields.Str(data_key="secret_key", allow_none=True)
    r""" Pre-shared key for IKE negotiation. """

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", unknown=EXCLUDE, data_key="svm", allow_none=True)
    r""" The svm field of the ipsec_policy_response_records. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Unique identifier of the IPsec policy.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return IpsecPolicyResponseRecords

    gettable_fields = [
        "action",
        "authentication_method",
        "certificate.links",
        "certificate.name",
        "certificate.uuid",
        "enabled",
        "ipspace.links",
        "ipspace.name",
        "ipspace.uuid",
        "local_endpoint",
        "local_identity",
        "name",
        "protocol",
        "remote_endpoint",
        "remote_identity",
        "scope",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """action,authentication_method,certificate.links,certificate.name,certificate.uuid,enabled,ipspace.links,ipspace.name,ipspace.uuid,local_endpoint,local_identity,name,protocol,remote_endpoint,remote_identity,scope,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
        "certificate.name",
        "certificate.uuid",
        "enabled",
        "local_endpoint",
        "local_identity",
        "protocol",
        "remote_endpoint",
        "remote_identity",
        "scope",
    ]
    """certificate.name,certificate.uuid,enabled,local_endpoint,local_identity,protocol,remote_endpoint,remote_identity,scope,"""

    postable_fields = [
        "action",
        "authentication_method",
        "certificate.name",
        "certificate.uuid",
        "enabled",
        "ipspace.name",
        "ipspace.uuid",
        "local_endpoint",
        "local_identity",
        "name",
        "protocol",
        "remote_endpoint",
        "remote_identity",
        "scope",
        "secret_key",
        "svm.name",
        "svm.uuid",
    ]
    """action,authentication_method,certificate.name,certificate.uuid,enabled,ipspace.name,ipspace.uuid,local_endpoint,local_identity,name,protocol,remote_endpoint,remote_identity,scope,secret_key,svm.name,svm.uuid,"""


class IpsecPolicyResponseRecords(Resource):

    _schema = IpsecPolicyResponseRecordsSchema
