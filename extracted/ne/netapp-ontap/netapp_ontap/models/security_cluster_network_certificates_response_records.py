r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["SecurityClusterNetworkCertificatesResponseRecords", "SecurityClusterNetworkCertificatesResponseRecordsSchema"]
__pdoc__ = {
    "SecurityClusterNetworkCertificatesResponseRecordsSchema.resource": False,
    "SecurityClusterNetworkCertificatesResponseRecordsSchema.opts": False,
    "SecurityClusterNetworkCertificatesResponseRecords": False,
}

class SecurityClusterNetworkCertificatesResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityClusterNetworkCertificatesResponseRecords object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                unknown=EXCLUDE,
                data_key="_links",
                allow_none=True
            )
    r""" The links field of the security_cluster_network_certificates_response_records. """

    certificate = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.security_certificate", "SecurityCertificateSchema"),
                unknown=EXCLUDE,
                data_key="certificate",
                allow_none=True
            )
    r""" The certificate field of the security_cluster_network_certificates_response_records. """

    node = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.node", "NodeSchema"),
                unknown=EXCLUDE,
                data_key="node",
                allow_none=True
            )
    r""" The node field of the security_cluster_network_certificates_response_records. """

    @property
    def resource(self):
        return SecurityClusterNetworkCertificatesResponseRecords

    gettable_fields = [
        "links",
        "certificate.links",
        "certificate.name",
        "certificate.uuid",
        "node.links",
        "node.name",
        "node.uuid",
    ]
    """links,certificate.links,certificate.name,certificate.uuid,node.links,node.name,node.uuid,"""

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


class SecurityClusterNetworkCertificatesResponseRecords(Resource):

    _schema = SecurityClusterNetworkCertificatesResponseRecordsSchema
