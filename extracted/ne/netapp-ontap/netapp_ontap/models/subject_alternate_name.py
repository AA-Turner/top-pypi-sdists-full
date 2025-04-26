r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SubjectAlternateName", "SubjectAlternateNameSchema"]
__pdoc__ = {
    "SubjectAlternateNameSchema.resource": False,
    "SubjectAlternateNameSchema.opts": False,
    "SubjectAlternateName": False,
}


class SubjectAlternateNameSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SubjectAlternateName object"""

    dns = marshmallow_fields.List(marshmallow_fields.Str, data_key="dns", allow_none=True)
    r""" A list of DNS names for Subject Alternate name extension. """

    email = marshmallow_fields.List(marshmallow_fields.Str, data_key="email", allow_none=True)
    r""" A list of email addresses for Subject Alternate name extension """

    ip = marshmallow_fields.List(marshmallow_fields.Str, data_key="ip", allow_none=True)
    r""" A list of IP addresses for Subject Alternate name extension. """

    uri = marshmallow_fields.List(marshmallow_fields.Str, data_key="uri", allow_none=True)
    r""" A list of URIs for Subject Alternate name extension. """

    @property
    def resource(self):
        return SubjectAlternateName

    gettable_fields = [
        "dns",
        "email",
        "ip",
        "uri",
    ]
    """dns,email,ip,uri,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "dns",
        "email",
        "ip",
        "uri",
    ]
    """dns,email,ip,uri,"""


class SubjectAlternateName(Resource):

    _schema = SubjectAlternateNameSchema
