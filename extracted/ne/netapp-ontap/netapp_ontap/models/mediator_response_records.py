r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["MediatorResponseRecords", "MediatorResponseRecordsSchema"]
__pdoc__ = {
    "MediatorResponseRecordsSchema.resource": False,
    "MediatorResponseRecordsSchema.opts": False,
    "MediatorResponseRecords": False,
}

class MediatorResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MediatorResponseRecords object"""

    account_token = marshmallow_fields.Str(data_key="account_token", allow_none=True)
    r""" NetApp Console account token. This field is only applicable to the ONTAP cloud mediator. """

    bluexp_account_token = marshmallow_fields.Str(data_key="bluexp_account_token", allow_none=True)
    r""" BlueXP account token. This field is only applicable to the ONTAP cloud mediator. This has been replaced by account_token. Support for this field will be removed in a future release. """

    bluexp_org_id = marshmallow_fields.Str(data_key="bluexp_org_id", allow_none=True)
    r""" BlueXP organization ID. This field is only applicable to the ONTAP cloud mediator. This has been replaced by org_id. Support for this field will be removed in a future release. """

    ca_certificate = marshmallow_fields.Str(data_key="ca_certificate", allow_none=True)
    r""" CA certificate for ONTAP Mediator. This is optional if the certificate is already installed. """

    connection_type = marshmallow_fields.Str(data_key="connection_type", allow_none=True)
    r""" Connection type from ONTAP MetroCluster to mediator. Applicable only to on-prem mediator used in ONTAP MetroCluster configurations.

Valid choices:

* iscsi_mediator
* https_mediator """

    dr_group = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.metrocluster_dr_group", "MetroclusterDrGroupSchema"),
                unknown=EXCLUDE,
                data_key="dr_group",
                allow_none=True
            )
    r""" The dr_group field of the mediator_response_records. """

    ip_address = marshmallow_fields.Str(data_key="ip_address", allow_none=True)
    r""" The IP address of the mediator.

Example: 10.10.10.7 """

    local_mediator_connectivity = marshmallow_fields.Str(data_key="local_mediator_connectivity", allow_none=True)
    r""" Indicates the mediator connectivity status of the local cluster. Possible values are connected, unreachable, unusable and down-high-latency. This field is only applicable to the mediators in SnapMirror active sync configuration.

Example: connected """

    org_id = marshmallow_fields.Str(data_key="org_id", allow_none=True)
    r""" NetApp Console organization ID. This field is only applicable to the ONTAP cloud mediator. """

    password = marshmallow_fields.Str(data_key="password", allow_none=True)
    r""" The password used to connect to the REST server on the mediator.

Example: mypassword """

    peer_cluster = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.cluster_peer", "ClusterPeerSchema"),
                unknown=EXCLUDE,
                data_key="peer_cluster",
                allow_none=True
            )
    r""" The peer_cluster field of the mediator_response_records. """

    peer_mediator_connectivity = marshmallow_fields.Str(data_key="peer_mediator_connectivity", allow_none=True)
    r""" Indicates the mediator connectivity status of the peer cluster. Possible values are connected, unreachable, unknown and down-high-latency.

Example: connected """

    port = Size(data_key="port", allow_none=True)
    r""" The REST server's port number on the mediator.

Example: 31784 """

    reachable = marshmallow_fields.Boolean(data_key="reachable", allow_none=True)
    r""" Indicates the connectivity status of the mediator.

Example: true """

    service_account_client_id = marshmallow_fields.Str(data_key="service_account_client_id", allow_none=True)
    r""" Client ID of the NetApp Console service account. This field is only applicable to the ONTAP cloud mediator. """

    service_account_client_secret = marshmallow_fields.Str(data_key="service_account_client_secret", allow_none=True)
    r""" Client secret token of the NetApp Console service account. This field is only applicable to the ONTAP cloud mediator. """

    strict_cert_validation = marshmallow_fields.Boolean(data_key="strict_cert_validation", allow_none=True)
    r""" Indicates if strict validation of certificates is performed while making REST API calls to the mediator. This field is only applicable to the ONTAP Cloud Mediator.

Example: true """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Mediator type. This field is only applicable to the mediators in SnapMirror active sync configuration.

Valid choices:

* cloud
* on_prem """

    use_http_proxy_local = marshmallow_fields.Boolean(data_key="use_http_proxy_local", allow_none=True)
    r""" Indicates if the local cluster should use an http-proxy server while making REST API calls to the mediator. This field is only applicable to the ONTAP cloud mediator.

Example: true """

    use_http_proxy_remote = marshmallow_fields.Boolean(data_key="use_http_proxy_remote", allow_none=True)
    r""" Indicates if the remote cluster should use an http-proxy server while making REST API calls to the mediator. This field is only applicable to the ONTAP cloud mediator.

Example: true """

    user = marshmallow_fields.Str(data_key="user", allow_none=True)
    r""" The username used to connect to the REST server on the mediator.

Example: myusername """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier for the mediator service. """

    @property
    def resource(self):
        return MediatorResponseRecords

    gettable_fields = [
        "connection_type",
        "ip_address",
        "local_mediator_connectivity",
        "peer_cluster.links",
        "peer_cluster.name",
        "peer_cluster.uuid",
        "peer_mediator_connectivity",
        "port",
        "reachable",
        "strict_cert_validation",
        "type",
        "use_http_proxy_local",
        "uuid",
    ]
    """connection_type,ip_address,local_mediator_connectivity,peer_cluster.links,peer_cluster.name,peer_cluster.uuid,peer_mediator_connectivity,port,reachable,strict_cert_validation,type,use_http_proxy_local,uuid,"""

    patchable_fields = [
        "strict_cert_validation",
        "use_http_proxy_local",
        "use_http_proxy_remote",
    ]
    """strict_cert_validation,use_http_proxy_local,use_http_proxy_remote,"""

    postable_fields = [
        "account_token",
        "bluexp_account_token",
        "bluexp_org_id",
        "ca_certificate",
        "connection_type",
        "ip_address",
        "org_id",
        "password",
        "peer_cluster.name",
        "peer_cluster.uuid",
        "port",
        "service_account_client_id",
        "service_account_client_secret",
        "strict_cert_validation",
        "type",
        "use_http_proxy_local",
        "use_http_proxy_remote",
        "user",
    ]
    """account_token,bluexp_account_token,bluexp_org_id,ca_certificate,connection_type,ip_address,org_id,password,peer_cluster.name,peer_cluster.uuid,port,service_account_client_id,service_account_client_secret,strict_cert_validation,type,use_http_proxy_local,use_http_proxy_remote,user,"""


class MediatorResponseRecords(Resource):

    _schema = MediatorResponseRecordsSchema
