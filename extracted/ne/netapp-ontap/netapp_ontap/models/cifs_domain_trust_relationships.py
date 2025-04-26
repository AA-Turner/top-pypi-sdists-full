r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["CifsDomainTrustRelationships", "CifsDomainTrustRelationshipsSchema"]
__pdoc__ = {
    "CifsDomainTrustRelationshipsSchema.resource": False,
    "CifsDomainTrustRelationshipsSchema.opts": False,
    "CifsDomainTrustRelationships": False,
}


class CifsDomainTrustRelationshipsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CifsDomainTrustRelationships object"""

    home_domain = marshmallow_fields.Str(data_key="home_domain", allow_none=True)
    r""" Home Domain Name """

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the cifs_domain_trust_relationships. """

    trusted_domains = marshmallow_fields.List(marshmallow_fields.Str, data_key="trusted_domains", allow_none=True)
    r""" Trusted Domain Name """

    @property
    def resource(self):
        return CifsDomainTrustRelationships

    gettable_fields = [
        "home_domain",
        "node.links",
        "node.name",
        "node.uuid",
        "trusted_domains",
    ]
    """home_domain,node.links,node.name,node.uuid,trusted_domains,"""

    patchable_fields = [
        "home_domain",
        "node.name",
        "node.uuid",
        "trusted_domains",
    ]
    """home_domain,node.name,node.uuid,trusted_domains,"""

    postable_fields = [
        "home_domain",
        "node.name",
        "node.uuid",
        "trusted_domains",
    ]
    """home_domain,node.name,node.uuid,trusted_domains,"""


class CifsDomainTrustRelationships(Resource):

    _schema = CifsDomainTrustRelationshipsSchema
