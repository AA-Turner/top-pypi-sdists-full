r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationComponentSnapshotRestoreComponent", "ApplicationComponentSnapshotRestoreComponentSchema"]
__pdoc__ = {
    "ApplicationComponentSnapshotRestoreComponentSchema.resource": False,
    "ApplicationComponentSnapshotRestoreComponentSchema.opts": False,
    "ApplicationComponentSnapshotRestoreComponent": False,
}


class ApplicationComponentSnapshotRestoreComponentSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationComponentSnapshotRestoreComponent object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the application_component_snapshot_restore_component. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Application Component UUID. Valid in URL or POST """

    @property
    def resource(self):
        return ApplicationComponentSnapshotRestoreComponent

    gettable_fields = [
        "links",
        "uuid",
    ]
    """links,uuid,"""

    patchable_fields = [
        "uuid",
    ]
    """uuid,"""

    postable_fields = [
        "uuid",
    ]
    """uuid,"""


class ApplicationComponentSnapshotRestoreComponent(Resource):

    _schema = ApplicationComponentSnapshotRestoreComponentSchema
