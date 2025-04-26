r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VscanOnDemandScope", "VscanOnDemandScopeSchema"]
__pdoc__ = {
    "VscanOnDemandScopeSchema.resource": False,
    "VscanOnDemandScopeSchema.opts": False,
    "VscanOnDemandScope": False,
}


class VscanOnDemandScopeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VscanOnDemandScope object"""

    exclude_extensions = marshmallow_fields.List(marshmallow_fields.Str, data_key="exclude_extensions", allow_none=True)
    r""" List of file extensions for which scanning is not performed.

Example: ["mp3","mp4"] """

    exclude_paths = marshmallow_fields.List(marshmallow_fields.Str, data_key="exclude_paths", allow_none=True)
    r""" List of file paths for which scanning must not be performed.

Example: ["/vol1/cold-files/","/vol1/cifs/names"] """

    include_extensions = marshmallow_fields.List(marshmallow_fields.Str, data_key="include_extensions", allow_none=True)
    r""" List of file extensions to be scanned.

Example: ["vmdk","mp*"] """

    max_file_size = Size(data_key="max_file_size", allow_none=True)
    r""" Maximum file size, in bytes, allowed for scanning.

Example: 10737418240 """

    scan_without_extension = marshmallow_fields.Boolean(data_key="scan_without_extension", allow_none=True)
    r""" Specifies whether or not files without any extension can be scanned. """

    @property
    def resource(self):
        return VscanOnDemandScope

    gettable_fields = [
        "exclude_extensions",
        "exclude_paths",
        "include_extensions",
        "max_file_size",
        "scan_without_extension",
    ]
    """exclude_extensions,exclude_paths,include_extensions,max_file_size,scan_without_extension,"""

    patchable_fields = [
        "exclude_extensions",
        "exclude_paths",
        "include_extensions",
        "max_file_size",
        "scan_without_extension",
    ]
    """exclude_extensions,exclude_paths,include_extensions,max_file_size,scan_without_extension,"""

    postable_fields = [
        "exclude_extensions",
        "exclude_paths",
        "include_extensions",
        "max_file_size",
        "scan_without_extension",
    ]
    """exclude_extensions,exclude_paths,include_extensions,max_file_size,scan_without_extension,"""


class VscanOnDemandScope(Resource):

    _schema = VscanOnDemandScopeSchema
