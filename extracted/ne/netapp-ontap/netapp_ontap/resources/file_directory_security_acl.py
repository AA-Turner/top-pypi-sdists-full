r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union

from marshmallow import fields as marshmallow_fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["FileDirectorySecurityAcl", "FileDirectorySecurityAclSchema"]
__pdoc__ = {
    "FileDirectorySecurityAclSchema.resource": False,
    "FileDirectorySecurityAclSchema.opts": False,
}


class FileDirectorySecurityAclSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FileDirectorySecurityAcl object"""

    access = marshmallow_fields.Str(
        data_key="access",
        validate=enum_validation(['access_allow', 'access_deny', 'audit_failure', 'audit_success']),
        allow_none=True,
    )
    r""" Specifies whether the ACL is for DACL or SACL. It is a required field.
The available values are:

* access_allow                     - DACL for allow access
* access_deny                      - DACL for deny access
* audit_success                    - SACL for success access
* audit_failure                    - SACL for failure access


Valid choices:

* access_allow
* access_deny
* audit_failure
* audit_success"""

    access_control = marshmallow_fields.Str(
        data_key="access_control",
        validate=enum_validation(['file_directory', 'slag']),
        allow_none=True,
    )
    r""" Access Control Level specifies the access control of the task to be applied. Valid values
are "file-directory" or "Storage-Level Access Guard (SLAG)". SLAG is used to apply the
specified security descriptors with the task for the volume or qtree. Otherwise, the
security descriptors are applied on files and directories at the specified path. The
value SLAG is not supported on FlexGroups volumes. The default value is "file-directory"
('-' and '_' are interchangeable).


Valid choices:

* file_directory
* slag"""

    advanced_rights = marshmallow_fields.Nested("netapp_ontap.models.advanced_rights.AdvancedRightsSchema", data_key="advanced_rights", unknown=EXCLUDE, allow_none=True)
    r""" Specifies the advanced access right controlled by the ACE for the account specified.
 You can specify more than one "advanced-rights" value by using a comma-delimited list."""

    apply_to = marshmallow_fields.Nested("netapp_ontap.models.apply_to.ApplyToSchema", data_key="apply_to", unknown=EXCLUDE, allow_none=True)
    r""" Specifies where to apply the DACL or SACL entries.
You can specify more than one value by using a comma-delimited list."""

    ignore_paths = marshmallow_fields.List(marshmallow_fields.Str, data_key="ignore_paths", allow_none=True)
    r""" Specifies that permissions on this file or directory cannot be replaced.


Example: ["/dir1/dir2/","/parent/dir3"]"""

    propagation_mode = marshmallow_fields.Str(
        data_key="propagation_mode",
        validate=enum_validation(['propagate', 'ignore', 'replace']),
        allow_none=True,
    )
    r""" Specifies how to propagate security settings to child subfolders and files.
This setting determines how child files/folders contained within a parent
folder inherit access control and audit information from the parent folder.
The available values are:

* propagate    - propagate inheritable permissions to all subfolders and files
* ignore       - ignore inheritable permissions
* replace      - replace existing permissions on all subfolders and files with inheritable permissions


Valid choices:

* propagate
* ignore
* replace"""

    rights = marshmallow_fields.Str(
        data_key="rights",
        allow_none=True,
    )
    r""" The rights field of the file_directory_security_acl."""

    user = marshmallow_fields.Str(
        data_key="user",
        allow_none=True,
    )
    r""" Specifies the account to which the ACE applies.
You can specify either name or SID.


Example: S-1-5-21-2233347455-2266964949-1780268902-69304"""

    @property
    def resource(self):
        return FileDirectorySecurityAcl

    gettable_fields = [
        "access",
        "access_control",
        "advanced_rights",
        "apply_to",
        "ignore_paths",
        "propagation_mode",
        "rights",
        "user",
    ]
    """access,access_control,advanced_rights,apply_to,ignore_paths,propagation_mode,rights,user,"""

    patchable_fields = [
        "access",
        "access_control",
        "advanced_rights",
        "apply_to",
        "ignore_paths",
        "propagation_mode",
        "rights",
    ]
    """access,access_control,advanced_rights,apply_to,ignore_paths,propagation_mode,rights,"""

    postable_fields = [
        "access",
        "access_control",
        "advanced_rights",
        "apply_to",
        "ignore_paths",
        "propagation_mode",
        "rights",
        "user",
    ]
    """access,access_control,advanced_rights,apply_to,ignore_paths,propagation_mode,rights,user,"""

class FileDirectorySecurityAcl(Resource):
    r""" Manages the DACLS or SACLS. """

    _schema = FileDirectorySecurityAclSchema
    _path = "/api/protocols/file-security/permissions/{svm[uuid]}/{file_directory_security_acl[path]}/acl"
    _keys = ["svm.uuid", "file_directory_security_acl.path", "user"]


    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["FileDirectorySecurityAcl"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the SACLs/DACLs
You must keep the following points in mind while using these endpoints:
* SLAG applies to all files and/or directories in a volume hence, inheritance is not required to be propagated.
* Set access_control field to slag while updating SLAG ACE.
* Set access_control field to file_directory while updating file-directory ACE. By Default access_control field is set to file_directory.
* For SLAG, valid apply_to combinations are "this-folder, sub-folders", "files", "this-folder, sub-folders, files".
### Required properties
* `access` - Specifies whether the ACE is for DACL or SACL.
* `user` - Name of the user to which the ACE applies.
### Related ONTAP commands
* `vserver security file-directory ntfs dacl modify`
* `vserver security file-directory ntfs sacl modify`
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["FileDirectorySecurityAcl"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["FileDirectorySecurityAcl"], NetAppResponse]:
        r"""Adds the new SACL/DACL ACE.
You must keep the following points in mind while using these endpoints:
* SLAG applies to all files and/or directories in a volume hence, inheritance is not required to be propagated.
* Set access_control field to slag while adding SLAG ACE.
* Set access_control field to file_directory while adding file-directory ACE. By Default access_control field is set to file_directory.
* For SLAG, valid apply_to combinations are "this-folder, sub-folders", "files", "this-folder, sub-folders, files".
### Required properties
* `user` - Name of the user to which the ACE applies.
* `access` - Specifies whether the ACE is for DACL or SACL.
### Related ONTAP commands
* `vserver security file-directory ntfs dacl add`
* `vserver security file-directory ntfs sacl add`
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["FileDirectorySecurityAcl"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the SACL/DACL ACL
You must keep the following points in mind while using these endpoints:
* SLAG applies to all files and/or directories in a volume hence, inheritance is not required to be propagated.
* Set access_control field to slag while deleting SLAG ACE.
* Set access_control field to file_directory while deleting file-directory ACE. By Default access_control field is set to file_directory.
* For SLAG, valid apply_to combinations are "this-folder, sub-folders", "files", "this-folder, sub-folders, files".
### Required properties
* `access` - Specifies whether the ACE is for DACL or SACL.
* `user` - Name of the user to which the ACE applies.
### Related ONTAP commands
* `vserver security file-directory ntfs dacl remove`
* `vserver security file-directory ntfs sacl remove`
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)



    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Adds the new SACL/DACL ACE.
You must keep the following points in mind while using these endpoints:
* SLAG applies to all files and/or directories in a volume hence, inheritance is not required to be propagated.
* Set access_control field to slag while adding SLAG ACE.
* Set access_control field to file_directory while adding file-directory ACE. By Default access_control field is set to file_directory.
* For SLAG, valid apply_to combinations are "this-folder, sub-folders", "files", "this-folder, sub-folders, files".
### Required properties
* `user` - Name of the user to which the ACE applies.
* `access` - Specifies whether the ACE is for DACL or SACL.
### Related ONTAP commands
* `vserver security file-directory ntfs dacl add`
* `vserver security file-directory ntfs sacl add`
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the SACLs/DACLs
You must keep the following points in mind while using these endpoints:
* SLAG applies to all files and/or directories in a volume hence, inheritance is not required to be propagated.
* Set access_control field to slag while updating SLAG ACE.
* Set access_control field to file_directory while updating file-directory ACE. By Default access_control field is set to file_directory.
* For SLAG, valid apply_to combinations are "this-folder, sub-folders", "files", "this-folder, sub-folders, files".
### Required properties
* `access` - Specifies whether the ACE is for DACL or SACL.
* `user` - Name of the user to which the ACE applies.
### Related ONTAP commands
* `vserver security file-directory ntfs dacl modify`
* `vserver security file-directory ntfs sacl modify`
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the SACL/DACL ACL
You must keep the following points in mind while using these endpoints:
* SLAG applies to all files and/or directories in a volume hence, inheritance is not required to be propagated.
* Set access_control field to slag while deleting SLAG ACE.
* Set access_control field to file_directory while deleting file-directory ACE. By Default access_control field is set to file_directory.
* For SLAG, valid apply_to combinations are "this-folder, sub-folders", "files", "this-folder, sub-folders, files".
### Required properties
* `access` - Specifies whether the ACE is for DACL or SACL.
* `user` - Name of the user to which the ACE applies.
### Related ONTAP commands
* `vserver security file-directory ntfs dacl remove`
* `vserver security file-directory ntfs sacl remove`
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


