r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationProtectionGroupsRpo", "ApplicationProtectionGroupsRpoSchema"]
__pdoc__ = {
    "ApplicationProtectionGroupsRpoSchema.resource": False,
    "ApplicationProtectionGroupsRpoSchema.opts": False,
    "ApplicationProtectionGroupsRpo": False,
}


class ApplicationProtectionGroupsRpoSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationProtectionGroupsRpo object"""

    local = marshmallow_fields.Nested("netapp_ontap.models.application_protection_groups_rpo_local.ApplicationProtectionGroupsRpoLocalSchema", unknown=EXCLUDE, data_key="local", allow_none=True)
    r""" The local field of the application_protection_groups_rpo. """

    remote = marshmallow_fields.Nested("netapp_ontap.models.application_protection_groups_rpo_remote.ApplicationProtectionGroupsRpoRemoteSchema", unknown=EXCLUDE, data_key="remote", allow_none=True)
    r""" The remote field of the application_protection_groups_rpo. """

    @property
    def resource(self):
        return ApplicationProtectionGroupsRpo

    gettable_fields = [
        "local",
        "remote",
    ]
    """local,remote,"""

    patchable_fields = [
        "local",
        "remote",
    ]
    """local,remote,"""

    postable_fields = [
        "local",
        "remote",
    ]
    """local,remote,"""


class ApplicationProtectionGroupsRpo(Resource):

    _schema = ApplicationProtectionGroupsRpoSchema
