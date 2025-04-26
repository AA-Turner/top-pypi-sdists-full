r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Access to files and folders can be secured over a network by configuring share access control lists (ACLs) on CIFS shares. Share-level ACLs can be configured by using either Windows users and groups or UNIX users and groups. A share-level ACL consists of a list of access control entries (ACEs). Each ACE contains a user or group name and a set of permissions that determines user or group access to the share, regardless of the security style of the volume or qtree containing the share. </br>
When an SMB user tries to access a share, ONTAP checks the share-level ACL to determine whether access should be granted. A share-level ACL only restricts access to files in the share; it never grants more access than the file level ACLs.
## Examples
### Creating a CIFS share ACL
To create a share ACL for a CIFS share, use the following API. Note the <i>return_records=true</i> query parameter used to obtain the newly created entry in the response.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsShareAcl

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsShareAcl("sh1")
    resource.permission = "no_access"
    resource.type = "windows"
    resource.user_or_group = "root"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
CifsShareAcl(
    {
        "permission": "no_access",
        "sid": "S-1-1-0",
        "svm": {"name": "vs1"},
        "type": "windows",
        "user_or_group": "root",
    }
)

```
</div>
</div>

---
### Retrieving all CIFS shares ACLs for a specific CIFS share for a specific SVM in the cluster
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsShareAcl

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(CifsShareAcl.get_collection("sh1", fields="*", return_timeout=15)))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    CifsShareAcl(
        {
            "permission": "full_control",
            "sid": "S-1-1-0",
            "svm": {"name": "vs1", "uuid": "000c5cd2-ebdf-11e8-a96e-0050568ea3cb"},
            "type": "windows",
            "user_or_group": "Everyone",
        }
    ),
    CifsShareAcl(
        {
            "permission": "no_access",
            "sid": "S-1-1-0",
            "svm": {"name": "vs1", "uuid": "000c5cd2-ebdf-11e8-a96e-0050568ea3cb"},
            "type": "windows",
            "user_or_group": "root",
        }
    ),
]

```
</div>
</div>

---
### Retrieving a CIFS share ACLs for a user or a group of type Windows or type UNIX on a CIFS share for a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsShareAcl

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsShareAcl("sh1", type="windows", user_or_group="everyone")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
CifsShareAcl(
    {
        "permission": "full_control",
        "sid": "S-1-1-0",
        "svm": {"name": "vs1", "uuid": "000c5cd2-ebdf-11e8-a96e-0050568ea3cb"},
        "type": "windows",
        "user_or_group": "everyone",
    }
)

```
</div>
</div>

### Updating a CIFS share ACLs of a user or group on a CIFS share for a specific SVM
The CIFS share ACL being modified is identified by the UUID of its SVM, the CIFS share name, user or group name and the type of the user or group.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsShareAcl

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsShareAcl("sh1", type="windows", user_or_group="everyone")
    resource.permission = "no_access"
    resource.patch()

```

### Removing a CIFS share ACLs of a user or group on a CIFS Share for a specific SVM
The CIFS share ACL being removed is identified by the UUID of its SVM, the CIFS share name, user or group name and the type of the user or group.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsShareAcl

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsShareAcl("sh1", type="windows", user_or_group="everyone")
    resource.delete()

```

---"""

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


__all__ = ["CifsShareAcl", "CifsShareAclSchema"]
__pdoc__ = {
    "CifsShareAclSchema.resource": False,
    "CifsShareAclSchema.opts": False,
}


class CifsShareAclSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CifsShareAcl object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the cifs_share_acl."""

    permission = marshmallow_fields.Str(
        data_key="permission",
        validate=enum_validation(['no_access', 'read', 'change', 'full_control']),
        allow_none=True,
    )
    r""" Specifies the access rights that a user or group has on the defined CIFS Share.
The following values are allowed:

* no_access    - User does not have CIFS share access
* read         - User has only read access
* change       - User has change access
* full_control - User has full_control access


Valid choices:

* no_access
* read
* change
* full_control"""

    sid = marshmallow_fields.Str(
        data_key="sid",
        allow_none=True,
    )
    r""" Specifies the user or group secure identifier (SID).

Example: S-1-5-21-256008430-3394229847-3930036330-1001"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the cifs_share_acl."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['windows', 'unix_user', 'unix_group']),
        allow_none=True,
    )
    r""" Specifies the type of the user or group to add to the access control
list of a CIFS share. The following values are allowed:

* windows    - Windows user or group
* unix_user  - UNIX user
* unix_group - UNIX group


Valid choices:

* windows
* unix_user
* unix_group"""

    unix_id = Size(
        data_key="unix_id",
        allow_none=True,
    )
    r""" Specifies the UNIX user or group identifier (UID/GID).

Example: 100"""

    user_or_group = marshmallow_fields.Str(
        data_key="user_or_group",
        allow_none=True,
    )
    r""" Specifies the user or group name to add to the access control list of a CIFS share.

Example: ENGDOMAIN\ad_user"""

    @property
    def resource(self):
        return CifsShareAcl

    gettable_fields = [
        "links",
        "permission",
        "share",
        "sid",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "type",
        "unix_id",
        "user_or_group",
    ]
    """links,permission,share,sid,svm.links,svm.name,svm.uuid,type,unix_id,user_or_group,"""

    patchable_fields = [
        "permission",
    ]
    """permission,"""

    postable_fields = [
        "permission",
        "type",
        "user_or_group",
    ]
    """permission,type,user_or_group,"""

class CifsShareAcl(Resource):
    r""" The permissions that users and groups have on a CIFS share. """

    _schema = CifsShareAclSchema
    _path = "/api/protocols/cifs/shares/{svm[uuid]}/{cifs_share[share]}/acls"
    _keys = ["svm.uuid", "cifs_share.share", "user_or_group", "type"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the share-level ACL on a CIFS share.
### Related ONTAP commands
* `vserver cifs share access-control show`
### Learn more
* [`DOC /protocols/cifs/shares/{svm.uuid}/{share}/acls`](#docs-NAS-protocols_cifs_shares_{svm.uuid}_{share}_acls)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all CifsShareAcl resources that match the provided query"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)


    @classmethod
    def fast_get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["RawResource"]:
        """Returns a list of RawResources that represent CifsShareAcl resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["CifsShareAcl"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a share-level ACL on a CIFS share.
### Related ONTAP commands
* `vserver cifs share access-control modify`
### Learn more
* [`DOC /protocols/cifs/shares/{svm.uuid}/{share}/acls`](#docs-NAS-protocols_cifs_shares_{svm.uuid}_{share}_acls)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["CifsShareAcl"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["CifsShareAcl"], NetAppResponse]:
        r"""Creates a share-level ACL on a CIFS share.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the share acl.
* `share` - Existing CIFS share in which to create the share acl.
* `user_or_group` - Existing user or group name for which the acl is added on the CIFS share.
* `permission` - Access rights that a user or group has on the defined CIFS share.
### Default property values
* `type` - _windows_
### Related ONTAP commands
* `vserver cifs share access-control create`
### Learn more
* [`DOC /protocols/cifs/shares/{svm.uuid}/{share}/acls`](#docs-NAS-protocols_cifs_shares_{svm.uuid}_{share}_acls)
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
        records: Iterable["CifsShareAcl"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a share-level ACL on a CIFS share.
### Related ONTAP commands
* `vserver cifs share access-control delete`
### Learn more
* [`DOC /protocols/cifs/shares/{svm.uuid}/{share}/acls`](#docs-NAS-protocols_cifs_shares_{svm.uuid}_{share}_acls)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the share-level ACL on a CIFS share.
### Related ONTAP commands
* `vserver cifs share access-control show`
### Learn more
* [`DOC /protocols/cifs/shares/{svm.uuid}/{share}/acls`](#docs-NAS-protocols_cifs_shares_{svm.uuid}_{share}_acls)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the share-level ACL on CIFS share for a specified user or group.
### Related ONTAP commands
* `vserver cifs share access-control show`
### Learn more
* [`DOC /protocols/cifs/shares/{svm.uuid}/{share}/acls`](#docs-NAS-protocols_cifs_shares_{svm.uuid}_{share}_acls)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Creates a share-level ACL on a CIFS share.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the share acl.
* `share` - Existing CIFS share in which to create the share acl.
* `user_or_group` - Existing user or group name for which the acl is added on the CIFS share.
* `permission` - Access rights that a user or group has on the defined CIFS share.
### Default property values
* `type` - _windows_
### Related ONTAP commands
* `vserver cifs share access-control create`
### Learn more
* [`DOC /protocols/cifs/shares/{svm.uuid}/{share}/acls`](#docs-NAS-protocols_cifs_shares_{svm.uuid}_{share}_acls)
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
        r"""Updates a share-level ACL on a CIFS share.
### Related ONTAP commands
* `vserver cifs share access-control modify`
### Learn more
* [`DOC /protocols/cifs/shares/{svm.uuid}/{share}/acls`](#docs-NAS-protocols_cifs_shares_{svm.uuid}_{share}_acls)
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
        r"""Deletes a share-level ACL on a CIFS share.
### Related ONTAP commands
* `vserver cifs share access-control delete`
### Learn more
* [`DOC /protocols/cifs/shares/{svm.uuid}/{share}/acls`](#docs-NAS-protocols_cifs_shares_{svm.uuid}_{share}_acls)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


