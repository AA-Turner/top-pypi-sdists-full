r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ZappNvmeComponentsPerformance", "ZappNvmeComponentsPerformanceSchema"]
__pdoc__ = {
    "ZappNvmeComponentsPerformanceSchema.resource": False,
    "ZappNvmeComponentsPerformanceSchema.opts": False,
    "ZappNvmeComponentsPerformance": False,
}


class ZappNvmeComponentsPerformanceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ZappNvmeComponentsPerformance object"""

    storage_service = marshmallow_fields.Nested("netapp_ontap.models.nas_application_components_storage_service.NasApplicationComponentsStorageServiceSchema", unknown=EXCLUDE, data_key="storage_service", allow_none=True)
    r""" The storage_service field of the zapp_nvme_components_performance. """

    @property
    def resource(self):
        return ZappNvmeComponentsPerformance

    gettable_fields = [
        "storage_service",
    ]
    """storage_service,"""

    patchable_fields = [
        "storage_service",
    ]
    """storage_service,"""

    postable_fields = [
        "storage_service",
    ]
    """storage_service,"""


class ZappNvmeComponentsPerformance(Resource):

    _schema = ZappNvmeComponentsPerformanceSchema
