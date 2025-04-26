r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AuditEvents", "AuditEventsSchema"]
__pdoc__ = {
    "AuditEventsSchema.resource": False,
    "AuditEventsSchema.opts": False,
    "AuditEvents": False,
}


class AuditEventsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AuditEvents object"""

    async_delete = marshmallow_fields.Boolean(data_key="async_delete", allow_none=True)
    r""" Volume file async delete events """

    audit_policy_change = marshmallow_fields.Boolean(data_key="audit_policy_change", allow_none=True)
    r""" Audit policy change events """

    authorization_policy = marshmallow_fields.Boolean(data_key="authorization_policy", allow_none=True)
    r""" Authorization policy change events """

    cap_staging = marshmallow_fields.Boolean(data_key="cap_staging", allow_none=True)
    r""" Central access policy staging events """

    cifs_logon_logoff = marshmallow_fields.Boolean(data_key="cifs_logon_logoff", allow_none=True)
    r""" CIFS logon and logoff events """

    file_operations = marshmallow_fields.Boolean(data_key="file_operations", allow_none=True)
    r""" File operation events """

    file_share = marshmallow_fields.Boolean(data_key="file_share", allow_none=True)
    r""" File share category events """

    security_group = marshmallow_fields.Boolean(data_key="security_group", allow_none=True)
    r""" Local security group management events """

    user_account = marshmallow_fields.Boolean(data_key="user_account", allow_none=True)
    r""" Local user account management events """

    @property
    def resource(self):
        return AuditEvents

    gettable_fields = [
        "async_delete",
        "audit_policy_change",
        "authorization_policy",
        "cap_staging",
        "cifs_logon_logoff",
        "file_operations",
        "file_share",
        "security_group",
        "user_account",
    ]
    """async_delete,audit_policy_change,authorization_policy,cap_staging,cifs_logon_logoff,file_operations,file_share,security_group,user_account,"""

    patchable_fields = [
        "async_delete",
        "audit_policy_change",
        "authorization_policy",
        "cap_staging",
        "cifs_logon_logoff",
        "file_operations",
        "file_share",
        "security_group",
        "user_account",
    ]
    """async_delete,audit_policy_change,authorization_policy,cap_staging,cifs_logon_logoff,file_operations,file_share,security_group,user_account,"""

    postable_fields = [
        "async_delete",
        "audit_policy_change",
        "authorization_policy",
        "cap_staging",
        "cifs_logon_logoff",
        "file_operations",
        "file_share",
        "security_group",
        "user_account",
    ]
    """async_delete,audit_policy_change,authorization_policy,cap_staging,cifs_logon_logoff,file_operations,file_share,security_group,user_account,"""


class AuditEvents(Resource):

    _schema = AuditEventsSchema
