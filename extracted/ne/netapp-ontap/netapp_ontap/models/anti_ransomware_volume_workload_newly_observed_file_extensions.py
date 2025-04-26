r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AntiRansomwareVolumeWorkloadNewlyObservedFileExtensions", "AntiRansomwareVolumeWorkloadNewlyObservedFileExtensionsSchema"]
__pdoc__ = {
    "AntiRansomwareVolumeWorkloadNewlyObservedFileExtensionsSchema.resource": False,
    "AntiRansomwareVolumeWorkloadNewlyObservedFileExtensionsSchema.opts": False,
    "AntiRansomwareVolumeWorkloadNewlyObservedFileExtensions": False,
}


class AntiRansomwareVolumeWorkloadNewlyObservedFileExtensionsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AntiRansomwareVolumeWorkloadNewlyObservedFileExtensions object"""

    count = Size(data_key="count", allow_none=True)
    r""" Count of newly observed file extensions.

Example: """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the newly observed file extension.

Example: """

    @property
    def resource(self):
        return AntiRansomwareVolumeWorkloadNewlyObservedFileExtensions

    gettable_fields = [
        "count",
        "name",
    ]
    """count,name,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class AntiRansomwareVolumeWorkloadNewlyObservedFileExtensions(Resource):

    _schema = AntiRansomwareVolumeWorkloadNewlyObservedFileExtensionsSchema
