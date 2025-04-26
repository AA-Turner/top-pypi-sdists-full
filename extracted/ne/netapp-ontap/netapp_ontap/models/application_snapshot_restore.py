r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationSnapshotRestore", "ApplicationSnapshotRestoreSchema"]
__pdoc__ = {
    "ApplicationSnapshotRestoreSchema.resource": False,
    "ApplicationSnapshotRestoreSchema.opts": False,
    "ApplicationSnapshotRestore": False,
}


class ApplicationSnapshotRestoreSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationSnapshotRestore object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the application_snapshot_restore. """

    application = marshmallow_fields.Nested("netapp_ontap.models.application_snapshot_restore_application.ApplicationSnapshotRestoreApplicationSchema", unknown=EXCLUDE, data_key="application", allow_none=True)
    r""" The application field of the application_snapshot_restore. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The snapshot UUID. Valid in URL or POST. """

    @property
    def resource(self):
        return ApplicationSnapshotRestore

    gettable_fields = [
        "links",
        "application",
        "uuid",
    ]
    """links,application,uuid,"""

    patchable_fields = [
        "application",
        "uuid",
    ]
    """application,uuid,"""

    postable_fields = [
        "application",
        "uuid",
    ]
    """application,uuid,"""


class ApplicationSnapshotRestore(Resource):

    _schema = ApplicationSnapshotRestoreSchema
