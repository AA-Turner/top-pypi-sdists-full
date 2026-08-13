r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["SecurityClusterNetworkIpsecAssociationResponseRecords", "SecurityClusterNetworkIpsecAssociationResponseRecordsSchema"]
__pdoc__ = {
    "SecurityClusterNetworkIpsecAssociationResponseRecordsSchema.resource": False,
    "SecurityClusterNetworkIpsecAssociationResponseRecordsSchema.opts": False,
    "SecurityClusterNetworkIpsecAssociationResponseRecords": False,
}

class SecurityClusterNetworkIpsecAssociationResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityClusterNetworkIpsecAssociationResponseRecords object"""

    cipher_suite = marshmallow_fields.Str(data_key="cipher_suite", allow_none=True)
    r""" Cipher suite for the security association.

Valid choices:

* suite_aescbc
* suiteb_gcm256
* suiteb_gmac256 """

    ike = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.security_cluster_network_ipsec_association_ike", "SecurityClusterNetworkIpsecAssociationIkeSchema"),
                unknown=EXCLUDE,
                data_key="ike",
                allow_none=True
            )
    r""" Objects containing parameters specific to IKE (Internet Key Exchange) security association for cluster network. """

    ipsec = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.security_cluster_network_ipsec_association_ipsec", "SecurityClusterNetworkIpsecAssociationIpsecSchema"),
                unknown=EXCLUDE,
                data_key="ipsec",
                allow_none=True
            )
    r""" Objects containing parameters specific to IPsec security association for cluster network. """

    lifetime = Size(data_key="lifetime", allow_none=True)
    r""" Lifetime for the security association in seconds. """

    local_address = marshmallow_fields.Str(data_key="local_address", allow_none=True)
    r""" Local address of the security association. """

    node = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.node", "NodeSchema"),
                unknown=EXCLUDE,
                data_key="node",
                allow_none=True
            )
    r""" The node field of the security_cluster_network_ipsec_association_response_records. """

    policy_name = marshmallow_fields.Str(data_key="policy_name", allow_none=True)
    r""" Policy name for the security association. """

    remote_address = marshmallow_fields.Str(data_key="remote_address", allow_none=True)
    r""" Remote address of the security association. """

    scope = marshmallow_fields.Str(data_key="scope", allow_none=True)
    r""" The scope field of the security_cluster_network_ipsec_association_response_records. """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Type of security association, it can be IPsec or IKE (Internet Key Exchange).

Valid choices:

* ipsec
* ike """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Unique identifier of the security association. """

    @property
    def resource(self):
        return SecurityClusterNetworkIpsecAssociationResponseRecords

    gettable_fields = [
        "cipher_suite",
        "ike",
        "ipsec",
        "lifetime",
        "local_address",
        "node.links",
        "node.name",
        "node.uuid",
        "policy_name",
        "remote_address",
        "scope",
        "type",
        "uuid",
    ]
    """cipher_suite,ike,ipsec,lifetime,local_address,node.links,node.name,node.uuid,policy_name,remote_address,scope,type,uuid,"""

    patchable_fields = [
        "cipher_suite",
        "ike",
        "ipsec",
        "lifetime",
        "local_address",
        "node.name",
        "node.uuid",
        "policy_name",
        "remote_address",
        "scope",
        "type",
        "uuid",
    ]
    """cipher_suite,ike,ipsec,lifetime,local_address,node.name,node.uuid,policy_name,remote_address,scope,type,uuid,"""

    postable_fields = [
        "cipher_suite",
        "ike",
        "ipsec",
        "lifetime",
        "local_address",
        "node.name",
        "node.uuid",
        "policy_name",
        "remote_address",
        "scope",
        "type",
        "uuid",
    ]
    """cipher_suite,ike,ipsec,lifetime,local_address,node.name,node.uuid,policy_name,remote_address,scope,type,uuid,"""


class SecurityClusterNetworkIpsecAssociationResponseRecords(Resource):

    _schema = SecurityClusterNetworkIpsecAssociationResponseRecordsSchema
