r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["HealthMonitorPolicyFields", "HealthMonitorPolicyFieldsSchema"]
__pdoc__ = {
    "HealthMonitorPolicyFieldsSchema.resource": False,
    "HealthMonitorPolicyFieldsSchema.opts": False,
    "HealthMonitorPolicyFields": False,
}


class HealthMonitorPolicyFieldsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the HealthMonitorPolicyFields object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Indicates whether health monitor is enabled. """

    manage_volume_offline = marshmallow_fields.Boolean(data_key="manage_volume_offline", allow_none=True)
    r""" Indicates whether the health monitor manages the volume offline operation. """

    @property
    def resource(self):
        return HealthMonitorPolicyFields

    gettable_fields = [
        "enabled",
        "manage_volume_offline",
    ]
    """enabled,manage_volume_offline,"""

    patchable_fields = [
        "enabled",
        "manage_volume_offline",
    ]
    """enabled,manage_volume_offline,"""

    postable_fields = [
    ]
    """"""


class HealthMonitorPolicyFields(Resource):

    _schema = HealthMonitorPolicyFieldsSchema
