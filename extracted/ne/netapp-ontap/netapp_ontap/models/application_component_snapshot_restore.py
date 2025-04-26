r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationComponentSnapshotRestore", "ApplicationComponentSnapshotRestoreSchema"]
__pdoc__ = {
    "ApplicationComponentSnapshotRestoreSchema.resource": False,
    "ApplicationComponentSnapshotRestoreSchema.opts": False,
    "ApplicationComponentSnapshotRestore": False,
}


class ApplicationComponentSnapshotRestoreSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationComponentSnapshotRestore object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the application_component_snapshot_restore. """

    application = marshmallow_fields.Nested("netapp_ontap.models.application_component_snapshot_restore_application.ApplicationComponentSnapshotRestoreApplicationSchema", unknown=EXCLUDE, data_key="application", allow_none=True)
    r""" The application field of the application_component_snapshot_restore. """

    component = marshmallow_fields.Nested("netapp_ontap.models.application_component_snapshot_restore_component.ApplicationComponentSnapshotRestoreComponentSchema", unknown=EXCLUDE, data_key="component", allow_none=True)
    r""" The component field of the application_component_snapshot_restore. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Snapshot UUID. Valid in URL or POST """

    @property
    def resource(self):
        return ApplicationComponentSnapshotRestore

    gettable_fields = [
        "links",
        "application",
        "component",
        "uuid",
    ]
    """links,application,component,uuid,"""

    patchable_fields = [
        "application",
        "component",
        "uuid",
    ]
    """application,component,uuid,"""

    postable_fields = [
        "application",
        "component",
        "uuid",
    ]
    """application,component,uuid,"""


class ApplicationComponentSnapshotRestore(Resource):

    _schema = ApplicationComponentSnapshotRestoreSchema
