r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationNvmeAccess", "ApplicationNvmeAccessSchema"]
__pdoc__ = {
    "ApplicationNvmeAccessSchema.resource": False,
    "ApplicationNvmeAccessSchema.opts": False,
    "ApplicationNvmeAccess": False,
}


class ApplicationNvmeAccessSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationNvmeAccess object"""

    backing_storage = marshmallow_fields.Nested("netapp_ontap.models.application_nvme_access_backing_storage.ApplicationNvmeAccessBackingStorageSchema", unknown=EXCLUDE, data_key="backing_storage", allow_none=True)
    r""" The backing_storage field of the application_nvme_access. """

    is_clone = marshmallow_fields.Boolean(data_key="is_clone", allow_none=True)
    r""" Clone """

    subsystem_map = marshmallow_fields.Nested("netapp_ontap.models.application_subsystem_map_object.ApplicationSubsystemMapObjectSchema", unknown=EXCLUDE, data_key="subsystem_map", allow_none=True)
    r""" Subsystem map object """

    @property
    def resource(self):
        return ApplicationNvmeAccess

    gettable_fields = [
        "backing_storage",
        "is_clone",
        "subsystem_map",
    ]
    """backing_storage,is_clone,subsystem_map,"""

    patchable_fields = [
        "subsystem_map",
    ]
    """subsystem_map,"""

    postable_fields = [
        "subsystem_map",
    ]
    """subsystem_map,"""


class ApplicationNvmeAccess(Resource):

    _schema = ApplicationNvmeAccessSchema
