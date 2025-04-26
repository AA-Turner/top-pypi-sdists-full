r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["MediatorResponseRecords", "MediatorResponseRecordsSchema"]
__pdoc__ = {
    "MediatorResponseRecordsSchema.resource": False,
    "MediatorResponseRecordsSchema.opts": False,
    "MediatorResponseRecords": False,
}


class MediatorResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MediatorResponseRecords object"""

    ca_certificate = marshmallow_fields.Str(data_key="ca_certificate", allow_none=True)
    r""" CA certificate for ONTAP Mediator. This is optional if the certificate is already installed. """

    dr_group = marshmallow_fields.Nested("netapp_ontap.resources.metrocluster_dr_group.MetroclusterDrGroupSchema", unknown=EXCLUDE, data_key="dr_group", allow_none=True)
    r""" The dr_group field of the mediator_response_records. """

    ip_address = marshmallow_fields.Str(data_key="ip_address", allow_none=True)
    r""" The IP address of the mediator.

Example: 10.10.10.7 """

    password = marshmallow_fields.Str(data_key="password", allow_none=True)
    r""" The password used to connect to the REST server on the mediator.

Example: mypassword """

    peer_cluster = marshmallow_fields.Nested("netapp_ontap.resources.cluster_peer.ClusterPeerSchema", unknown=EXCLUDE, data_key="peer_cluster", allow_none=True)
    r""" The peer_cluster field of the mediator_response_records. """

    peer_mediator_connectivity = marshmallow_fields.Str(data_key="peer_mediator_connectivity", allow_none=True)
    r""" Indicates the mediator connectivity status of the peer cluster. Possible values are connected, unreachable, unknown.

Example: connected """

    port = Size(data_key="port", allow_none=True)
    r""" The REST server's port number on the mediator.

Example: 31784 """

    reachable = marshmallow_fields.Boolean(data_key="reachable", allow_none=True)
    r""" Indicates the connectivity status of the mediator.

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
        "ip_address",
        "peer_cluster.links",
        "peer_cluster.name",
        "peer_cluster.uuid",
        "peer_mediator_connectivity",
        "port",
        "reachable",
        "uuid",
    ]
    """ip_address,peer_cluster.links,peer_cluster.name,peer_cluster.uuid,peer_mediator_connectivity,port,reachable,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "ca_certificate",
        "ip_address",
        "password",
        "peer_cluster.name",
        "peer_cluster.uuid",
        "port",
        "user",
    ]
    """ca_certificate,ip_address,password,peer_cluster.name,peer_cluster.uuid,port,user,"""


class MediatorResponseRecords(Resource):

    _schema = MediatorResponseRecordsSchema
