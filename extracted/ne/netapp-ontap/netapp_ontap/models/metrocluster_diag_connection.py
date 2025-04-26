r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["MetroclusterDiagConnection", "MetroclusterDiagConnectionSchema"]
__pdoc__ = {
    "MetroclusterDiagConnectionSchema.resource": False,
    "MetroclusterDiagConnectionSchema.opts": False,
    "MetroclusterDiagConnection": False,
}


class MetroclusterDiagConnectionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MetroclusterDiagConnection object"""

    destination_address = marshmallow_fields.Str(data_key="destination_address", allow_none=True)
    r""" The destination_address field of the metrocluster_diag_connection. """

    partner = marshmallow_fields.Nested("netapp_ontap.models.metrocluster_partner.MetroclusterPartnerSchema", unknown=EXCLUDE, data_key="partner", allow_none=True)
    r""" The partner field of the metrocluster_diag_connection. """

    port = marshmallow_fields.Str(data_key="port", allow_none=True)
    r""" The port field of the metrocluster_diag_connection. """

    result = marshmallow_fields.Str(data_key="result", allow_none=True)
    r""" Result of the diagnostic operation on this component.

Valid choices:

* ok
* warning
* not_run
* not_applicable """

    source_address = marshmallow_fields.Str(data_key="source_address", allow_none=True)
    r""" The source_address field of the metrocluster_diag_connection. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state field of the metrocluster_diag_connection.

Valid choices:

* disconnected
* completed
* pinging_partner_nodes
* enabling_ip_ports
* connecting_to_storage
* disconnecting_from_storage
* disabling_ip_ports
* configuring_ip_addresses
* updating_node_roles
* connecting_to_mediator
* disconnecting_from_mediator """

    @property
    def resource(self):
        return MetroclusterDiagConnection

    gettable_fields = [
        "destination_address",
        "partner",
        "port",
        "result",
        "source_address",
        "state",
    ]
    """destination_address,partner,port,result,source_address,state,"""

    patchable_fields = [
        "partner",
    ]
    """partner,"""

    postable_fields = [
        "partner",
    ]
    """partner,"""


class MetroclusterDiagConnection(Resource):

    _schema = MetroclusterDiagConnectionSchema
