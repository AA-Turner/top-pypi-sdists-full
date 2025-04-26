r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VscanOnAccessScope", "VscanOnAccessScopeSchema"]
__pdoc__ = {
    "VscanOnAccessScopeSchema.resource": False,
    "VscanOnAccessScopeSchema.opts": False,
    "VscanOnAccessScope": False,
}


class VscanOnAccessScopeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VscanOnAccessScope object"""

    exclude_extensions = marshmallow_fields.List(marshmallow_fields.Str, data_key="exclude_extensions", allow_none=True)
    r""" List of file extensions for which scanning is not performed.

Example: ["mp*","txt"] """

    exclude_paths = marshmallow_fields.List(marshmallow_fields.Str, data_key="exclude_paths", allow_none=True)
    r""" List of file paths for which scanning must not be performed.

Example: ["\\dir1\\dir2\\name","\\vol\\a b","\\vol\\a,b\\"] """

    include_extensions = marshmallow_fields.List(marshmallow_fields.Str, data_key="include_extensions", allow_none=True)
    r""" List of file extensions to be scanned.

Example: ["mp*","txt"] """

    max_file_size = Size(data_key="max_file_size", allow_none=True)
    r""" Maximum file size, in bytes, allowed for scanning.

Example: 2147483648 """

    only_execute_access = marshmallow_fields.Boolean(data_key="only_execute_access", allow_none=True)
    r""" Scan only files opened with execute-access. """

    scan_readonly_volumes = marshmallow_fields.Boolean(data_key="scan_readonly_volumes", allow_none=True)
    r""" Specifies whether or not read-only volume can be scanned. """

    scan_without_extension = marshmallow_fields.Boolean(data_key="scan_without_extension", allow_none=True)
    r""" Specifies whether or not files without any extension can be scanned. """

    @property
    def resource(self):
        return VscanOnAccessScope

    gettable_fields = [
        "exclude_extensions",
        "exclude_paths",
        "include_extensions",
        "max_file_size",
        "only_execute_access",
        "scan_readonly_volumes",
        "scan_without_extension",
    ]
    """exclude_extensions,exclude_paths,include_extensions,max_file_size,only_execute_access,scan_readonly_volumes,scan_without_extension,"""

    patchable_fields = [
        "exclude_extensions",
        "exclude_paths",
        "include_extensions",
        "max_file_size",
        "only_execute_access",
        "scan_readonly_volumes",
        "scan_without_extension",
    ]
    """exclude_extensions,exclude_paths,include_extensions,max_file_size,only_execute_access,scan_readonly_volumes,scan_without_extension,"""

    postable_fields = [
        "exclude_extensions",
        "exclude_paths",
        "include_extensions",
        "max_file_size",
        "only_execute_access",
        "scan_readonly_volumes",
        "scan_without_extension",
    ]
    """exclude_extensions,exclude_paths,include_extensions,max_file_size,only_execute_access,scan_readonly_volumes,scan_without_extension,"""


class VscanOnAccessScope(Resource):

    _schema = VscanOnAccessScopeSchema
