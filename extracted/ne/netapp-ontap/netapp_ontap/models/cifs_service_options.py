r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["CifsServiceOptions", "CifsServiceOptionsSchema"]
__pdoc__ = {
    "CifsServiceOptionsSchema.resource": False,
    "CifsServiceOptionsSchema.opts": False,
    "CifsServiceOptions": False,
}


class CifsServiceOptionsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CifsServiceOptions object"""

    admin_to_root_mapping = marshmallow_fields.Boolean(data_key="admin_to_root_mapping", allow_none=True)
    r""" Specifies whether or not Administrator can be mapped to the UNIX user "root". """

    advanced_sparse_file = marshmallow_fields.Boolean(data_key="advanced_sparse_file", allow_none=True)
    r""" Specifies whether or not the CIFS server supports the advanced sparse file capabilities. This allows
CIFS clients to query the allocated ranges of a file and to write zeroes or free data blocks for ranges
of a file. """

    backup_symlink_enabled = marshmallow_fields.Boolean(data_key="backup_symlink_enabled", allow_none=True)
    r""" Specifies whether or not to preserve UNIX symlinks during backup through SMB. """

    client_dup_detection_enabled = marshmallow_fields.Boolean(data_key="client_dup_detection_enabled", allow_none=True)
    r""" Specifies whether or not client duplicate session detection is enabled for CIFS. """

    client_version_reporting_enabled = marshmallow_fields.Boolean(data_key="client_version_reporting_enabled", allow_none=True)
    r""" Specifies whether or not client version reporting is enabled for CIFS. """

    copy_offload = marshmallow_fields.Boolean(data_key="copy_offload", allow_none=True)
    r""" Specifies whether or not to enable the Copy Offload feature. This feature enables direct
data transfers within or between compatible storage devices without transferring the data
through the host computer.<br/>
Note that this will also enable/disable the direct copy feature accordingly. """

    dac_enabled = marshmallow_fields.Boolean(data_key="dac_enabled", allow_none=True)
    r""" Specifies whether or not the Dynamic Access Control (DAC) feature is enabled for the CIFS server. """

    export_policy_enabled = marshmallow_fields.Boolean(data_key="export_policy_enabled", allow_none=True)
    r""" Specifies whether or not export policies are enabled for CIFS. """

    fake_open = marshmallow_fields.Boolean(data_key="fake_open", allow_none=True)
    r""" Specifies whether or not fake open support is enabled. This parameter allows you to optimize the
open and close requests coming from SMB 2 clients. """

    fsctl_trim = marshmallow_fields.Boolean(data_key="fsctl_trim", allow_none=True)
    r""" Specifies whether or not the trim requests (FSCTL_FILE_LEVEL_TRIM) are supported on the CIFS server. """

    junction_reparse = marshmallow_fields.Boolean(data_key="junction_reparse", allow_none=True)
    r""" Specifies whether or not the reparse point support is enabled. When enabled the CIFS server
exposes junction points to Windows clients as reparse points. This parameter is only active
if the client has negotiated use of the SMB 2 or SMB 3 protocol. This parameter is not supported
for SVMs with Infinite Volume. """

    large_mtu = marshmallow_fields.Boolean(data_key="large_mtu", allow_none=True)
    r""" Specifies whether or not SMB clients can send reads up to 1 MB in size. """

    max_connections_per_session = Size(data_key="max_connections_per_session", allow_none=True)
    r""" Specifies the maximum number of connections allowed per multichannel session.

Example: 32 """

    max_lifs_per_session = Size(data_key="max_lifs_per_session", allow_none=True)
    r""" Specifies the maximum number of LIFs advertised per multichannel session.

Example: 256 """

    max_opens_same_file_per_tree = Size(data_key="max_opens_same_file_per_tree", allow_none=True)
    r""" Specifies the maximum number of opens on the same file per tree.

Example: 1000 """

    max_same_tree_connect_per_session = Size(data_key="max_same_tree_connect_per_session", allow_none=True)
    r""" Specifies the maximum number of same tree connections per session.

Example: 5000 """

    max_same_user_sessions_per_connection = Size(data_key="max_same_user_sessions_per_connection", allow_none=True)
    r""" Specifies the maximum number of same user sessions per connection.

Example: 2500 """

    max_watches_set_per_tree = Size(data_key="max_watches_set_per_tree", allow_none=True)
    r""" Specifies the maximum number of watches set per tree.

Example: 500 """

    multichannel = marshmallow_fields.Boolean(data_key="multichannel", allow_none=True)
    r""" Specifies whether or not the CIFS server supports Multichannel. """

    null_user_windows_name = marshmallow_fields.Str(data_key="null_user_windows_name", allow_none=True)
    r""" Specifies a Windows User or Group name that should be mapped in case of a NULL user
value. """

    path_component_cache = marshmallow_fields.Boolean(data_key="path_component_cache", allow_none=True)
    r""" Specifies whether or not the path component cache is enabled on the CIFS server. """

    referral = marshmallow_fields.Boolean(data_key="referral", allow_none=True)
    r""" Specifies whether or not to refer clients to more optimal LIFs. When enabled, it automatically
refers clients to a data LIF local to the node which hosts the root of the requested share. """

    shadowcopy = marshmallow_fields.Boolean(data_key="shadowcopy", allow_none=True)
    r""" Specifies whether or not to enable the Shadowcopy Feature. This feature enables
to take share-based backup copies of data that is in a data-consistent state at
a specific point in time where the data is accessed over SMB 3.0 shares. """

    shadowcopy_dir_depth = Size(data_key="shadowcopy_dir_depth", allow_none=True)
    r""" Specifies the maximum level of subdirectories on which ONTAP should create shadow copies. """

    smb_credits = Size(data_key="smb_credits", allow_none=True)
    r""" Specifies the maximum number of outstanding requests on a CIFS connection.

Example: 128 """

    trusted_domain_enum_search_enabled = marshmallow_fields.Boolean(data_key="trusted_domain_enum_search_enabled", allow_none=True)
    r""" Specifies whether or not to enable trusted domain search.
- If this parameter is set to true, it displays CIFS options only for CIFS servers
  that support enumeration of bidirectional trusted domains and that support searching in
  all bidirectional trusted domains when performing Windows user lookups for UNIX user to
  Windows user name mapping.
- If set to false, it displays CIFS options for CIFS servers that do not support enumeration
  of bidirectional trusted domains. """

    widelink_reparse_versions = marshmallow_fields.List(marshmallow_fields.Str, data_key="widelink_reparse_versions", allow_none=True)
    r""" Specifies the CIFS protocol versions for which the widelink is reported as reparse point. """

    @property
    def resource(self):
        return CifsServiceOptions

    gettable_fields = [
        "admin_to_root_mapping",
        "advanced_sparse_file",
        "backup_symlink_enabled",
        "client_dup_detection_enabled",
        "client_version_reporting_enabled",
        "copy_offload",
        "dac_enabled",
        "export_policy_enabled",
        "fake_open",
        "fsctl_trim",
        "junction_reparse",
        "large_mtu",
        "max_connections_per_session",
        "max_lifs_per_session",
        "max_opens_same_file_per_tree",
        "max_same_tree_connect_per_session",
        "max_same_user_sessions_per_connection",
        "max_watches_set_per_tree",
        "multichannel",
        "null_user_windows_name",
        "path_component_cache",
        "referral",
        "shadowcopy",
        "shadowcopy_dir_depth",
        "smb_credits",
        "trusted_domain_enum_search_enabled",
        "widelink_reparse_versions",
    ]
    """admin_to_root_mapping,advanced_sparse_file,backup_symlink_enabled,client_dup_detection_enabled,client_version_reporting_enabled,copy_offload,dac_enabled,export_policy_enabled,fake_open,fsctl_trim,junction_reparse,large_mtu,max_connections_per_session,max_lifs_per_session,max_opens_same_file_per_tree,max_same_tree_connect_per_session,max_same_user_sessions_per_connection,max_watches_set_per_tree,multichannel,null_user_windows_name,path_component_cache,referral,shadowcopy,shadowcopy_dir_depth,smb_credits,trusted_domain_enum_search_enabled,widelink_reparse_versions,"""

    patchable_fields = [
        "admin_to_root_mapping",
        "advanced_sparse_file",
        "backup_symlink_enabled",
        "client_dup_detection_enabled",
        "client_version_reporting_enabled",
        "copy_offload",
        "dac_enabled",
        "export_policy_enabled",
        "fake_open",
        "fsctl_trim",
        "junction_reparse",
        "large_mtu",
        "max_connections_per_session",
        "max_lifs_per_session",
        "max_opens_same_file_per_tree",
        "max_same_tree_connect_per_session",
        "max_same_user_sessions_per_connection",
        "max_watches_set_per_tree",
        "multichannel",
        "null_user_windows_name",
        "path_component_cache",
        "referral",
        "shadowcopy",
        "shadowcopy_dir_depth",
        "smb_credits",
        "trusted_domain_enum_search_enabled",
        "widelink_reparse_versions",
    ]
    """admin_to_root_mapping,advanced_sparse_file,backup_symlink_enabled,client_dup_detection_enabled,client_version_reporting_enabled,copy_offload,dac_enabled,export_policy_enabled,fake_open,fsctl_trim,junction_reparse,large_mtu,max_connections_per_session,max_lifs_per_session,max_opens_same_file_per_tree,max_same_tree_connect_per_session,max_same_user_sessions_per_connection,max_watches_set_per_tree,multichannel,null_user_windows_name,path_component_cache,referral,shadowcopy,shadowcopy_dir_depth,smb_credits,trusted_domain_enum_search_enabled,widelink_reparse_versions,"""

    postable_fields = [
        "admin_to_root_mapping",
        "advanced_sparse_file",
        "backup_symlink_enabled",
        "client_dup_detection_enabled",
        "client_version_reporting_enabled",
        "copy_offload",
        "dac_enabled",
        "export_policy_enabled",
        "fake_open",
        "fsctl_trim",
        "junction_reparse",
        "large_mtu",
        "max_connections_per_session",
        "max_lifs_per_session",
        "max_opens_same_file_per_tree",
        "max_same_tree_connect_per_session",
        "max_same_user_sessions_per_connection",
        "max_watches_set_per_tree",
        "multichannel",
        "null_user_windows_name",
        "path_component_cache",
        "referral",
        "shadowcopy",
        "shadowcopy_dir_depth",
        "smb_credits",
        "trusted_domain_enum_search_enabled",
        "widelink_reparse_versions",
    ]
    """admin_to_root_mapping,advanced_sparse_file,backup_symlink_enabled,client_dup_detection_enabled,client_version_reporting_enabled,copy_offload,dac_enabled,export_policy_enabled,fake_open,fsctl_trim,junction_reparse,large_mtu,max_connections_per_session,max_lifs_per_session,max_opens_same_file_per_tree,max_same_tree_connect_per_session,max_same_user_sessions_per_connection,max_watches_set_per_tree,multichannel,null_user_windows_name,path_component_cache,referral,shadowcopy,shadowcopy_dir_depth,smb_credits,trusted_domain_enum_search_enabled,widelink_reparse_versions,"""


class CifsServiceOptions(Resource):

    _schema = CifsServiceOptionsSchema
