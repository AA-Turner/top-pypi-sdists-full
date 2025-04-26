r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationSanAccess", "ApplicationSanAccessSchema"]
__pdoc__ = {
    "ApplicationSanAccessSchema.resource": False,
    "ApplicationSanAccessSchema.opts": False,
    "ApplicationSanAccess": False,
}


class ApplicationSanAccessSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationSanAccess object"""

    backing_storage = marshmallow_fields.Nested("netapp_ontap.models.application_san_access_backing_storage.ApplicationSanAccessBackingStorageSchema", unknown=EXCLUDE, data_key="backing_storage", allow_none=True)
    r""" The backing_storage field of the application_san_access. """

    is_clone = marshmallow_fields.Boolean(data_key="is_clone", allow_none=True)
    r""" Clone """

    lun_mappings = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.application_lun_mapping_object.ApplicationLunMappingObjectSchema", unknown=EXCLUDE, allow_none=True), data_key="lun_mappings", allow_none=True)
    r""" The lun_mappings field of the application_san_access. """

    serial_number = marshmallow_fields.Str(data_key="serial_number", allow_none=True)
    r""" LUN serial number """

    @property
    def resource(self):
        return ApplicationSanAccess

    gettable_fields = [
        "backing_storage",
        "is_clone",
        "lun_mappings",
        "serial_number",
    ]
    """backing_storage,is_clone,lun_mappings,serial_number,"""

    patchable_fields = [
        "lun_mappings",
    ]
    """lun_mappings,"""

    postable_fields = [
        "lun_mappings",
    ]
    """lun_mappings,"""


class ApplicationSanAccess(Resource):

    _schema = ApplicationSanAccessSchema
