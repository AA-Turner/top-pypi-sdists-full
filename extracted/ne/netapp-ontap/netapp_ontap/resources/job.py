r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to view and manipulate jobs. Jobs provide information about asynchronous operations. Some long-running jobs are paused or cancelled by calling a PATCH request. Individual operations indicate if they support PATCH requests on the job. After a job transitions to a terminal state, it is deleted after a default time of 300 seconds. Attempts to call a GET or PATCH request on the job returns a 404 error code After the job has been deleted.
## Example
The following examples show how to retrieve and update a job state:
### Retrieving job information
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Job

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Job(uuid="b5145e1d-b53b-11e8-8252-005056bbd8f5")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
Job(
    {
        "description": "Cluster Backup Job",
        "code": 0,
        "message": "creating_node_backups",
        "state": "running",
        "uuid": "b5145e1d-b53b-11e8-8252-005056bbd8f5",
        "_links": {
            "self": {"href": "/api/cluster/jobs/b5145e1d-b53b-11e8-8252-005056bbd8f5"}
        },
    }
)

```
</div>
</div>

---
### Updating a job that supports the new state
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Job

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Job(uuid="b5145e1d-b53b-11e8-8252-005056bbd8f5")
    resource.patch(hydrate=True, action="cancel")

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


__all__ = ["Job", "JobSchema"]
__pdoc__ = {
    "JobSchema.resource": False,
    "JobSchema.opts": False,
}


class JobSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Job object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the job."""

    code = Size(
        data_key="code",
        allow_none=True,
    )
    r""" If the state indicates "failure", this is the final error code.

Example: 0"""

    description = marshmallow_fields.Str(
        data_key="description",
        allow_none=True,
    )
    r""" The description of the job to help identify it independent of the UUID.

Example: App Snapshot Job"""

    end_time = ImpreciseDateTime(
        data_key="end_time",
        allow_none=True,
    )
    r""" The time the job ended."""

    error = marshmallow_fields.Nested("netapp_ontap.models.error.ErrorSchema", data_key="error", unknown=EXCLUDE, allow_none=True)
    r""" The error field of the job."""

    message = marshmallow_fields.Str(
        data_key="message",
        allow_none=True,
    )
    r""" A message corresponding to the state of the job providing additional details about the current state.

Example: Complete: Successful"""

    node = marshmallow_fields.Nested("netapp_ontap.models.job_node.JobNodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node where this job was run"""

    start_time = ImpreciseDateTime(
        data_key="start_time",
        allow_none=True,
    )
    r""" The time the job started."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['queued', 'running', 'paused', 'success', 'failure']),
        allow_none=True,
    )
    r""" The state of the job.

Valid choices:

* queued
* running
* paused
* success
* failure"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the job."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The uuid field of the job.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return Job

    gettable_fields = [
        "links",
        "code",
        "description",
        "end_time",
        "error",
        "message",
        "node",
        "start_time",
        "state",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """links,code,description,end_time,error,message,node,start_time,state,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class Job(Resource):
    """Allows interaction with Job objects on the host"""

    _schema = JobSchema
    _path = "/api/cluster/jobs"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of recently running asynchronous jobs. After a job transitions to a failure or success state, it is deleted after a default time of 300 seconds.
### Learn more
* [`DOC /cluster/jobs`](#docs-cluster-cluster_jobs)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all Job resources that match the provided query"""
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
        """Returns a list of RawResources that represent Job resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Job"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the state of a specific asynchronous job.
### Learn more
* [`DOC /cluster/jobs`](#docs-cluster-cluster_jobs)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of recently running asynchronous jobs. After a job transitions to a failure or success state, it is deleted after a default time of 300 seconds.
### Learn more
* [`DOC /cluster/jobs`](#docs-cluster-cluster_jobs)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the details of a specific asynchronous job. After a job transitions to a failure or success state, it is deleted after a default time of 300 seconds.
### Learn more
* [`DOC /cluster/jobs`](#docs-cluster-cluster_jobs)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)


    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the state of a specific asynchronous job.
### Learn more
* [`DOC /cluster/jobs`](#docs-cluster-cluster_jobs)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



