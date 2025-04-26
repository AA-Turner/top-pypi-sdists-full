r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmDns", "SvmDnsSchema"]
__pdoc__ = {
    "SvmDnsSchema.resource": False,
    "SvmDnsSchema.opts": False,
    "SvmDns": False,
}


class SvmDnsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmDns object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the svm_dns. """

    domains = marshmallow_fields.List(marshmallow_fields.Str, data_key="domains", allow_none=True)
    r""" The domains field of the svm_dns. """

    servers = marshmallow_fields.List(marshmallow_fields.Str, data_key="servers", allow_none=True)
    r""" The servers field of the svm_dns. """

    @property
    def resource(self):
        return SvmDns

    gettable_fields = [
        "links",
        "domains",
        "servers",
    ]
    """links,domains,servers,"""

    patchable_fields = [
        "domains",
        "servers",
    ]
    """domains,servers,"""

    postable_fields = [
        "domains",
        "servers",
    ]
    """domains,servers,"""


class SvmDns(Resource):

    _schema = SvmDnsSchema
