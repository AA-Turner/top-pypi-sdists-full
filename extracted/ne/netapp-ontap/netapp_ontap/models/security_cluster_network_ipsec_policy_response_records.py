r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["SecurityClusterNetworkIpsecPolicyResponseRecords", "SecurityClusterNetworkIpsecPolicyResponseRecordsSchema"]
__pdoc__ = {
    "SecurityClusterNetworkIpsecPolicyResponseRecordsSchema.resource": False,
    "SecurityClusterNetworkIpsecPolicyResponseRecordsSchema.opts": False,
    "SecurityClusterNetworkIpsecPolicyResponseRecords": False,
}

class SecurityClusterNetworkIpsecPolicyResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityClusterNetworkIpsecPolicyResponseRecords object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                unknown=EXCLUDE,
                data_key="_links",
                allow_none=True
            )
    r""" The links field of the security_cluster_network_ipsec_policy_response_records. """

    action = marshmallow_fields.Str(data_key="action", allow_none=True)
    r""" Action for the IPsec policy.

Valid choices:

* bypass
* discard
* esp_transport
* esp_udp """

    authentication_method = marshmallow_fields.Str(data_key="authentication_method", allow_none=True)
    r""" Authentication method for the IPsec policy. Must be PKI for cluster security.

Valid choices:

* pki """

    certificate = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.security_certificate", "SecurityCertificateSchema"),
                unknown=EXCLUDE,
                data_key="certificate",
                allow_none=True
            )
    r""" The certificate field of the security_cluster_network_ipsec_policy_response_records. """

    local_ip = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.security_cluster_network_ipsec_policy_local_ip", "SecurityClusterNetworkIpsecPolicyLocalIpSchema"),
                unknown=EXCLUDE,
                data_key="local_ip",
                allow_none=True
            )
    r""" Local IP endpoint for the IPsec policy. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" IPsec policy name.

Example: policy1 """

    node = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.node", "NodeSchema"),
                unknown=EXCLUDE,
                data_key="node",
                allow_none=True
            )
    r""" The node field of the security_cluster_network_ipsec_policy_response_records. """

    remote_ip = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.security_cluster_network_ipsec_policy_remote_ip", "SecurityClusterNetworkIpsecPolicyRemoteIpSchema"),
                unknown=EXCLUDE,
                data_key="remote_ip",
                allow_none=True
            )
    r""" Remote IP endpoint for the IPsec policy. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Unique identifier for the IPsec policy.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return SecurityClusterNetworkIpsecPolicyResponseRecords

    gettable_fields = [
        "links",
        "action",
        "authentication_method",
        "certificate.links",
        "certificate.name",
        "certificate.uuid",
        "local_ip",
        "name",
        "node.links",
        "node.name",
        "node.uuid",
        "remote_ip",
        "uuid",
    ]
    """links,action,authentication_method,certificate.links,certificate.name,certificate.uuid,local_ip,name,node.links,node.name,node.uuid,remote_ip,uuid,"""

    patchable_fields = [
        "certificate.name",
        "certificate.uuid",
        "node.name",
        "node.uuid",
    ]
    """certificate.name,certificate.uuid,node.name,node.uuid,"""

    postable_fields = [
        "certificate.name",
        "certificate.uuid",
        "node.name",
        "node.uuid",
    ]
    """certificate.name,certificate.uuid,node.name,node.uuid,"""


class SecurityClusterNetworkIpsecPolicyResponseRecords(Resource):

    _schema = SecurityClusterNetworkIpsecPolicyResponseRecordsSchema
