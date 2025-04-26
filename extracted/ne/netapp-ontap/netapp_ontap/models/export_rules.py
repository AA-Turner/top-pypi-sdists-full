r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ExportRules", "ExportRulesSchema"]
__pdoc__ = {
    "ExportRulesSchema.resource": False,
    "ExportRulesSchema.opts": False,
    "ExportRules": False,
}


class ExportRulesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ExportRules object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the export_rules. """

    allow_device_creation = marshmallow_fields.Boolean(data_key="allow_device_creation", allow_none=True)
    r""" Specifies whether or not device creation is allowed. """

    allow_suid = marshmallow_fields.Boolean(data_key="allow_suid", allow_none=True)
    r""" Specifies whether or not SetUID bits in SETATTR Op is to be honored. """

    anonymous_user = marshmallow_fields.Str(data_key="anonymous_user", allow_none=True)
    r""" User ID To Which Anonymous Users Are Mapped. """

    chown_mode = marshmallow_fields.Str(data_key="chown_mode", allow_none=True)
    r""" Specifies who is authorized to change the ownership mode of a file.

Valid choices:

* restricted
* unrestricted """

    clients = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.export_clients.ExportClientsSchema", unknown=EXCLUDE, allow_none=True), data_key="clients", allow_none=True)
    r""" Array of client matches """

    index = Size(data_key="index", allow_none=True)
    r""" Index of the rule within the export policy. """

    ntfs_unix_security = marshmallow_fields.Str(data_key="ntfs_unix_security", allow_none=True)
    r""" NTFS export UNIX security options.

Valid choices:

* fail
* ignore """

    protocols = marshmallow_fields.List(marshmallow_fields.Str, data_key="protocols", allow_none=True)
    r""" The protocols field of the export_rules. """

    ro_rule = marshmallow_fields.List(marshmallow_fields.Str, data_key="ro_rule", allow_none=True)
    r""" Authentication flavors that the read-only access rule governs """

    rw_rule = marshmallow_fields.List(marshmallow_fields.Str, data_key="rw_rule", allow_none=True)
    r""" Authentication flavors that the read/write access rule governs """

    superuser = marshmallow_fields.List(marshmallow_fields.Str, data_key="superuser", allow_none=True)
    r""" Authentication flavors that the superuser security type governs """

    @property
    def resource(self):
        return ExportRules

    gettable_fields = [
        "links",
        "allow_device_creation",
        "allow_suid",
        "anonymous_user",
        "chown_mode",
        "clients",
        "index",
        "ntfs_unix_security",
        "protocols",
        "ro_rule",
        "rw_rule",
        "superuser",
    ]
    """links,allow_device_creation,allow_suid,anonymous_user,chown_mode,clients,index,ntfs_unix_security,protocols,ro_rule,rw_rule,superuser,"""

    patchable_fields = [
        "allow_device_creation",
        "allow_suid",
        "anonymous_user",
        "chown_mode",
        "clients",
        "index",
        "ntfs_unix_security",
        "protocols",
        "ro_rule",
        "rw_rule",
        "superuser",
    ]
    """allow_device_creation,allow_suid,anonymous_user,chown_mode,clients,index,ntfs_unix_security,protocols,ro_rule,rw_rule,superuser,"""

    postable_fields = [
        "allow_device_creation",
        "allow_suid",
        "anonymous_user",
        "chown_mode",
        "clients",
        "index",
        "ntfs_unix_security",
        "protocols",
        "ro_rule",
        "rw_rule",
        "superuser",
    ]
    """allow_device_creation,allow_suid,anonymous_user,chown_mode,clients,index,ntfs_unix_security,protocols,ro_rule,rw_rule,superuser,"""


class ExportRules(Resource):

    _schema = ExportRulesSchema
