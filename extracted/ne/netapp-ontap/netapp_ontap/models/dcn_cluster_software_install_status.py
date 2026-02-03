r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DcnClusterSoftwareInstallStatus", "DcnClusterSoftwareInstallStatusSchema"]
__pdoc__ = {
    "DcnClusterSoftwareInstallStatusSchema.resource": False,
    "DcnClusterSoftwareInstallStatusSchema.opts": False,
    "DcnClusterSoftwareInstallStatus": False,
}

class DcnClusterSoftwareInstallStatusSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnClusterSoftwareInstallStatus object"""

    active = marshmallow_fields.Boolean(data_key="active", allow_none=True)
    r""" Upgrade status.

Example: false """

    duration = marshmallow_fields.Str(data_key="duration", allow_none=True)
    r""" Upgrade duration in ISO 8601 duration format.

Example: PT2D2H2M2S """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Upgrade status.

Example: Upgrading node1 """

    scope = marshmallow_fields.Str(data_key="scope", allow_none=True)
    r""" Scope of the upgrade.

Valid choices:

* cluster
* node """

    start_time = ImpreciseDateTime(data_key="start_time", allow_none=True)
    r""" Upgrade start time.

Example: 2025-05-20T19:00:00.000+0000 """

    @property
    def resource(self):
        return DcnClusterSoftwareInstallStatus

    gettable_fields = [
        "active",
        "duration",
        "message",
        "scope",
        "start_time",
    ]
    """active,duration,message,scope,start_time,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DcnClusterSoftwareInstallStatus(Resource):

    _schema = DcnClusterSoftwareInstallStatusSchema
