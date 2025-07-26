r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to download a software or firmware package from the server and to check the status of the software or firmware download.
<br/>
## Examples
### Downloading the software package
The following example shows how to download the software or firmware package from an HTTP or FTP server. If required, provide the url, username, and password to start the download of the package to the cluster.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SoftwarePackageDownload

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SoftwarePackageDownload()
    resource.url = "http://server/package"
    resource.username = "admin"
    resource.password = "*********"
    resource.post(hydrate=True, return_timeout=0)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
SoftwarePackageDownload(
    {"password": "*********", "username": "admin", "url": "http://server/package"}
)

```
</div>
</div>

---
The call to download the software or firmware package returns the job UUID, including a HAL link to retrieve details about the job. The job object includes a `state` field and a message to indicate the progress of the job. When the job is complete and the application is fully created, the message indicates success and the job `state` field is set to `success`.
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
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
Job(
    {
        "message": "success",
        "state": "success",
        "code": 0,
        "description": "POST /api/cluster/software/download",
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
### Checking the progress of the software package being downloaded from an HTTP or FTP server
The following example shows how to retrieve the progress status of the software package that is being
downloaded from a HTTP or FTP server.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SoftwarePackageDownload

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SoftwarePackageDownload()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
SoftwarePackageDownload(
    {"message": "Package download in progress", "state": "running", "code": 10551382}
)

```
</div>
</div>

---
### Learn more

* [`DOC /cluster/software/download`](#docs-cluster-cluster_software_download)"""

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


__all__ = ["SoftwarePackageDownload", "SoftwarePackageDownloadSchema"]
__pdoc__ = {
    "SoftwarePackageDownloadSchema.resource": False,
    "SoftwarePackageDownloadSchema.opts": False,
}


class SoftwarePackageDownloadSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SoftwarePackageDownload object"""

    code = Size(
        data_key="code",
        allow_none=True,
    )
    r""" Code returned corresponds to a download message.

Example: 10551382"""

    message = marshmallow_fields.Str(
        data_key="message",
        allow_none=True,
    )
    r""" Download progress details.

Example: Package download in progress"""

    password = marshmallow_fields.Str(
        data_key="password",
        allow_none=True,
    )
    r""" Password for download

Example: admin_password"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['not_started', 'running', 'success', 'failure']),
        allow_none=True,
    )
    r""" Download status of the package.

Valid choices:

* not_started
* running
* success
* failure"""

    url = marshmallow_fields.Str(
        data_key="url",
        allow_none=True,
    )
    r""" HTTP or FTP URL of the package through a server

Example: http://server/package"""

    username = marshmallow_fields.Str(
        data_key="username",
        allow_none=True,
    )
    r""" Username for download

Example: admin"""

    @property
    def resource(self):
        return SoftwarePackageDownload

    gettable_fields = [
        "code",
        "message",
        "state",
    ]
    """code,message,state,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "password",
        "url",
        "username",
    ]
    """password,url,username,"""

class SoftwarePackageDownload(Resource):
    """Allows interaction with SoftwarePackageDownload objects on the host"""

    _schema = SoftwarePackageDownloadSchema
    _path = "/api/cluster/software/download"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the software or firmware download status.
### Learn more
* [`DOC /cluster/software/download`](#docs-cluster-cluster_software_download)
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
        r"""Downloads a software or firmware package from the server.
### Required properties
* `url` - URL location of the software package
### Recommended optional parameters
* `username` - Username of HTTPS/FTP server
* `password` - Password of HTTPS/FTP server
### Related ONTAP commands
* `cluster image package get`
### Learn more
* [`DOC /cluster/software/download`](#docs-cluster-cluster_software_download)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)




