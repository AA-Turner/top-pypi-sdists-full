r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AdDomainDelete", "AdDomainDeleteSchema"]
__pdoc__ = {
    "AdDomainDeleteSchema.resource": False,
    "AdDomainDeleteSchema.opts": False,
    "AdDomainDelete": False,
}


class AdDomainDeleteSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AdDomainDelete object"""

    fqdn = marshmallow_fields.Str(data_key="fqdn", allow_none=True)
    r""" The fully qualified domain name of the Windows Active Directory to which this CIFS server belongs. A CIFS server appears as a member of Windows server object in the Active Directory store. POST and PATCH only.

Example: example.com """

    organizational_unit = marshmallow_fields.Str(data_key="organizational_unit", allow_none=True)
    r""" Specifies the organizational unit within the Active Directory domain to associate with the CIFS server. POST and PATCH only. """

    password = marshmallow_fields.Str(data_key="password", allow_none=True)
    r""" The account password used to add this CIFS server to the Active Directory. This is not audited. """

    user = marshmallow_fields.Str(data_key="user", allow_none=True)
    r""" The user account used to add this CIFS server to the Active Directory. """

    @property
    def resource(self):
        return AdDomainDelete

    gettable_fields = [
        "fqdn",
        "organizational_unit",
    ]
    """fqdn,organizational_unit,"""

    patchable_fields = [
        "fqdn",
        "organizational_unit",
        "password",
        "user",
    ]
    """fqdn,organizational_unit,password,user,"""

    postable_fields = [
        "fqdn",
        "organizational_unit",
        "password",
        "user",
    ]
    """fqdn,organizational_unit,password,user,"""


class AdDomainDelete(Resource):

    _schema = AdDomainDeleteSchema
