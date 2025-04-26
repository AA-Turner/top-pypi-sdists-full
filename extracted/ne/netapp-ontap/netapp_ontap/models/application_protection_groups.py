r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationProtectionGroups", "ApplicationProtectionGroupsSchema"]
__pdoc__ = {
    "ApplicationProtectionGroupsSchema.resource": False,
    "ApplicationProtectionGroupsSchema.opts": False,
    "ApplicationProtectionGroups": False,
}


class ApplicationProtectionGroupsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationProtectionGroups object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Protection group name """

    rpo = marshmallow_fields.Nested("netapp_ontap.models.application_protection_groups_rpo.ApplicationProtectionGroupsRpoSchema", unknown=EXCLUDE, data_key="rpo", allow_none=True)
    r""" The rpo field of the application_protection_groups. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Protection group UUID """

    @property
    def resource(self):
        return ApplicationProtectionGroups

    gettable_fields = [
        "name",
        "rpo",
        "uuid",
    ]
    """name,rpo,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ApplicationProtectionGroups(Resource):

    _schema = ApplicationProtectionGroupsSchema
