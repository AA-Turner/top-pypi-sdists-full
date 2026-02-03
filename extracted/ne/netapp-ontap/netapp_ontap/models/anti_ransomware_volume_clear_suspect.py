r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["AntiRansomwareVolumeClearSuspect", "AntiRansomwareVolumeClearSuspectSchema"]
__pdoc__ = {
    "AntiRansomwareVolumeClearSuspectSchema.resource": False,
    "AntiRansomwareVolumeClearSuspectSchema.opts": False,
    "AntiRansomwareVolumeClearSuspect": False,
}

class AntiRansomwareVolumeClearSuspectSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AntiRansomwareVolumeClearSuspect object"""

    phase = marshmallow_fields.Str(data_key="phase", allow_none=True)
    r""" Clear suspect phase.

Valid choices:

* file_extension_processing
* snapshot_processing
* done """

    start_time = ImpreciseDateTime(data_key="start_time", allow_none=True)
    r""" Clear suspect start time. """

    @property
    def resource(self):
        return AntiRansomwareVolumeClearSuspect

    gettable_fields = [
        "phase",
        "start_time",
    ]
    """phase,start_time,"""

    patchable_fields = [
        "phase",
        "start_time",
    ]
    """phase,start_time,"""

    postable_fields = [
        "phase",
        "start_time",
    ]
    """phase,start_time,"""


class AntiRansomwareVolumeClearSuspect(Resource):

    _schema = AntiRansomwareVolumeClearSuspectSchema
