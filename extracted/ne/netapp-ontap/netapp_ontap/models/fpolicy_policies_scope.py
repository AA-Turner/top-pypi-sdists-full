r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FpolicyPoliciesScope", "FpolicyPoliciesScopeSchema"]
__pdoc__ = {
    "FpolicyPoliciesScopeSchema.resource": False,
    "FpolicyPoliciesScopeSchema.opts": False,
    "FpolicyPoliciesScope": False,
}


class FpolicyPoliciesScopeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FpolicyPoliciesScope object"""

    check_extensions_on_directories = marshmallow_fields.Boolean(data_key="check_extensions_on_directories", allow_none=True)
    r""" Specifies whether the file name extension checks also apply to directory objects. If this parameter is set to true,
the directory objects are subjected to the same extension checks as regular files. If this parameter is set to false,
the directory names are not matched for extensions and notifications are sent for directories even if their name
extensions do not match. Default is false. """

    exclude_export_policies = marshmallow_fields.List(marshmallow_fields.Str, data_key="exclude_export_policies", allow_none=True)
    r""" The exclude_export_policies field of the fpolicy_policies_scope. """

    exclude_extension = marshmallow_fields.List(marshmallow_fields.Str, data_key="exclude_extension", allow_none=True)
    r""" The exclude_extension field of the fpolicy_policies_scope. """

    exclude_shares = marshmallow_fields.List(marshmallow_fields.Str, data_key="exclude_shares", allow_none=True)
    r""" The exclude_shares field of the fpolicy_policies_scope. """

    exclude_volumes = marshmallow_fields.List(marshmallow_fields.Str, data_key="exclude_volumes", allow_none=True)
    r""" The exclude_volumes field of the fpolicy_policies_scope.

Example: ["vol1","vol_svm1","*"] """

    include_export_policies = marshmallow_fields.List(marshmallow_fields.Str, data_key="include_export_policies", allow_none=True)
    r""" The include_export_policies field of the fpolicy_policies_scope. """

    include_extension = marshmallow_fields.List(marshmallow_fields.Str, data_key="include_extension", allow_none=True)
    r""" The include_extension field of the fpolicy_policies_scope. """

    include_shares = marshmallow_fields.List(marshmallow_fields.Str, data_key="include_shares", allow_none=True)
    r""" The include_shares field of the fpolicy_policies_scope.

Example: ["sh1","share_cifs"] """

    include_volumes = marshmallow_fields.List(marshmallow_fields.Str, data_key="include_volumes", allow_none=True)
    r""" The include_volumes field of the fpolicy_policies_scope.

Example: ["vol1","vol_svm1"] """

    object_monitoring_with_no_extension = marshmallow_fields.Boolean(data_key="object_monitoring_with_no_extension", allow_none=True)
    r""" Specifies whether the extension checks also apply to objects with no extension. If this parameter is set to true,
all objects with or without extensions are monitored. Default is false. """

    @property
    def resource(self):
        return FpolicyPoliciesScope

    gettable_fields = [
        "check_extensions_on_directories",
        "exclude_export_policies",
        "exclude_extension",
        "exclude_shares",
        "exclude_volumes",
        "include_export_policies",
        "include_extension",
        "include_shares",
        "include_volumes",
        "object_monitoring_with_no_extension",
    ]
    """check_extensions_on_directories,exclude_export_policies,exclude_extension,exclude_shares,exclude_volumes,include_export_policies,include_extension,include_shares,include_volumes,object_monitoring_with_no_extension,"""

    patchable_fields = [
        "check_extensions_on_directories",
        "exclude_export_policies",
        "exclude_extension",
        "exclude_shares",
        "exclude_volumes",
        "include_export_policies",
        "include_extension",
        "include_shares",
        "include_volumes",
        "object_monitoring_with_no_extension",
    ]
    """check_extensions_on_directories,exclude_export_policies,exclude_extension,exclude_shares,exclude_volumes,include_export_policies,include_extension,include_shares,include_volumes,object_monitoring_with_no_extension,"""

    postable_fields = [
        "check_extensions_on_directories",
        "exclude_export_policies",
        "exclude_extension",
        "exclude_shares",
        "exclude_volumes",
        "include_export_policies",
        "include_extension",
        "include_shares",
        "include_volumes",
        "object_monitoring_with_no_extension",
    ]
    """check_extensions_on_directories,exclude_export_policies,exclude_extension,exclude_shares,exclude_volumes,include_export_policies,include_extension,include_shares,include_volumes,object_monitoring_with_no_extension,"""


class FpolicyPoliciesScope(Resource):

    _schema = FpolicyPoliciesScopeSchema
