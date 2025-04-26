r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Rfc2307bis", "Rfc2307bisSchema"]
__pdoc__ = {
    "Rfc2307bisSchema.resource": False,
    "Rfc2307bisSchema.opts": False,
    "Rfc2307bis": False,
}


class Rfc2307bisSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Rfc2307bis object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Indicates whether RFC 2307bis is enabled for the client schema.

Example: false """

    group_of_unique_names = marshmallow_fields.Str(data_key="group_of_unique_names", allow_none=True)
    r""" RFC 2307bis groupOfUniqueNames object class.

Example: groupOfUniqueNames """

    maximum_groups = Size(data_key="maximum_groups", allow_none=True)
    r""" Maximum number of groups supported when RFC 2307bis is enabled.

Example: 256 """

    unique_member = marshmallow_fields.Str(data_key="unique_member", allow_none=True)
    r""" RFC 2307bis uniqueMember attribute.

Example: uniqueMember """

    @property
    def resource(self):
        return Rfc2307bis

    gettable_fields = [
        "enabled",
        "group_of_unique_names",
        "maximum_groups",
        "unique_member",
    ]
    """enabled,group_of_unique_names,maximum_groups,unique_member,"""

    patchable_fields = [
        "enabled",
        "group_of_unique_names",
        "maximum_groups",
        "unique_member",
    ]
    """enabled,group_of_unique_names,maximum_groups,unique_member,"""

    postable_fields = [
    ]
    """"""


class Rfc2307bis(Resource):

    _schema = Rfc2307bisSchema
