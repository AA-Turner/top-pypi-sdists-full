r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
ONTAP home directory functionality can be used to create home directories for SMB users on the CIFS server and automatically offer each user a dynamic share to their home directory without creating an individual SMB share for each user.<p/>
The home directory search path is a set of absolute paths from the root of an SVM that directs ONTAP to search for home directories. If there are multiple search paths, ONTAP tries them in the order specified until it finds a valid path. To use the CIFS home directories feature, at least one home directory search path must be added for an SVM. <p/>
## Examples
### Creating a home directory search path
To create a home directory search path, use the following API. Note the <i>return_records=true</i> query parameter used to obtain the newly created entry in the response.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsSearchPath

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsSearchPath()
    resource.path = "/"
    resource.svm = {"name": "vs1", "uuid": "a41fd873-ecf8-11e8-899d-0050568e9333"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
CifsSearchPath(
    {
        "svm": {"name": "vs1", "uuid": "a41fd873-ecf8-11e8-899d-0050568e9333"},
        "path": "/",
    }
)

```
</div>
</div>

---
### Retrieving the CIFS home directory search paths configuration for all SVMs in the cluster
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsSearchPath

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(CifsSearchPath.get_collection(fields="*", return_timeout=15)))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    CifsSearchPath(
        {
            "svm": {"name": "vs1", "uuid": "2d96f9aa-f4ce-11e8-b075-0050568e278e"},
            "index": 1,
            "path": "/",
        }
    ),
    CifsSearchPath(
        {
            "svm": {"name": "vs1", "uuid": "2d96f9aa-f4ce-11e8-b075-0050568e278e"},
            "index": 2,
            "path": "/a",
        }
    ),
    CifsSearchPath(
        {
            "svm": {"name": "vs2", "uuid": "4f23449b-f4ce-11e8-b075-0050568e278e"},
            "index": 1,
            "path": "/",
        }
    ),
    CifsSearchPath(
        {
            "svm": {"name": "vs2", "uuid": "4f23449b-f4ce-11e8-b075-0050568e278e"},
            "index": 2,
            "path": "/1",
        }
    ),
]

```
</div>
</div>

### Retrieving a specific home directory searchpath configuration for an SVM
The configuration returned is identified by the UUID of its SVM and the index (position) in the list of search paths that is searched to  find a home directory of a user. <br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsSearchPath

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsSearchPath(
        index=2, **{"svm.uuid": "2d96f9aa-f4ce-11e8-b075-0050568e278e"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
CifsSearchPath(
    {
        "svm": {"name": "vs1", "uuid": "2d96f9aa-f4ce-11e8-b075-0050568e278e"},
        "index": 2,
        "path": "/a",
    }
)

```
</div>
</div>

### Reordering a specific home directory search path in the list
An entry in the home directory search path list can be reordered to a new positin by specifying the 'new_index' field. The reordered configuration is identified by the UUID of its SVM and the index. <br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsSearchPath

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsSearchPath(
        index=2, **{"svm.uuid": "2d96f9aa-f4ce-11e8-b075-0050568e278e"}
    )
    resource.patch(hydrate=True, new_index=1)

```

### Removing a specific home directory search path for an SVM
The entry being removed is identified by the UUID of its SVM and the index. <br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsSearchPath

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsSearchPath(
        index=2, **{"svm.uuid": "2d96f9aa-f4ce-11e8-b075-0050568e278e"}
    )
    resource.delete()

```
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


__all__ = ["CifsSearchPath", "CifsSearchPathSchema"]
__pdoc__ = {
    "CifsSearchPathSchema.resource": False,
    "CifsSearchPathSchema.opts": False,
}


class CifsSearchPathSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CifsSearchPath object"""

    index = Size(
        data_key="index",
        allow_none=True,
    )
    r""" The position in the list of paths that is searched to find the home directory of the CIFS client. Not available in POST."""

    path = marshmallow_fields.Str(
        data_key="path",
        allow_none=True,
    )
    r""" The file system path that is searched to find the home directory of the CIFS client.

Example: /HomeDirectory/EngDomain"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the cifs_search_path."""

    @property
    def resource(self):
        return CifsSearchPath

    gettable_fields = [
        "index",
        "path",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """index,path,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "svm.name",
        "svm.uuid",
    ]
    """svm.name,svm.uuid,"""

    postable_fields = [
        "path",
        "svm.name",
        "svm.uuid",
    ]
    """path,svm.name,svm.uuid,"""

class CifsSearchPath(Resource):
    r""" This is a list of CIFS home directory search paths. When a CIFS client connects to a home directory share, these paths are searched in the order indicated by the position field to find the home directory of the connected CIFS client. """

    _schema = CifsSearchPathSchema
    _path = "/api/protocols/cifs/home-directory/search-paths"
    _keys = ["svm.uuid", "index"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves CIFS home directory search paths.
### Related ONTAP commands
* `cifs server home-directory search-path show`
### Learn more
* [`DOC /protocols/cifs/home-directory/search-paths`](#docs-NAS-protocols_cifs_home-directory_search-paths)
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
        """Returns a count of all CifsSearchPath resources that match the provided query"""
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
        """Returns a list of RawResources that represent CifsSearchPath resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["CifsSearchPath"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Reorders a CIFS home directory search path.
### Related ONTAP commands
* `cifs server home-directory search-path reorder`
### Learn more
* [`DOC /protocols/cifs/home-directory/search-paths`](#docs-NAS-protocols_cifs_home-directory_search-paths)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["CifsSearchPath"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["CifsSearchPath"], NetAppResponse]:
        r"""Creates a home directory search path.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the home directory search path.
* `path` - Path in the owning SVM namespace that is used to search for home directories.
### Related ONTAP commands
* `cifs server home-directory search-path add`
### Learn more
* [`DOC /protocols/cifs/home-directory/search-paths`](#docs-NAS-protocols_cifs_home-directory_search-paths)
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
        records: Iterable["CifsSearchPath"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a CIFS home directory search path.
### Related ONTAP commands
* `cifs server home-directory search-path remove`
### Learn more
* [`DOC /protocols/cifs/home-directory/search-paths`](#docs-NAS-protocols_cifs_home-directory_search-paths)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves CIFS home directory search paths.
### Related ONTAP commands
* `cifs server home-directory search-path show`
### Learn more
* [`DOC /protocols/cifs/home-directory/search-paths`](#docs-NAS-protocols_cifs_home-directory_search-paths)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a CIFS home directory search path of an SVM.
### Related ONTAP commands
* `cifs server home-directory search-path show`
### Learn more
* [`DOC /protocols/cifs/home-directory/search-paths`](#docs-NAS-protocols_cifs_home-directory_search-paths)
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
        r"""Creates a home directory search path.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the home directory search path.
* `path` - Path in the owning SVM namespace that is used to search for home directories.
### Related ONTAP commands
* `cifs server home-directory search-path add`
### Learn more
* [`DOC /protocols/cifs/home-directory/search-paths`](#docs-NAS-protocols_cifs_home-directory_search-paths)
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
        r"""Reorders a CIFS home directory search path.
### Related ONTAP commands
* `cifs server home-directory search-path reorder`
### Learn more
* [`DOC /protocols/cifs/home-directory/search-paths`](#docs-NAS-protocols_cifs_home-directory_search-paths)
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
        r"""Deletes a CIFS home directory search path.
### Related ONTAP commands
* `cifs server home-directory search-path remove`
### Learn more
* [`DOC /protocols/cifs/home-directory/search-paths`](#docs-NAS-protocols_cifs_home-directory_search-paths)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


