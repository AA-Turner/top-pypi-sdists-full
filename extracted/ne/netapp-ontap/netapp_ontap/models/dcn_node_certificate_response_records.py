r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DcnNodeCertificateResponseRecords", "DcnNodeCertificateResponseRecordsSchema"]
__pdoc__ = {
    "DcnNodeCertificateResponseRecordsSchema.resource": False,
    "DcnNodeCertificateResponseRecordsSchema.opts": False,
    "DcnNodeCertificateResponseRecords": False,
}

class DcnNodeCertificateResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnNodeCertificateResponseRecords object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                unknown=EXCLUDE,
                data_key="_links",
                allow_none=True
            )
    r""" The links field of the dcn_node_certificate_response_records. """

    dcn_cert_name = marshmallow_fields.Str(data_key="dcn-cert-name", allow_none=True)
    r""" Certificate name used by DCN.

Example: dcn-node1-cert """

    dcn_node_name = marshmallow_fields.Str(data_key="dcn-node-name", allow_none=True)
    r""" The DCN node name.

Example: dcn-node1 """

    @property
    def resource(self):
        return DcnNodeCertificateResponseRecords

    gettable_fields = [
        "links",
        "dcn_cert_name",
        "dcn_node_name",
    ]
    """links,dcn_cert_name,dcn_node_name,"""

    patchable_fields = [
        "dcn_cert_name",
    ]
    """dcn_cert_name,"""

    postable_fields = [
    ]
    """"""


class DcnNodeCertificateResponseRecords(Resource):

    _schema = DcnNodeCertificateResponseRecordsSchema
