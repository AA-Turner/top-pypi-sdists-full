r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationStatisticsComponentsStorageService", "ApplicationStatisticsComponentsStorageServiceSchema"]
__pdoc__ = {
    "ApplicationStatisticsComponentsStorageServiceSchema.resource": False,
    "ApplicationStatisticsComponentsStorageServiceSchema.opts": False,
    "ApplicationStatisticsComponentsStorageService": False,
}


class ApplicationStatisticsComponentsStorageServiceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationStatisticsComponentsStorageService object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The storage service name. AFF systems support the extreme storage service. All other systems only support value. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The storage service UUID. """

    @property
    def resource(self):
        return ApplicationStatisticsComponentsStorageService

    gettable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ApplicationStatisticsComponentsStorageService(Resource):

    _schema = ApplicationStatisticsComponentsStorageServiceSchema
