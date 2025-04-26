r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AclDelete", "AclDeleteSchema"]
__pdoc__ = {
    "AclDeleteSchema.resource": False,
    "AclDeleteSchema.opts": False,
    "AclDelete": False,
}


class AclDeleteSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AclDelete object"""

    access = marshmallow_fields.Str(data_key="access", allow_none=True)
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
* audit_success """

    access_control = marshmallow_fields.Str(data_key="access_control", allow_none=True)
    r""" An Access Control Level specifies the access control of the task to be applied. Valid values
are "file-directory" or "Storage-Level Access Guard (SLAG)". SLAG is used to apply the
specified security descriptors with the task for the volume or qtree. Otherwise, the
security descriptors are applied on files and directories at the specified path.
The value SLAG is not supported on FlexGroups volumes. The default value is "file-directory"
('-' and '_' are interchangeable).


Valid choices:

* file_directory
* slag """

    apply_to = marshmallow_fields.Nested("netapp_ontap.models.apply_to.ApplyToSchema", unknown=EXCLUDE, data_key="apply_to", allow_none=True)
    r""" Specifies where to apply the DACL or SACL entries.
You can specify more than one value by using a comma-delimited list. """

    ignore_paths = marshmallow_fields.List(marshmallow_fields.Str, data_key="ignore_paths", allow_none=True)
    r""" Specifies that permissions on this file or directory cannot be replaced.


Example: ["/dir1/dir2/","/parent/dir3"] """

    propagation_mode = marshmallow_fields.Str(data_key="propagation_mode", allow_none=True)
    r""" Specifies how to propagate security settings to child subfolders and files.
This setting determines how child files/folders contained within a parent
folder inherit access control and audit information from the parent folder.
The available values are:

* propagate    - propagate inheritable permissions to all subfolders and files
* replace      - replace existing permissions on all subfolders and files with inheritable permissions


Valid choices:

* propagate
* replace """

    @property
    def resource(self):
        return AclDelete

    gettable_fields = [
        "access",
        "access_control",
        "apply_to",
        "ignore_paths",
        "propagation_mode",
    ]
    """access,access_control,apply_to,ignore_paths,propagation_mode,"""

    patchable_fields = [
        "access",
        "access_control",
        "apply_to",
        "ignore_paths",
        "propagation_mode",
    ]
    """access,access_control,apply_to,ignore_paths,propagation_mode,"""

    postable_fields = [
        "access",
        "access_control",
        "apply_to",
        "ignore_paths",
        "propagation_mode",
    ]
    """access,access_control,apply_to,ignore_paths,propagation_mode,"""


class AclDelete(Resource):

    _schema = AclDeleteSchema
