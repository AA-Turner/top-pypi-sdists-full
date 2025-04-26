r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to create, perform operations, and retrieve relevant information pertaining to MetroCluster DR groups. The GET operation retrieves all the DR groups in the MetroCluster over IP configuration or a DR group information specified by the DR group id. The POST request can be used to create a new DR group in the MetroCluster over IP configuration. The DELETE operation removes a DR group information specified by the DR group id from the existing MetroCluster over IP configuration.
## Creating a new DR group
A new DR group in MetroCluster over IP configuration is created by issuing a POST to /cluster/metrocluster/dr-groups. Parameters are provided in the body of the POST request.
This operation requires a valid MetroCluster over IP configuration. The new nodes added belong to either the local or partner cluster.
### Fields used for setting up a new DR group
The fields used for MetroCluster APIs are either required or optional and are described as follows:
### Required configuration fields
These fields are always required for any POST /cluster/dr-groups request.

* `partner_cluster.name` - Specifies the partner cluster name to which cluster peering has been established.
* `dr_pairs` - Specifies local and DR partner node pairs.  Each pair uniquely identifies a DR group.
### Optional configuration fields
This field is used to set up additional MetroCluster DR configuration.

* `mccip_ports` - Specifies relevant layer 3 network configuration information for each port. These include port name, node name, IP address, gateway, and netmask. If mccip_ports is not provided, then the API automatically generates IP addresses for the ports and creates an layer 2 network configuration.
### Polling the create job
After a successful POST /cluster/metrocluster/dr-groups is issued, an HTTP status code of 202 (Accepted) is returned along with a job UUID and a link in the body of the response. The create job continues asynchronously and can be monitored by using the job UUID and the /cluster/jobs API. The "message" field in the response of the GET /cluster/jobs/{uuid} request shows the current step in the job, and the "state" field shows the overall state of the job.
## Deleting a DR group using ID
A DR group in MetroCluster over IP configuration can be deleted by issuing a DELETE to /cluster/metrocluster/dr-groups/{id}. No parameters are required for the DELETE request.
The following preparation steps must be completed on the local and partner clusters before removing a DR group.

* Move all the data volumes to another DR group.
* Move all the MDV_CRS metadata volumes to another DR group.
* Delete all the MDV_aud metadata volumes that may exist in the DR group to be removed.
* Delete all the data aggregates in the DR group to be removed. Root aggregates are not deleted.
* Migrate all the data LIFs to home nodes in another DR group.
* Migrate the cluster management LIF to a home node in another DR group. Node management and inter-cluster LIFs are not migrated.
* Transfer epsilon to a node in another DR group.
The operation is refused if the preparation steps are not completed on the local and partner clusters.
### Polling the delete job
After a successful DELETE /cluster/metrocluster/dr-groups is issued, an HTTP status code of 202 (Accepted) is returned along with a job UUID and a link in the body of the response. The delete job continues asynchronously and can be monitored by using the job UUID and the /cluster/jobs API. The "message" field in the response of the GET /cluster/jobs/{uuid} request shows the current step in the job, and the "state" field shows the overall state of the job.
<br/>
---
## Examples
### Creating a DR group for MetroCluster over IP configuration
This example shows the POST body when creating a DR group for MetroCluster.
```
# API
/api/cluster/metrocluster/dr-groups
```
### POST body included from file
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import MetroclusterDrGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = MetroclusterDrGroup()
    resource.partner_cluster = {"name": "mcc_siteB"}
    resource.dr_pairs = [{"node": {"name": "node-e"}, "partner": {"name": "node-g"}}]
    resource.post(hydrate=True)
    print(resource)

```

### Inline POST body
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import MetroclusterDrGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = MetroclusterDrGroup()
    resource.partner_cluster = {"name": "mcc_siteB"}
    resource.dr_pairs = [{"node": {"name": "node-e"}, "partner": {"name": "node-g"}}]
    resource.post(hydrate=True)
    print(resource)

```

### POST Response
```
HTTP/1.1 202 Accepted
Date: Fri, 18 Sep 2020 20:38:05 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Location: /api/cluster/metrocluster/dr-groups
Content-Length: 189
Content-Type: application/hal+json
{
  "job": {
    "uuid": "5b89472e-f9e8-11ea-9c31-005056bb42f7",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/5b89472e-f9e8-11ea-9c31-005056bb42f7"
      }
    }
  }
}
```
### Monitoring the job progress
Use the link provided in the response to the POST request to fetch information for the DR group job.
<br/>
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Job

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Job(uuid="5b89472e-f9e8-11ea-9c31-005056bb42f7")
    resource.get()
    print(resource)

```

<br/>
#### Job status response
The following is an example of the job status response returned by the running DR group job:
<br/>
```
HTTP/1.1 200 OK
Date: Fri, 18 Sep 2020 20:40:20 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Length: 373
Content-Type: application/hal+json
{
  "uuid": "5b89472e-f9e8-11ea-9c31-005056bb42f7",
  "description": "POST /api/cluster/metrocluster/dr-groups/",
  "state": "running",
  "message": "Mirroring aggregates",
  "code": 2432845,
  "start_time": "2020-09-18T15:38:08-04:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/5b89472e-f9e8-11ea-9c31-005056bb42f7"
    }
  }
}
```
#### Final status of a successful DR Group create workflow
When the create job completes, the 'end_time' field is populated, and the 'state' and 'message' fields report final status.
<br/>
```
HTTP/1.1 200 OK
Date: Fri, 18 Sep 2020 20:43:54 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Length: 373
Content-Type: application/hal+json
{
  "uuid": "5b89472e-f9e8-11ea-9c31-005056bb42f7",
  "description": "POST /api/cluster/metrocluster/dr-groups/",
  "state": "success",
  "message": "success",
  "code": 0,
  "start_time": "2020-09-18T15:51:35-04:00",
  "end_time": "2020-09-18T16:10:17-04:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/5b89472e-f9e8-11ea-9c31-005056bb42f7"
    }
  }
}
```
### Retrieving the MetroCluster DR Groups configured in the MetroCluster over IP configuration
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import MetroclusterDrGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(MetroclusterDrGroup.get_collection()))

```

<br/>
#### Response
```
HTTP/1.1 200 OK
Date: Fri, 18 Sep 2020 20:47:05 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Length: 849
Content-Type: application/hal+json
{
  "records": [
    {
      "id": 1,
      "_links": {
        "self": {
          "href": "/api/cluster/metrocluster/dr-groups/1"
        }
      }
    },
    {
      "id": 2,
      "_links": {
        "self": {
          "href": "/api/cluster/metrocluster/dr-groups/2"
        }
      }
    }
  ],
  "num_records": 2,
  "_links": {
    "self": {
      "href": "/api/cluster/metrocluster/dr-groups"
    }
  }
}
```
### Retrieving a Specific MetroCluster DR Group
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import MetroclusterDrGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = MetroclusterDrGroup(id=2)
    resource.get()
    print(resource)

```

<br/>
#### Response
```
HTTP/1.1 200 OK
Date: Fri, 18 Sep 2020 20:49:05 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Length: 1049
Content-Type: application/hal+json
{
  "id": 2,
  "partner_cluster": {
    "name": "mcc_siteB",
    "uuid": "ea4d7114-f97f-11ea-a4bf-005056bb070a"
  },
  "dr_pairs": [
    {
      "node": {
        "name": "node-e",
        "uuid": "28f71e17-f988-11ea-b1dd-005056bb47e8"
      },
      "partner": {
        "name": "node-g",
        "uuid": "1af02867-f989-11ea-b86c-005056bbe97f"
      }
    },
    {
      "node": {
        "name": "node-f",
        "uuid": "b34ae3b8-f988-11ea-866b-005056bb0934"
      },
      "partner": {
        "name": "node-h",
        "uuid": "a21a2b16-f989-11ea-98d0-005056bb321d"
      }
    }
  ],
  "_links": {
    "self": {
      "href": "/api/cluster/metrocluster/dr-groups/2"
    }
  }
}
```
### Deleting a MetroCluster DR Group
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import MetroclusterDrGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = MetroclusterDrGroup(id="{id}")
    resource.delete()

```

#### Response
```
HTTP/1.1 200 OK
Date: Tue, 22 Sep 2020 03:29:01 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Length: 189
Content-Type: application/hal+json
{
  "job": {
    "uuid": "c24d1083-fc83-11ea-acaf-005056bb47c1",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/c24d1083-fc83-11ea-acaf-005056bb47c1"
      }
    }
  }
}
```
### Monitoring the job progress
Use the link provided in the response to the DELETE request to fetch information for the delete job.
<br/>
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Job

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Job(uuid="c24d1083-fc83-11ea-acaf-005056bb47c1")
    resource.get()
    print(resource)

```

#### Job status response
The following is an example of the job status response returned by the MetroCluster DR Group delete job.
<br/>
```
HTTP/1.1 200 OK
Date: Tue, 22 Sep 2020 03:30:01 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Length: 374
Content-Type: application/hal+json
{
  "uuid": "c24d1083-fc83-11ea-acaf-005056bb47c1",
  "description": "DELETE /api/cluster/metrocluster/dr-groups/2",
  "state": "running",
  "message": "Unconfiguring Metrocluster DR Group",
  "code": 2432859,
  "start_time": "2020-09-21T23:29:01-04:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/c24d1083-fc83-11ea-acaf-005056bb47c1"
    }
  }
}
```
#### Final Status of a successful MetroCluster DR Group delete workflow
When the delete job completes, the 'end_time' field is populated, and the 'state' and 'message' fields report the final status.
<br/>
```
HTTP/1.1 200 OK
Date: Tue, 22 Sep 2020 03:38:08 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Length: 374
Content-Type: application/hal+json
{
  "uuid": "c24d1083-fc83-11ea-acaf-005056bb47c1",
  "description": "DELETE /api/cluster/metrocluster/dr-groups/2",
  "state": "success",
  "message": "success",
  "code": 0,
  "start_time": "2020-09-21T23:29:01-04:00",
  "end_time": "2020-09-21T23:36:36-04:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/c24d1083-fc83-11ea-acaf-005056bb47c1"
    }
  }
}
```"""

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


__all__ = ["MetroclusterDrGroup", "MetroclusterDrGroupSchema"]
__pdoc__ = {
    "MetroclusterDrGroupSchema.resource": False,
    "MetroclusterDrGroupSchema.opts": False,
}


class MetroclusterDrGroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MetroclusterDrGroup object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the metrocluster_dr_group."""

    dr_pairs = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.dr_pair.DrPairSchema", unknown=EXCLUDE, allow_none=True), data_key="dr_pairs", allow_none=True)
    r""" The dr_pairs field of the metrocluster_dr_group."""

    id = Size(
        data_key="id",
        allow_none=True,
    )
    r""" DR Group ID"""

    mccip_ports = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.metrocluster_mccip_ports.MetroclusterMccipPortsSchema", unknown=EXCLUDE, allow_none=True), data_key="mccip_ports", allow_none=True)
    r""" List of Port specifications."""

    partner_cluster = marshmallow_fields.Nested("netapp_ontap.resources.cluster.ClusterSchema", data_key="partner_cluster", unknown=EXCLUDE, allow_none=True)
    r""" The partner_cluster field of the metrocluster_dr_group."""

    @property
    def resource(self):
        return MetroclusterDrGroup

    gettable_fields = [
        "links",
        "dr_pairs",
        "id",
        "partner_cluster.links",
        "partner_cluster.name",
        "partner_cluster.uuid",
    ]
    """links,dr_pairs,id,partner_cluster.links,partner_cluster.name,partner_cluster.uuid,"""

    patchable_fields = [
        "dr_pairs",
        "partner_cluster.name",
        "partner_cluster.uuid",
    ]
    """dr_pairs,partner_cluster.name,partner_cluster.uuid,"""

    postable_fields = [
        "dr_pairs",
        "mccip_ports",
        "partner_cluster.name",
        "partner_cluster.uuid",
    ]
    """dr_pairs,mccip_ports,partner_cluster.name,partner_cluster.uuid,"""

class MetroclusterDrGroup(Resource):
    r""" DR group information. """

    _schema = MetroclusterDrGroupSchema
    _path = "/api/cluster/metrocluster/dr-groups"
    _keys = ["id"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves all the DR group in the MetroCluster over IP configuration.
### Related ONTAP commands
* `metrocluster configuration-settings dr-group show`

### Learn more
* [`DOC /cluster/metrocluster/dr-groups`](#docs-cluster-cluster_metrocluster_dr-groups)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all MetroclusterDrGroup resources that match the provided query"""
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
        """Returns a list of RawResources that represent MetroclusterDrGroup resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["MetroclusterDrGroup"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["MetroclusterDrGroup"], NetAppResponse]:
        r"""Creates a new DR group in the MetroCluster over IP configuration.
### Required properties
* `partner_cluster.name`
* `dr_pairs`
### Recommended optional properties
* `mccip_ports`
### Learn more
* [`DOC /cluster/metrocluster/dr-groups`](#docs-cluster-cluster_metrocluster_dr-groups)
### Related ONTAP commands
* `metrocluster configuration-settings dr-group create`
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
        records: Iterable["MetroclusterDrGroup"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Remove the DR group from the current MetroCluster over IP configuration specified by the DR group id.
### Related ONTAP commands
* `metrocluster configuration-settings dr-group delete`

### Learn more
* [`DOC /cluster/metrocluster/dr-groups`](#docs-cluster-cluster_metrocluster_dr-groups)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves all the DR group in the MetroCluster over IP configuration.
### Related ONTAP commands
* `metrocluster configuration-settings dr-group show`

### Learn more
* [`DOC /cluster/metrocluster/dr-groups`](#docs-cluster-cluster_metrocluster_dr-groups)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the DR group information specified by the DR group id.
### Related ONTAP commands
* `metrocluster configuration-settings dr-group show`

### Learn more
* [`DOC /cluster/metrocluster/dr-groups`](#docs-cluster-cluster_metrocluster_dr-groups)"""
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
        r"""Creates a new DR group in the MetroCluster over IP configuration.
### Required properties
* `partner_cluster.name`
* `dr_pairs`
### Recommended optional properties
* `mccip_ports`
### Learn more
* [`DOC /cluster/metrocluster/dr-groups`](#docs-cluster-cluster_metrocluster_dr-groups)
### Related ONTAP commands
* `metrocluster configuration-settings dr-group create`
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)


    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Remove the DR group from the current MetroCluster over IP configuration specified by the DR group id.
### Related ONTAP commands
* `metrocluster configuration-settings dr-group delete`

### Learn more
* [`DOC /cluster/metrocluster/dr-groups`](#docs-cluster-cluster_metrocluster_dr-groups)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


