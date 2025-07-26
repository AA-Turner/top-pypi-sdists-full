r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to retrieve the software packages for a cluster.
<br/>
## Examples
### Retrieving cluster software packages information
The following example shows how to retrieve the ONTAP software packages in a cluster.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SoftwarePackage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(SoftwarePackage.get_collection(return_timeout=15)))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    SoftwarePackage(
        {
            "_links": {"self": {"href": "/api/cluster/software/packages/9.7.0"}},
            "version": "9.7.0",
        }
    ),
    SoftwarePackage(
        {
            "_links": {"self": {"href": "/api/cluster/software/packages/9.5.0"}},
            "version": "9.5.0",
        }
    ),
]

```
</div>
</div>

---
### Retrieves the software package information for a particular version
The following example shows how to retrieve the details of a given cluster software package.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SoftwarePackage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SoftwarePackage(version="9.7.0")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
SoftwarePackage(
    {
        "create_time": "2018-05-21T10:06:59+05:30",
        "_links": {"self": {"href": "/api/cluster/software/packages/9.7.0"}},
        "version": "9.7.0",
    }
)

```
</div>
</div>

---
### Deleting a cluster software package
The following example shows how to delete a package from the cluster. You need to provide the package version that you want to delete. The software package delete creates a job to perform the delete operation.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SoftwarePackage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SoftwarePackage(version="9.6.0")
    resource.delete()

```

---
The call to delete the package returns the job UUID, including a HAL link to retrieve details about the job. The job object includes a `state` field and a message to indicate the progress of the job. When the job is complete and the application is fully created, the message indicates success and the job `state` field is set to `success`.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Job

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Job(uuid="f587d316-5feb-11e8-b0e0-005056956dfc")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
Job(
    {
        "message": "success",
        "state": "success",
        "code": 0,
        "description": "DELETE /api/cluster/software/packages/9.6.0",
        "uuid": "f587d316-5feb-11e8-b0e0-005056956dfc",
        "_links": {
            "self": {"href": "/api/cluster/jobs/f587d316-5feb-11e8-b0e0-005056956dfc"}
        },
    }
)

```
</div>
</div>

---
### Learn more

* [`DOC /cluster/software/packages`](#docs-cluster-cluster_software_packages)"""

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


__all__ = ["SoftwarePackage", "SoftwarePackageSchema"]
__pdoc__ = {
    "SoftwarePackageSchema.resource": False,
    "SoftwarePackageSchema.opts": False,
}


class SoftwarePackageSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SoftwarePackage object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the software_package."""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" Indicates when this package was loaded

Example: 2019-02-04T19:00:00.000+0000"""

    version = marshmallow_fields.Str(
        data_key="version",
        allow_none=True,
    )
    r""" Version of this package

Example: ONTAP_X"""

    @property
    def resource(self):
        return SoftwarePackage

    gettable_fields = [
        "links",
        "create_time",
        "version",
    ]
    """links,create_time,version,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class SoftwarePackage(Resource):
    """Allows interaction with SoftwarePackage objects on the host"""

    _schema = SoftwarePackageSchema
    _path = "/api/cluster/software/packages"
    _keys = ["version"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the software packages for a cluster.
### Related ONTAP commands
* `cluster image package show-repository`
### Learn more
* [`DOC /cluster/software/packages`](#docs-cluster-cluster_software_packages)
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
        """Returns a count of all SoftwarePackage resources that match the provided query"""
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
        """Returns a list of RawResources that represent SoftwarePackage resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)



    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["SoftwarePackage"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a software package from the cluster. The delete operation fails if the package is currently installed.
### Related ONTAP commands
* `cluster image package delete`
### Learn more
* [`DOC /cluster/software/packages`](#docs-cluster-cluster_software_packages)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the software packages for a cluster.
### Related ONTAP commands
* `cluster image package show-repository`
### Learn more
* [`DOC /cluster/software/packages`](#docs-cluster-cluster_software_packages)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the software package information.
### Related ONTAP commands
* `cluster image package show-repository`
### Learn more
* [`DOC /cluster/software/packages`](#docs-cluster-cluster_software_packages)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)



    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a software package from the cluster. The delete operation fails if the package is currently installed.
### Related ONTAP commands
* `cluster image package delete`
### Learn more
* [`DOC /cluster/software/packages`](#docs-cluster-cluster_software_packages)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


