r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API displays the effective permission granted to a Windows or UNIX user on the specified file or folder path.
## Examples
### Retrieving the effective permission for the specified Windows user on the specified path of an SVM.
```
# The API:
curl -X GET "https://10.63.26.252/api/protocols/file-security/effective-permissions/cf5f271a-1beb-11ea-8fad-005056bb645e/administrator/windows/%2F?share.name=sh1&return_records=true" -H "accept: application/json" -H "authorization: Basic YWRtaW46bmV0YXBwMSE="
# The response:
{
  "svm": {
    "uuid": "cf5f271a-1beb-11ea-8fad-005056bb645e",
    "name": "vs1"
  },
  "user": "administrator",
  "type": "windows",
  "path": "/",
  "share": {
    "path": "/"
  },
  "file_permission": [
    "read",
    "write",
    "append",
    "read_ea",
    "write_ea",
    "execute",
    "delete_child",
    "read_attributes",
    "write_attributes",
    "delete",
    "read_control",
    "write_dac",
    "write_owner",
    "synchronize",
    "system_security"
  ],
  "share_permission": [
    "read",
    "read_ea",
    "execute",
    "read_attributes",
    "read_control",
    "synchronize"
  ]
}"""

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


__all__ = ["EffectivePermission", "EffectivePermissionSchema"]
__pdoc__ = {
    "EffectivePermissionSchema.resource": False,
    "EffectivePermissionSchema.opts": False,
}


class EffectivePermissionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EffectivePermission object"""

    file_permissions = marshmallow_fields.List(marshmallow_fields.Str, data_key="file_permissions", allow_none=True)
    r""" Specifies the effective permission granted to a user on the specified file or folder path."""

    path = marshmallow_fields.Str(
        data_key="path",
        allow_none=True,
    )
    r""" Specifies the path of the file or the folder for which you want to display effective permissions.
The path is relative to the SVM root volume. If "-share-name" is specified then path will be relative to the share path.


Example: /dir1/dir2"""

    share = marshmallow_fields.Nested("netapp_ontap.models.share.ShareSchema", data_key="share", unknown=EXCLUDE, allow_none=True)
    r""" The share field of the effective_permission."""

    share_permissions = marshmallow_fields.List(marshmallow_fields.Str, data_key="share_permissions", allow_none=True)
    r""" Specifies the effective permission granted to a user on the specified file or folder path."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the effective_permission."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['windows', 'unix']),
        allow_none=True,
    )
    r""" Specifies the user type. The following values are allowed:

* windows  - Windows user
* unix     - UNIX user


Valid choices:

* windows
* unix"""

    user = marshmallow_fields.Str(
        data_key="user",
        allow_none=True,
    )
    r""" Specifies the user for which effective permission needs to be displayed for the specified path.

Example: cifs1/administrator"""

    @property
    def resource(self):
        return EffectivePermission

    gettable_fields = [
        "file_permissions",
        "path",
        "share",
        "share_permissions",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "type",
        "user",
    ]
    """file_permissions,path,share,share_permissions,svm.links,svm.name,svm.uuid,type,user,"""

    patchable_fields = [
        "file_permissions",
        "path",
        "share",
        "share_permissions",
        "svm.name",
        "svm.uuid",
        "type",
        "user",
    ]
    """file_permissions,path,share,share_permissions,svm.name,svm.uuid,type,user,"""

    postable_fields = [
        "file_permissions",
        "path",
        "share",
        "share_permissions",
        "svm.name",
        "svm.uuid",
        "type",
        "user",
    ]
    """file_permissions,path,share,share_permissions,svm.name,svm.uuid,type,user,"""

class EffectivePermission(Resource):
    r""" Displays the effective permission granted to a Windows or UNIX user on the specified file or folder path. """

    _schema = EffectivePermissionSchema
    _path = "/api/protocols/file-security/effective-permissions"
    _keys = ["svm.uuid", "path"]






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves effective security permissions on a file.
### Related ONTAP commands
* `vserver security file-directory show-effective-permissions`

### Learn more
* [`DOC /protocols/file-security/effective-permissions/{svm.uuid}/{path}`](#docs-NAS-protocols_file-security_effective-permissions_{svm.uuid}_{path})"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





