r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationLunMappingObjectIgroup", "ApplicationLunMappingObjectIgroupSchema"]
__pdoc__ = {
    "ApplicationLunMappingObjectIgroupSchema.resource": False,
    "ApplicationLunMappingObjectIgroupSchema.opts": False,
    "ApplicationLunMappingObjectIgroup": False,
}


class ApplicationLunMappingObjectIgroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationLunMappingObjectIgroup object"""

    initiators = marshmallow_fields.List(marshmallow_fields.Str, data_key="initiators", allow_none=True)
    r""" The initiators field of the application_lun_mapping_object_igroup. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Igroup name """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Igroup UUID """

    @property
    def resource(self):
        return ApplicationLunMappingObjectIgroup

    gettable_fields = [
        "initiators",
        "name",
        "uuid",
    ]
    """initiators,name,uuid,"""

    patchable_fields = [
        "initiators",
    ]
    """initiators,"""

    postable_fields = [
        "initiators",
    ]
    """initiators,"""


class ApplicationLunMappingObjectIgroup(Resource):

    _schema = ApplicationLunMappingObjectIgroupSchema
