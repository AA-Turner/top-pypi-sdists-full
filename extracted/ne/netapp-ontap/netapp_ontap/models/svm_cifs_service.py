r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmCifsService", "SvmCifsServiceSchema"]
__pdoc__ = {
    "SvmCifsServiceSchema.resource": False,
    "SvmCifsServiceSchema.opts": False,
    "SvmCifsService": False,
}


class SvmCifsServiceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmCifsService object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the svm_cifs_service. """

    ad_domain = marshmallow_fields.Nested("netapp_ontap.models.ad_domain_svm.AdDomainSvmSchema", unknown=EXCLUDE, data_key="ad_domain", allow_none=True)
    r""" The ad_domain field of the svm_cifs_service. """

    allowed = marshmallow_fields.Boolean(data_key="allowed", allow_none=True)
    r""" If this is set to true, an SVM administrator can manage the CIFS service. If it is false, only the cluster administrator can manage the service. """

    auth_style = marshmallow_fields.Str(data_key="auth-style", allow_none=True)
    r""" Authentication type.

Valid choices:

* domain
* workgroup """

    domain_workgroup = marshmallow_fields.Str(data_key="domain_workgroup", allow_none=True)
    r""" The NetBIOS name of the domain or workgroup associated with the CIFS server. """

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" If allowed, setting to true enables the CIFS service. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The NetBIOS name of the CIFS server.

Example: CIFS1 """

    workgroup = marshmallow_fields.Str(data_key="workgroup", allow_none=True)
    r""" The workgroup name.

Example: workgrp1 """

    @property
    def resource(self):
        return SvmCifsService

    gettable_fields = [
        "links",
        "ad_domain",
        "allowed",
        "auth_style",
        "domain_workgroup",
        "enabled",
        "name",
        "workgroup",
    ]
    """links,ad_domain,allowed,auth_style,domain_workgroup,enabled,name,workgroup,"""

    patchable_fields = [
        "allowed",
        "workgroup",
    ]
    """allowed,workgroup,"""

    postable_fields = [
        "ad_domain",
        "allowed",
        "enabled",
        "name",
        "workgroup",
    ]
    """ad_domain,allowed,enabled,name,workgroup,"""


class SvmCifsService(Resource):

    _schema = SvmCifsServiceSchema
