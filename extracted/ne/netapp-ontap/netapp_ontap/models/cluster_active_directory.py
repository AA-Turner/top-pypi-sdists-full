r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterActiveDirectory", "ClusterActiveDirectorySchema"]
__pdoc__ = {
    "ClusterActiveDirectorySchema.resource": False,
    "ClusterActiveDirectorySchema.opts": False,
    "ClusterActiveDirectory": False,
}


class ClusterActiveDirectorySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterActiveDirectory object"""

    force_account_overwrite = marshmallow_fields.Boolean(data_key="force_account_overwrite", allow_none=True)
    r""" If set to true and a machine account exists with the same name as specified in "name" in Active Directory, it is overwritten and reused.

Example: false """

    fqdn = marshmallow_fields.Str(data_key="fqdn", allow_none=True)
    r""" Fully qualified domain name.

Example: server1.com """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Active Directory account NetBIOS name.

Example: account1 """

    organizational_unit = marshmallow_fields.Str(data_key="organizational_unit", allow_none=True)
    r""" Organizational unit under which the Active Directory account is created.

Example: CN=Test """

    password = marshmallow_fields.Str(data_key="password", allow_none=True)
    r""" Administrator password required for Active Directory account creation, modification, and deletion.

Example: testpwd """

    username = marshmallow_fields.Str(data_key="username", allow_none=True)
    r""" Administrator username required for Active Directory account creation, modification, and deletion.

Example: admin """

    @property
    def resource(self):
        return ClusterActiveDirectory

    gettable_fields = [
        "fqdn",
        "name",
        "organizational_unit",
    ]
    """fqdn,name,organizational_unit,"""

    patchable_fields = [
        "force_account_overwrite",
        "fqdn",
        "name",
        "organizational_unit",
        "password",
        "username",
    ]
    """force_account_overwrite,fqdn,name,organizational_unit,password,username,"""

    postable_fields = [
        "force_account_overwrite",
        "fqdn",
        "name",
        "organizational_unit",
        "password",
        "username",
    ]
    """force_account_overwrite,fqdn,name,organizational_unit,password,username,"""


class ClusterActiveDirectory(Resource):

    _schema = ClusterActiveDirectorySchema
