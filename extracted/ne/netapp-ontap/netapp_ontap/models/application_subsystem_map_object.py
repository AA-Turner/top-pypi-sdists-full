r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationSubsystemMapObject", "ApplicationSubsystemMapObjectSchema"]
__pdoc__ = {
    "ApplicationSubsystemMapObjectSchema.resource": False,
    "ApplicationSubsystemMapObjectSchema.opts": False,
    "ApplicationSubsystemMapObject": False,
}


class ApplicationSubsystemMapObjectSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationSubsystemMapObject object"""

    anagrpid = marshmallow_fields.Str(data_key="anagrpid", allow_none=True)
    r""" Subsystem ANA group ID """

    nsid = marshmallow_fields.Str(data_key="nsid", allow_none=True)
    r""" Subsystem namespace ID """

    subsystem = marshmallow_fields.Nested("netapp_ontap.models.application_nvme_access_subsystem_map_subsystem.ApplicationNvmeAccessSubsystemMapSubsystemSchema", unknown=EXCLUDE, data_key="subsystem", allow_none=True)
    r""" The subsystem field of the application_subsystem_map_object. """

    @property
    def resource(self):
        return ApplicationSubsystemMapObject

    gettable_fields = [
        "anagrpid",
        "nsid",
        "subsystem",
    ]
    """anagrpid,nsid,subsystem,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ApplicationSubsystemMapObject(Resource):

    _schema = ApplicationSubsystemMapObjectSchema
