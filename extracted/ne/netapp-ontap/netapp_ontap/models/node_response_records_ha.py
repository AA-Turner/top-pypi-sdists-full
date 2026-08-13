r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["NodeResponseRecordsHa", "NodeResponseRecordsHaSchema"]
__pdoc__ = {
    "NodeResponseRecordsHaSchema.resource": False,
    "NodeResponseRecordsHaSchema.opts": False,
    "NodeResponseRecordsHa": False,
}

class NodeResponseRecordsHaSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NodeResponseRecordsHa object"""

    auto_giveback = marshmallow_fields.Boolean(data_key="auto_giveback", allow_none=True)
    r""" Specifies whether giveback is automatically initiated when the node that owns the storage is ready. """

    auto_giveback_of = marshmallow_fields.Boolean(data_key="auto_giveback_of", allow_none=True)
    r""" Specifies whether giveback is automatically initiated when the node that owns the storage is ready. """

    enable_takeover_of = marshmallow_fields.Boolean(data_key="enable_takeover_of", allow_none=True)
    r""" Specifies whether or not storage failover is enabled. """

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Specifies whether or not storage failover is enabled. """

    giveback = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.node_response_records_ha_giveback", "NodeResponseRecordsHaGivebackSchema"),
                unknown=EXCLUDE,
                data_key="giveback",
                allow_none=True
            )
    r""" Represents the state of the node that is giving storage back to its HA partner. """

    giveback_of = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.cluster_nodes_ha_giveback_of", "ClusterNodesHaGivebackOfSchema"),
                unknown=EXCLUDE,
                data_key="giveback_of",
                allow_none=True
            )
    r""" Represents the state of storage being given back to the node. """

    giveback_of_possible = marshmallow_fields.Boolean(data_key="giveback_of_possible", allow_none=True)
    r""" Specifies whether or not storage giveback is possible. """

    interconnect = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.cluster_nodes_ha_interconnect", "ClusterNodesHaInterconnectSchema"),
                unknown=EXCLUDE,
                data_key="interconnect",
                allow_none=True
            )
    r""" The interconnect field of the node_response_records_ha. """

    partners = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.node_ha_partners", "NodeHaPartnersSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="partners",
                allow_none=True
                )
    r""" <personalities supports=unified,asar2>
Nodes in this node's High Availability (HA) group.
</personalities>
<personalities supports=aiml>
Nodes that are failover destinations for this node.
</personalities> """

    peering = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.cluster_nodes_ha_peering", "ClusterNodesHaPeeringSchema"),
                unknown=EXCLUDE,
                data_key="peering",
                allow_none=True
            )
    r""" The peering field of the node_response_records_ha. """

    ports = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.cluster_nodes_ha_ports", "ClusterNodesHaPortsSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="ports",
                allow_none=True
                )
    r""" The ports field of the node_response_records_ha. """

    takeover = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.cluster_nodes_ha_takeover", "ClusterNodesHaTakeoverSchema"),
                unknown=EXCLUDE,
                data_key="takeover",
                allow_none=True
            )
    r""" This represents the state of the node that is taking over storage from its HA partner. """

    takeover_check = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.cluster_nodes_ha_takeover_check", "ClusterNodesHaTakeoverCheckSchema"),
                unknown=EXCLUDE,
                data_key="takeover_check",
                allow_none=True
            )
    r""" The takeover check response. """

    takeover_of = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.cluster_nodes_ha_takeover_of", "ClusterNodesHaTakeoverOfSchema"),
                unknown=EXCLUDE,
                data_key="takeover_of",
                allow_none=True
            )
    r""" This represents the storage takeover state of the node. """

    takeover_of_possible = marshmallow_fields.Boolean(data_key="takeover_of_possible", allow_none=True)
    r""" Specifies whether or not storage takeover is possible. """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Type of storage.

Valid choices:

* shared_storage
* non_shared_storage """

    @property
    def resource(self):
        return NodeResponseRecordsHa

    gettable_fields = [
        "auto_giveback",
        "auto_giveback_of",
        "enable_takeover_of",
        "enabled",
        "giveback",
        "giveback_of",
        "giveback_of_possible",
        "interconnect",
        "partners.links",
        "partners.name",
        "partners.uuid",
        "peering",
        "ports",
        "takeover",
        "takeover_check",
        "takeover_of",
        "takeover_of_possible",
        "type",
    ]
    """auto_giveback,auto_giveback_of,enable_takeover_of,enabled,giveback,giveback_of,giveback_of_possible,interconnect,partners.links,partners.name,partners.uuid,peering,ports,takeover,takeover_check,takeover_of,takeover_of_possible,type,"""

    patchable_fields = [
        "auto_giveback",
        "auto_giveback_of",
        "enabled",
    ]
    """auto_giveback,auto_giveback_of,enabled,"""

    postable_fields = [
        "auto_giveback",
        "auto_giveback_of",
        "enabled",
    ]
    """auto_giveback,auto_giveback_of,enabled,"""


class NodeResponseRecordsHa(Resource):

    _schema = NodeResponseRecordsHaSchema
