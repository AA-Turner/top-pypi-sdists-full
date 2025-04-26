r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Nas", "NasSchema"]
__pdoc__ = {
    "NasSchema.resource": False,
    "NasSchema.opts": False,
    "Nas": False,
}


class NasSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Nas object"""

    application_components = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.nas_application_components.NasApplicationComponentsSchema", unknown=EXCLUDE, allow_none=True), data_key="application_components", allow_none=True)
    r""" The application_components field of the nas. """

    cifs_access = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.app_cifs_access.AppCifsAccessSchema", unknown=EXCLUDE, allow_none=True), data_key="cifs_access", allow_none=True)
    r""" The list of CIFS access controls. You must provide either 'user_or_group' or 'access' to enable CIFS access. """

    cifs_share_name = marshmallow_fields.Str(data_key="cifs_share_name", allow_none=True)
    r""" The name of the CIFS share. Usage: &lt;Share&gt; """

    exclude_aggregates = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.nas_exclude_aggregates.NasExcludeAggregatesSchema", unknown=EXCLUDE, allow_none=True), data_key="exclude_aggregates", allow_none=True)
    r""" The exclude_aggregates field of the nas. """

    nfs_access = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.app_nfs_access.AppNfsAccessSchema", unknown=EXCLUDE, allow_none=True), data_key="nfs_access", allow_none=True)
    r""" The list of NFS access controls. You must provide either 'host' or 'access' to enable NFS access. """

    protection_type = marshmallow_fields.Nested("netapp_ontap.models.nas_protection_type.NasProtectionTypeSchema", unknown=EXCLUDE, data_key="protection_type", allow_none=True)
    r""" The protection_type field of the nas. """

    @property
    def resource(self):
        return Nas

    gettable_fields = [
        "application_components",
        "cifs_access",
        "cifs_share_name",
        "exclude_aggregates",
        "nfs_access",
        "protection_type",
    ]
    """application_components,cifs_access,cifs_share_name,exclude_aggregates,nfs_access,protection_type,"""

    patchable_fields = [
        "application_components",
        "protection_type",
    ]
    """application_components,protection_type,"""

    postable_fields = [
        "application_components",
        "cifs_access",
        "cifs_share_name",
        "exclude_aggregates",
        "nfs_access",
        "protection_type",
    ]
    """application_components,cifs_access,cifs_share_name,exclude_aggregates,nfs_access,protection_type,"""


class Nas(Resource):

    _schema = NasSchema
