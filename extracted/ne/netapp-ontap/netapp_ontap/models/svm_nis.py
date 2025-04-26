r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmNis", "SvmNisSchema"]
__pdoc__ = {
    "SvmNisSchema.resource": False,
    "SvmNisSchema.opts": False,
    "SvmNis": False,
}


class SvmNisSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmNis object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the svm_nis. """

    domain = marshmallow_fields.Str(data_key="domain", allow_none=True)
    r""" The domain field of the svm_nis. """

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Enable NIS? Setting to true creates a configuration if not already created. """

    servers = marshmallow_fields.List(marshmallow_fields.Str, data_key="servers", allow_none=True)
    r""" The servers field of the svm_nis. """

    @property
    def resource(self):
        return SvmNis

    gettable_fields = [
        "links",
        "domain",
        "enabled",
        "servers",
    ]
    """links,domain,enabled,servers,"""

    patchable_fields = [
        "domain",
        "enabled",
        "servers",
    ]
    """domain,enabled,servers,"""

    postable_fields = [
        "domain",
        "enabled",
        "servers",
    ]
    """domain,enabled,servers,"""


class SvmNis(Resource):

    _schema = SvmNisSchema
