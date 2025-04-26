r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Before any users or applications can access data on the CIFS server over SMB, a CIFS share must be created with sufficient share permissions. CIFS share is a named access point in a volume which is tied to the CIFS server on the SVM. Before creating a CIFS share make sure that the path is valid within the scope of the SVM and that it is reachable.</br>
Permissions can be assigned to this newly created share by specifying the 'acls' field. When a CIFS share is created, ONTAP creates a default ACL for this share with 'Full-Control' permissions for an 'Everyone' user.
## Examples
### Creating a CIFS share
To create a CIFS share for a CIFS server, use the following API. Note the <i>return_records=true</i> query parameter used to obtain the newly created entry in the response.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsShare

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsShare()
    resource.access_based_enumeration = False
    resource.acls = [
        {"permission": "no_access", "type": "unix_user", "user_or_group": "root"}
    ]
    resource.change_notify = True
    resource.comment = "HR Department Share"
    resource.encryption = False
    resource.home_directory = False
    resource.name = "TEST"
    resource.oplocks = True
    resource.no_strict_security = True
    resource.path = "/"
    resource.svm = {"name": "vs1", "uuid": "6d8e8870-8753-11eb-8d86-0050568ea61a"}
    resource.unix_symlink = "local"
    resource.show_snapshot = True
    resource.continuously_available = False
    resource.namespace_caching = True
    resource.allow_unencrypted_access = False
    resource.file_umask = "025"
    resource.dir_umask = "026"
    resource.offline_files = "documents"
    resource.vscan_profile = "standard"
    resource.force_group_for_create = "root"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
CifsShare(
    {
        "namespace_caching": True,
        "name": "TEST",
        "svm": {"name": "vs1", "uuid": "6d8e8870-8753-11eb-8d86-0050568ea61a"},
        "path": "/",
        "no_strict_security": True,
        "continuously_available": False,
        "change_notify": True,
        "acls": [
            {
                "win_sid_unix_id": "0",
                "permission": "no_access",
                "type": "unix_user",
                "user_or_group": "root",
            }
        ],
        "offline_files": "documents",
        "vscan_profile": "standard",
        "access_based_enumeration": False,
        "file_umask": "25",
        "comment": "HR Department Share",
        "unix_symlink": "local",
        "allow_unencrypted_access": False,
        "force_group_for_create": "root",
        "home_directory": False,
        "dir_umask": "26",
        "oplocks": True,
        "show_snapshot": True,
        "encryption": False,
    }
)

```
</div>
</div>

---
### Retrieving CIFS Shares for all SVMs in the cluster
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsShare

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(CifsShare.get_collection(fields="*", return_timeout=15)))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    CifsShare(
        {
            "namespace_caching": False,
            "name": "c$",
            "_links": {
                "self": {
                    "href": "/api/protocols/cifs/shares/6d8e8870-8753-11eb-8d86-0050568ea61a/c%24"
                }
            },
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/6d8e8870-8753-11eb-8d86-0050568ea61a"
                    }
                },
                "uuid": "6d8e8870-8753-11eb-8d86-0050568ea61a",
            },
            "path": "/",
            "continuously_available": False,
            "change_notify": True,
            "acls": [
                {
                    "win_sid_unix_id": "S-1-1-0",
                    "permission": "full_control",
                    "type": "windows",
                    "user_or_group": "BUILTIN\\Administrators",
                }
            ],
            "vscan_profile": "standard",
            "access_based_enumeration": False,
            "unix_symlink": "local",
            "allow_unencrypted_access": True,
            "home_directory": False,
            "volume": {"name": "vol1", "uuid": "6f4fb33a-8753-11eb-8d86-0050568ea61a"},
            "oplocks": True,
            "show_snapshot": False,
            "encryption": False,
        }
    ),
    CifsShare(
        {
            "namespace_caching": False,
            "name": "ipc$",
            "_links": {
                "self": {
                    "href": "/api/protocols/cifs/shares/6d8e8870-8753-11eb-8d86-0050568ea61a/ipc%24"
                }
            },
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/6d8e8870-8753-11eb-8d86-0050568ea61a"
                    }
                },
                "uuid": "6d8e8870-8753-11eb-8d86-0050568ea61a",
            },
            "path": "/",
            "continuously_available": False,
            "change_notify": False,
            "vscan_profile": "standard",
            "access_based_enumeration": False,
            "allow_unencrypted_access": False,
            "home_directory": False,
            "volume": {"name": "vol1", "uuid": "6f4fb33a-8753-11eb-8d86-0050568ea61a"},
            "oplocks": False,
            "show_snapshot": False,
            "encryption": False,
        }
    ),
    CifsShare(
        {
            "namespace_caching": True,
            "name": "TEST",
            "_links": {
                "self": {
                    "href": "/api/protocols/cifs/shares/6d8e8870-8753-11eb-8d86-0050568ea61a/TEST"
                }
            },
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/6d8e8870-8753-11eb-8d86-0050568ea61a"
                    }
                },
                "uuid": "6d8e8870-8753-11eb-8d86-0050568ea61a",
            },
            "path": "/",
            "no_strict_security": True,
            "continuously_available": False,
            "change_notify": True,
            "acls": [
                {
                    "win_sid_unix_id": "S-1-1-0",
                    "permission": "full_control",
                    "type": "windows",
                    "user_or_group": "Everyone",
                },
                {
                    "win_sid_unix_id": "0",
                    "permission": "no_access",
                    "type": "unix_user",
                    "user_or_group": "root",
                },
            ],
            "offline_files": "documents",
            "vscan_profile": "standard",
            "access_based_enumeration": False,
            "file_umask": "25",
            "comment": "HR Department Share",
            "unix_symlink": "local",
            "allow_unencrypted_access": True,
            "force_group_for_create": "root",
            "home_directory": False,
            "volume": {"name": "vol1", "uuid": "6f4fb33a-8753-11eb-8d86-0050568ea61a"},
            "dir_umask": "26",
            "oplocks": True,
            "show_snapshot": True,
            "encryption": False,
        }
    ),
]

```
</div>
</div>

---
### Retrieving all CIFS Shares for all SVMs in the cluster for which the acls are configured for a "root" user
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsShare

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            CifsShare.get_collection(
                fields="*", return_timeout=15, **{"acls.user_or_group": "root"}
            )
        )
    )

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    CifsShare(
        {
            "namespace_caching": True,
            "name": "TEST",
            "svm": {"name": "vs1", "uuid": "6d8e8870-8753-11eb-8d86-0050568ea61a"},
            "path": "/",
            "no_strict_security": True,
            "continuously_available": False,
            "change_notify": True,
            "acls": [
                {
                    "win_sid_unix_id": "S-1-1-0",
                    "permission": "full_control",
                    "type": "windows",
                    "user_or_group": "Everyone",
                },
                {
                    "win_sid_unix_id": "0",
                    "permission": "no_access",
                    "type": "unix_user",
                    "user_or_group": "root",
                },
            ],
            "offline_files": "documents",
            "vscan_profile": "standard",
            "access_based_enumeration": False,
            "file_umask": "25",
            "comment": "HR Department Share",
            "unix_symlink": "local",
            "allow_unencrypted_access": True,
            "force_group_for_create": "root",
            "home_directory": False,
            "volume": {"name": "vol1", "uuid": "6f4fb33a-8753-11eb-8d86-0050568ea61a"},
            "dir_umask": "26",
            "oplocks": True,
            "show_snapshot": True,
            "encryption": False,
        }
    )
]

```
</div>
</div>

### Retrieving a specific CIFS share configuration for an SVM
The configuration being returned is identified by the UUID of its SVM and the name of the share.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsShare

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsShare(
        name="TEST", **{"svm.uuid": "6d8e8870-8753-11eb-8d86-0050568ea61a"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
CifsShare(
    {
        "namespace_caching": True,
        "name": "TEST",
        "svm": {"name": "vs1", "uuid": "6d8e8870-8753-11eb-8d86-0050568ea61a"},
        "path": "/",
        "no_strict_security": True,
        "continuously_available": False,
        "change_notify": True,
        "acls": [
            {
                "win_sid_unix_id": "S-1-1-0",
                "permission": "full_control",
                "type": "windows",
                "user_or_group": "Everyone",
            },
            {
                "win_sid_unix_id": "0",
                "permission": "no_access",
                "type": "unix_user",
                "user_or_group": "root",
            },
        ],
        "offline_files": "documents",
        "vscan_profile": "standard",
        "access_based_enumeration": False,
        "file_umask": "25",
        "comment": "HR Department Share",
        "unix_symlink": "local",
        "allow_unencrypted_access": True,
        "force_group_for_create": "root",
        "home_directory": False,
        "volume": {"name": "vol1", "uuid": "6f4fb33a-8753-11eb-8d86-0050568ea61a"},
        "dir_umask": "26",
        "oplocks": True,
        "show_snapshot": True,
        "encryption": False,
    }
)

```
</div>
</div>

### Updating a specific CIFS share for an SVM
The CIFS share being modified is identified by the UUID of its SVM and the CIFS share name. The CIFS share ACLs cannot be modified with this API.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsShare

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsShare(
        name="TEST", **{"svm.uuid": "6d8e8870-8753-11eb-8d86-0050568ea61a"}
    )
    resource.access_based_enumeration = True
    resource.change_notify = True
    resource.comment = "HR Department Share"
    resource.encryption = False
    resource.oplocks = True
    resource.no_strict_security = True
    resource.path = "/"
    resource.unix_symlink = "widelink"
    resource.show_snapshot = False
    resource.continuously_available = True
    resource.namespace_caching = False
    resource.allow_unencrypted_access = True
    resource.file_umask = "022"
    resource.dir_umask = "022"
    resource.offline_files = "programs"
    resource.vscan_profile = "no_scan"
    resource.force_group_for_create = "root"
    resource.patch()

```

### Removing a specific CIFS share for an SVM
The CIFS share being removed is identified by the UUID of its SVM and the CIFS share name.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsShare

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsShare(
        name="test", **{"svm.uuid": "6d8e8870-8753-11eb-8d86-0050568ea61a"}
    )
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


__all__ = ["CifsShare", "CifsShareSchema"]
__pdoc__ = {
    "CifsShareSchema.resource": False,
    "CifsShareSchema.opts": False,
}


class CifsShareSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CifsShare object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the cifs_share."""

    access_based_enumeration = marshmallow_fields.Boolean(
        data_key="access_based_enumeration",
        allow_none=True,
    )
    r""" If enabled, all folders inside this share are visible to a user based on that individual user access right; prevents
the display of folders or other shared resources that the user does not have access to."""

    acls = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.share_acl.ShareAclSchema", unknown=EXCLUDE, allow_none=True), data_key="acls", allow_none=True)
    r""" The permissions that users and groups have on a CIFS share."""

    allow_unencrypted_access = marshmallow_fields.Boolean(
        data_key="allow_unencrypted_access",
        allow_none=True,
    )
    r""" Specifies whether or not the SMB2 clients are allowed to access the encrypted share."""

    attribute_cache = marshmallow_fields.Boolean(
        data_key="attribute_cache",
        allow_none=True,
    )
    r""" Specifies that connections through this share cache attributes for a short time to improve performance."""

    browsable = marshmallow_fields.Boolean(
        data_key="browsable",
        allow_none=True,
    )
    r""" Specifies whether or not the Windows clients can browse the share."""

    change_notify = marshmallow_fields.Boolean(
        data_key="change_notify",
        allow_none=True,
    )
    r""" Specifies whether CIFS clients can request for change notifications for directories on this share."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        validate=len_validation(minimum=1, maximum=256),
        allow_none=True,
    )
    r""" Specify the CIFS share descriptions.

Example: HR Department Share"""

    continuously_available = marshmallow_fields.Boolean(
        data_key="continuously_available",
        allow_none=True,
    )
    r""" Specifies whether or not the clients connecting to this share can open files in a persistent manner.
Files opened in this way are protected from disruptive events, such as, failover and giveback."""

    dir_umask = marshmallow_fields.Str(
        data_key="dir_umask",
        allow_none=True,
    )
    r""" Directory Mode Creation Mask to be viewed as an octal number.

Example: 21"""

    encryption = marshmallow_fields.Boolean(
        data_key="encryption",
        allow_none=True,
    )
    r""" Specifies that SMB encryption must be used when accessing this share. Clients that do not support encryption are not
able to access this share."""

    file_umask = marshmallow_fields.Str(
        data_key="file_umask",
        allow_none=True,
    )
    r""" File Mode Creation Mask to be viewed as an octal number.

Example: 21"""

    force_group_for_create = marshmallow_fields.Str(
        data_key="force_group_for_create",
        allow_none=True,
    )
    r""" Specifies that all files that CIFS users create in a specific share belong to the same group
(also called the "force-group"). The "force-group" must be a predefined group in the UNIX group
database. This setting has no effect unless the security style of the volume is UNIX or mixed
security style."""

    home_directory = marshmallow_fields.Boolean(
        data_key="home_directory",
        allow_none=True,
    )
    r""" Specifies whether or not the share is a home directory share, where the share and path names are dynamic.
ONTAP home directory functionality automatically offer each user a dynamic share to their home directory without creating an
individual SMB share for each user.
The ONTAP CIFS home directory feature enable us to configure a share that maps to
different directories based on the user that connects to it. Instead of creating a separate shares for each user,
a single share with a home directory parameters can be created.
In a home directory share, ONTAP dynamically generates the share-name and share-path by substituting
%w, %u, and %d variables with the corresponding Windows user name, UNIX user name, and domain name, respectively."""

    max_connections_per_share = Size(
        data_key="max_connections_per_share",
        allow_none=True,
    )
    r""" Maximum number of tree connections on share."""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=80),
        allow_none=True,
    )
    r""" Specifies the name of the CIFS share that you want to create. If this
is a home directory share then the share name includes the pattern as
%w (Windows user name), %u (UNIX user name) and %d (Windows domain name)
variables in any combination with this parameter to generate shares dynamically.


Example: HR_SHARE"""

    namespace_caching = marshmallow_fields.Boolean(
        data_key="namespace_caching",
        allow_none=True,
    )
    r""" Specifies whether or not the SMB clients connecting to this share can cache the directory enumeration
results returned by the CIFS servers."""

    no_strict_security = marshmallow_fields.Boolean(
        data_key="no_strict_security",
        allow_none=True,
    )
    r""" Specifies whether or not CIFS clients can follow a unix symlinks outside the share boundaries."""

    offline_files = marshmallow_fields.Str(
        data_key="offline_files",
        validate=enum_validation(['none', 'manual', 'documents', 'programs']),
        allow_none=True,
    )
    r""" Offline Files
The supported values are:

  * none - Clients are not permitted to cache files for offline access.
  * manual - Clients may cache files that are explicitly selected by the user for offline access.
  * documents - Clients may automatically cache files that are used by the user for offline access.
  * programs - Clients may automatically cache files that are used by the user for offline access
               and may use those files in an offline mode even if the share is available.


Valid choices:

* none
* manual
* documents
* programs"""

    oplocks = marshmallow_fields.Boolean(
        data_key="oplocks",
        allow_none=True,
    )
    r""" Specify whether opportunistic locks are enabled on this share. "Oplocks" allow clients to lock files and cache content locally,
which can increase performance for file operations."""

    path = marshmallow_fields.Str(
        data_key="path",
        validate=len_validation(minimum=1, maximum=256),
        allow_none=True,
    )
    r""" The fully-qualified pathname in the owning SVM namespace that is shared through this share.
If this is a home directory share then the path should be dynamic by specifying the pattern
%w (Windows user name), %u (UNIX user name), or %d (domain name) variables in any combination.
ONTAP generates the path dynamically for the connected user and this path is appended to each
search path to find the full Home Directory path.


Example: /volume_1/eng_vol/"""

    show_previous_versions = marshmallow_fields.Boolean(
        data_key="show_previous_versions",
        allow_none=True,
    )
    r""" Specifies that the previous version can be viewed and restored from the client."""

    show_snapshot = marshmallow_fields.Boolean(
        data_key="show_snapshot",
        allow_none=True,
    )
    r""" Specifies whether or not the snapshots can be viewed and traversed by clients."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the cifs_share."""

    unix_symlink = marshmallow_fields.Str(
        data_key="unix_symlink",
        validate=enum_validation(['local', 'widelink', 'disable']),
        allow_none=True,
    )
    r""" Controls the access of UNIX symbolic links to CIFS clients.
The supported values are:

    * local - Enables only local symbolic links which is within the same CIFS share.
    * widelink - Enables both local symlinks and widelinks.
    * disable - Disables local symlinks and widelinks.


Valid choices:

* local
* widelink
* disable"""

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE, allow_none=True)
    r""" The volume field of the cifs_share."""

    vscan_profile = marshmallow_fields.Str(
        data_key="vscan_profile",
        validate=enum_validation(['no_scan', 'standard', 'strict', 'writes_only']),
        allow_none=True,
    )
    r""" Vscan File-Operations Profile
The supported values are:

  * no_scan - Virus scans are never triggered for accesses to this share.
  * standard - Virus scans can be triggered by open, close, and rename operations.
  * strict - Virus scans can be triggered by open, read, close, and rename operations.
  * writes_only - Virus scans can be triggered only when a file that has been modified is closed.


Valid choices:

* no_scan
* standard
* strict
* writes_only"""

    @property
    def resource(self):
        return CifsShare

    gettable_fields = [
        "links",
        "access_based_enumeration",
        "acls",
        "allow_unencrypted_access",
        "attribute_cache",
        "browsable",
        "change_notify",
        "comment",
        "continuously_available",
        "dir_umask",
        "encryption",
        "file_umask",
        "force_group_for_create",
        "home_directory",
        "max_connections_per_share",
        "name",
        "namespace_caching",
        "no_strict_security",
        "offline_files",
        "oplocks",
        "path",
        "show_previous_versions",
        "show_snapshot",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "unix_symlink",
        "volume.links",
        "volume.name",
        "volume.uuid",
        "vscan_profile",
    ]
    """links,access_based_enumeration,acls,allow_unencrypted_access,attribute_cache,browsable,change_notify,comment,continuously_available,dir_umask,encryption,file_umask,force_group_for_create,home_directory,max_connections_per_share,name,namespace_caching,no_strict_security,offline_files,oplocks,path,show_previous_versions,show_snapshot,svm.links,svm.name,svm.uuid,unix_symlink,volume.links,volume.name,volume.uuid,vscan_profile,"""

    patchable_fields = [
        "access_based_enumeration",
        "allow_unencrypted_access",
        "attribute_cache",
        "browsable",
        "change_notify",
        "comment",
        "continuously_available",
        "dir_umask",
        "encryption",
        "file_umask",
        "force_group_for_create",
        "max_connections_per_share",
        "namespace_caching",
        "no_strict_security",
        "offline_files",
        "oplocks",
        "path",
        "show_previous_versions",
        "show_snapshot",
        "unix_symlink",
        "vscan_profile",
    ]
    """access_based_enumeration,allow_unencrypted_access,attribute_cache,browsable,change_notify,comment,continuously_available,dir_umask,encryption,file_umask,force_group_for_create,max_connections_per_share,namespace_caching,no_strict_security,offline_files,oplocks,path,show_previous_versions,show_snapshot,unix_symlink,vscan_profile,"""

    postable_fields = [
        "access_based_enumeration",
        "acls",
        "allow_unencrypted_access",
        "attribute_cache",
        "browsable",
        "change_notify",
        "comment",
        "continuously_available",
        "dir_umask",
        "encryption",
        "file_umask",
        "force_group_for_create",
        "home_directory",
        "max_connections_per_share",
        "name",
        "namespace_caching",
        "no_strict_security",
        "offline_files",
        "oplocks",
        "path",
        "show_previous_versions",
        "show_snapshot",
        "svm.name",
        "svm.uuid",
        "unix_symlink",
        "vscan_profile",
    ]
    """access_based_enumeration,acls,allow_unencrypted_access,attribute_cache,browsable,change_notify,comment,continuously_available,dir_umask,encryption,file_umask,force_group_for_create,home_directory,max_connections_per_share,name,namespace_caching,no_strict_security,offline_files,oplocks,path,show_previous_versions,show_snapshot,svm.name,svm.uuid,unix_symlink,vscan_profile,"""

class CifsShare(Resource):
    r""" CIFS share is a named access point in a volume. Before users and applications can access data on the CIFS server over SMB,
a CIFS share must be created with sufficient share permission. CIFS shares are tied to the CIFS server on the SVM.
When a CIFS share is created, ONTAP creates a default ACL for the share with Full Control permissions for Everyone. """

    _schema = CifsShareSchema
    _path = "/api/protocols/cifs/shares"
    _keys = ["svm.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves CIFS shares.
### Related ONTAP commands
* `vserver cifs share show`
* `vserver cifs share properties show`
### Learn more
* [`DOC /protocols/cifs/shares`](#docs-NAS-protocols_cifs_shares)
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
        """Returns a count of all CifsShare resources that match the provided query"""
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
        """Returns a list of RawResources that represent CifsShare resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["CifsShare"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a CIFS share.
### Related ONTAP commands
* `vserver cifs share modify`
* `vserver cifs share properties add`
* `vserver cifs share properties remove`
### Learn more
* [`DOC /protocols/cifs/shares`](#docs-NAS-protocols_cifs_shares)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["CifsShare"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["CifsShare"], NetAppResponse]:
        r"""Creates a CIFS share.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the CIFS share.
* `name` - Name of the CIFS share.
* `path` - Path in the owning SVM namespace that is shared through this share.
### Recommended optional properties
* `comment` - Optionally choose to add a text comment of up to 256 characters about the CIFS share.
* `acls` - Optionally choose to add share permissions that users and groups have on the CIFS share.
### Default property values
If not specified in POST, the following default property values are assigned:
* `home_directory` - _false_
* `oplocks` - _true_
* `access_based_enumeration` - _false_
* `change_notify` - _true_
* `encryption` - _false_
* `unix_symlink` - _local_
### Related ONTAP commands
* `vserver cifs share create`
* `vserver cifs share properties add`
* `vserver cifs share access-control create`
### Learn more
* [`DOC /protocols/cifs/shares`](#docs-NAS-protocols_cifs_shares)
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
        records: Iterable["CifsShare"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a CIFS share.
### Related ONTAP commands
* `vserver cifs share delete`
### Learn more
* [`DOC /protocols/cifs/shares`](#docs-NAS-protocols_cifs_shares)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves CIFS shares.
### Related ONTAP commands
* `vserver cifs share show`
* `vserver cifs share properties show`
### Learn more
* [`DOC /protocols/cifs/shares`](#docs-NAS-protocols_cifs_shares)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a CIFS share.
### Related ONTAP commands
* `vserver cifs share show`
* `vserver cifs share properties show`
### Learn more
* [`DOC /protocols/cifs/shares`](#docs-NAS-protocols_cifs_shares)
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
        r"""Creates a CIFS share.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the CIFS share.
* `name` - Name of the CIFS share.
* `path` - Path in the owning SVM namespace that is shared through this share.
### Recommended optional properties
* `comment` - Optionally choose to add a text comment of up to 256 characters about the CIFS share.
* `acls` - Optionally choose to add share permissions that users and groups have on the CIFS share.
### Default property values
If not specified in POST, the following default property values are assigned:
* `home_directory` - _false_
* `oplocks` - _true_
* `access_based_enumeration` - _false_
* `change_notify` - _true_
* `encryption` - _false_
* `unix_symlink` - _local_
### Related ONTAP commands
* `vserver cifs share create`
* `vserver cifs share properties add`
* `vserver cifs share access-control create`
### Learn more
* [`DOC /protocols/cifs/shares`](#docs-NAS-protocols_cifs_shares)
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
        r"""Updates a CIFS share.
### Related ONTAP commands
* `vserver cifs share modify`
* `vserver cifs share properties add`
* `vserver cifs share properties remove`
### Learn more
* [`DOC /protocols/cifs/shares`](#docs-NAS-protocols_cifs_shares)
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
        r"""Deletes a CIFS share.
### Related ONTAP commands
* `vserver cifs share delete`
### Learn more
* [`DOC /protocols/cifs/shares`](#docs-NAS-protocols_cifs_shares)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


