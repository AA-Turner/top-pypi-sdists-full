r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

# Overview
You can use this API to migrate an SVM from a source cluster to a destination cluster. During the migration, you can pause, resume, or abort the operation, and retrieve the migration status and transfer status of volumes in the SVM.
The migrations APIs are only accessible from the destination cluster.
## Precondition
The cluster peering relationship should be created between the source and destination clusters prior to using this API.
## SVM migration APIs
The following APIs are used to manage SVM migration:
- POST /api/svm/migrations
- PATCH /api/svm/migrations/{uuid}
- GET /api/svm/migrations/
- GET /api/svm/migrations/{uuid}
- GET /api/svm/migrations/{svm_migration.uuid}/volumes
- GET /api/svm/migrations/{svm_migration.uuid}/volumes/{volume.uuid}
- DELETE /api/svm/migrations/{uuid}
## Important notes
The migration of temperature-sensitive storage efficiency (TSSE) volumes from AFF to FAS systems has a known limitation. The migration preserves the TSSE savings and after migration completes, the volume will not receive any further TSSE savings for the new data written on the volume.
## Starting a migration
To start a migration operation, issue a POST request to /svm/migrations. Parameters are provided in the body of the POST request to specify the source cluster and the source SVM.
## Monitoring the status of the SVM migration
You can use GET /svm/migrations to retrieve the status of the SVM migration and GET /svm/migrations/{svm_migration.uuid}/volumes to retrieve the transfer status of the volumes in the SVM migration.
### Possible errors before starting the migration
Configurations in the POST /svm/migrations request are validated before the SVM migration starts. If an invalid configuration is found or the migration pre-checks fail, an HTTP error code in the 4xx range is returned. No SVM migration operation is started.
### Polling the migration operation
After a successful POST /svm/migrations request is issued, an HTTP error code of 202 is returned along with a migration UUID and link in the body of the response. The SVM migration continues asynchronously and is monitored using the migration UUID and the GET /svm/migrations/{uuid} API.
### Errors during the migration operation
If a failure occurs during the SVM migration, the GET /svm/migrations response provides details of the error along with any error code fields.
### Pausing the migration operation
You can use PATCH /svm/migrations/{uuid} with the action "pause" to pause the SVM migration to update the SVM configuration on the source SVM.
### Resuming the migration operation
You can use PATCH /svm/migrations{uuid} with the action "resume" to resume the SVM migration from a paused state.
You can modify the throttle value when you resume the SVM migration. To set the throttle value to unlimited, specify the throttle value as 0.
### Aborting the migration operation
You can use DELETE /svm/migrations/{uuid} to delete the SVM on the destination cluster if the SVM migration has failed or is paused.
Use the DELETE /svm/migrations/{uuid} request to remove the SVM on the source cluster; this might be used when  communication between the source and destination cluster is reduced.
## Retrieving the migration status
You can use GET /svm/migrations/{uuid} to retrieve the current status of your migration.
## Retrieving the volume transfer status
You can use GET /svm/migrations/{svm_migration.uuid}/volumes to retrieve the current transfer status of all volumes in the migrating SVM.
## Retrieving the volume transfer status of a specific volume
You can use GET /svm/migrations/{svm_migrations.uuid}/volumes/{volume.uuid} to retrieve the transfer status of a specific volume in the migrating SVM.
<br/>
---
## Examples
### Starting a Migration
```
# API
/api/svm/migrations
```
### POST body included from file
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SvmMigration

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SvmMigration()
    resource.source = {"svm": {"name": "vs1"}, "cluster": {"name": "siteB"}}
    resource.post(hydrate=True)
    print(resource)

```

### Inline POST body
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SvmMigration

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SvmMigration()
    resource.source = {"svm": {"name": "vs1"}, "cluster": {"name": "siteB"}}
    resource.post(hydrate=True)
    print(resource)

```

### POST Response
```
Date: Wed, 25 Aug 2021 19:04:47 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Location: /api/svm/migrations/517c5e74-05d7-11ec-a40f-005056bba9a5
Content-Length: 189
Content-Type: application/hal+json
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
{
  "job": {
    "uuid": "5184a3e1-05d7-11ec-a40f-005056bba9a5",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/5184a3e1-05d7-11ec-a40f-005056bba9a5"
      }
    }
  }
}
```
### Retrieving POST Job status
Use the link provided in the response to the POST request to fetch the status of the start operation
<br/>
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Job

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Job(uuid="5184a3e1-05d7-11ec-a40f-005056bba9a5")
    resource.get()
    print(resource)

```

<br/>
#### Response
```
Date: Wed, 25 Aug 2021 19:05:04 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Type: application/hal+json
Vary: Accept-Encoding
Content-Encoding: gzip
Content-Length: 224
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
{
  "uuid": "5184a3e1-05d7-11ec-a40f-005056bba9a5",
  "description": "POST /api/svm/migrations/517c5e74-05d7-11ec-a40f-005056bba9a5",
  "state": "success",
  "message": "success",
  "code": 0,
  "start_time": "2021-08-25T15:04:48-04:00",
  "end_time": "2021-08-25T15:04:57-04:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/5184a3e1-05d7-11ec-a40f-005056bba9a5"
    }
  }
}
```
### Retrieving all migrations
The location header in the POST operation provides the uuid of the migrate operation that was started using POST. Also, you can list all the migrate operations using the collection GET.
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SvmMigration

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(SvmMigration.get_collection()))

```

<br/>
#### Response
```
Date: Wed, 25 Aug 2021 19:05:11 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Type: application/hal+json
Vary: Accept-Encoding
Content-Encoding: gzip
Content-Length: 170
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
{
  "records": [
    {
      "uuid": "517c5e74-05d7-11ec-a40f-005056bba9a5",
      "_links": {
        "self": {
          "href": "/api/svm/migrations/517c5e74-05d7-11ec-a40f-005056bba9a5"
        }
      }
    }
  ],
  "num_records": 1,
  "_links": {
    "self": {
      "href": "/api/svm/migrations/"
    }
  }
}
```
### Retrieving a specific migration
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SvmMigration

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SvmMigration(uuid="517c5e74-05d7-11ec-a40f-005056bba9a5")
    resource.get()
    print(resource)

```

<br/>
#### Response
```
Date: Wed, 25 Aug 2021 19:05:33 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Type: application/hal+json
Vary: Accept-Encoding
Content-Encoding: gzip
Content-Length: 379
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
{
  "uuid": "517c5e74-05d7-11ec-a40f-005056bba9a5",
  "state": "setup_configuration",
  "start_time": "2021-08-25T15:04:49-04:00",
  "current_operation": "start",
  "source": {
    "svm": {
      "uuid": "424b6002-fb1a-11eb-9383-005056bbcf32",
      "name": "vs1",
      "_links": {
        "self": {
          "href": "/api/svm/svms/424b6002-fb1a-11eb-9383-005056bbcf32"
        }
      }
    },
    "cluster": {
      "uuid": "b54babec-fb14-11eb-9383-005056bbcf32",
      "name": "siteB",
      "_links": {
        "self": {
          "href": "/api/cluster/peers/b54babec-fb14-11eb-9383-005056bbcf32"
        }
      }
    }
  },
  "destination": {
    "ipspace": {
      "uuid": "f305cf0b-fb14-11eb-829d-005056bba9a5",
      "name": "Default"
    }
  },
  "auto_cutover": false,
  "auto_source_cleanup": false,
  "throttle": 0,
  "_links": {
    "self": {
      "href": "/api/svm/migrations/517c5e74-05d7-11ec-a40f-005056bba9a5"
    }
  }
}
```
### Pausing a migration
To pause the migration use the PATCH request on the migration UUID.
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SvmMigration

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SvmMigration(uuid="517c5e74-05d7-11ec-a40f-005056bba9a5")
    resource.patch(hydrate=True, action="pause")

```

#### Response
```
Date: Wed, 25 Aug 2021 19:06:11 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Length: 189
Content-Type: application/hal+json
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
{
  "job": {
    "uuid": "82dea7c7-05d7-11ec-a40f-005056bba9a5",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/82dea7c7-05d7-11ec-a40f-005056bba9a5"
      }
    }
  }
}
```
### Monitoring PATCH job status
Use the link provided in the response of the PATCH request to fetch the information of the patch job.
<br/>
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Job

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Job(uuid="82dea7c7-05d7-11ec-a40f-005056bba9a5")
    resource.get()
    print(resource)

```

#### Response
```
Date: Wed, 25 Aug 2021 21:40:06 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Type: application/hal+json
Vary: Accept-Encoding
Content-Encoding: gzip
Content-Length: 222
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
{
  "uuid": "82dea7c7-05d7-11ec-a40f-005056bba9a5",
  "description": "PATCH /api/svm/migrations/517c5e74-05d7-11ec-a40f-005056bba9a5",
  "state": "success",
  "message": "success",
  "code": 0,
  "start_time": "2021-08-25T15:06:11-04:00",
  "end_time": "2021-08-25T15:06:11-04:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/82dea7c7-05d7-11ec-a40f-005056bba9a5"
    }
  }
}
```
### Aborting a migration
To abort the migration use the DELETE request on the migration UUID.
<br/>
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SvmMigration

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SvmMigration(uuid="517c5e74-05d7-11ec-a40f-005056bba9a5")
    resource.delete()

```

#### Response
```
Date: Wed, 25 Aug 2021 22:57:23 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Length: 189
Content-Type: application/hal+json
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
{
  "job": {
    "uuid": "cf870f19-05f7-11ec-a40f-005056bba9a5",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/cf870f19-05f7-11ec-a40f-005056bba9a5"
      }
    }
  }
}
```
### Monitoring DELETE job status
Use the link provided in the response of the PATCH request to fetch the information of the patch job.
<br/>
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Job

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Job(uuid="cf870f19-05f7-11ec-a40f-005056bba9a5")
    resource.get()
    print(resource)

```

#### Response
```
Date: Wed, 25 Aug 2021 23:05:47 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Type: application/hal+json
Vary: Accept-Encoding
Content-Encoding: gzip
Content-Length: 228
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
{
  "uuid": "cf870f19-05f7-11ec-a40f-005056bba9a5",
  "description": "DELETE /api/svm/migrations/517c5e74-05d7-11ec-a40f-005056bba9a5",
  "state": "success",
  "message": "success",
  "code": 0,
  "start_time": "2021-08-25T18:57:23-04:00",
  "end_time": "2021-08-25T18:57:24-04:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/cf870f19-05f7-11ec-a40f-005056bba9a5"
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


__all__ = ["SvmMigration", "SvmMigrationSchema"]
__pdoc__ = {
    "SvmMigrationSchema.resource": False,
    "SvmMigrationSchema.opts": False,
}


class SvmMigrationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmMigration object"""

    auto_cutover = marshmallow_fields.Boolean(
        data_key="auto_cutover",
        allow_none=True,
    )
    r""" Optional property that when set to true automatically performs cutover when the migration state reaches "ready for cutover"."""

    auto_source_cleanup = marshmallow_fields.Boolean(
        data_key="auto_source_cleanup",
        allow_none=True,
    )
    r""" Optional property that when set to true automatically cleans up the SVM on the source cluster after the migration cutover."""

    check_only = marshmallow_fields.Boolean(
        data_key="check_only",
        allow_none=True,
    )
    r""" Optional property that when set to true performs only migration pre-checks not the actual migration."""

    current_operation = marshmallow_fields.Str(
        data_key="current_operation",
        allow_none=True,
    )
    r""" The current_operation field of the svm_migration."""

    destination = marshmallow_fields.Nested("netapp_ontap.models.svm_migration_destination.SvmMigrationDestinationSchema", data_key="destination", unknown=EXCLUDE, allow_none=True)
    r""" Destination cluster details for the SVM migration."""

    ip_interface_placement = marshmallow_fields.Nested("netapp_ontap.models.svm_migration_ip_interface_placement.SvmMigrationIpInterfacePlacementSchema", data_key="ip_interface_placement", unknown=EXCLUDE, allow_none=True)
    r""" Optional property used to specify the IP interface placement in the destination. It is input only and is not returned by a subsequent GET."""

    last_failed_state = marshmallow_fields.Str(
        data_key="last_failed_state",
        allow_none=True,
    )
    r""" The last_failed_state field of the svm_migration."""

    last_operation = marshmallow_fields.Str(
        data_key="last_operation",
        validate=enum_validation(['none', 'start', 'resume', 'pause', 'cleanup', 'cutover']),
        allow_none=True,
    )
    r""" The last_operation field of the svm_migration.

Valid choices:

* none
* start
* resume
* pause
* cleanup
* cutover"""

    messages = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.ems_ui_message_arguments.EmsUiMessageArgumentsSchema", unknown=EXCLUDE, allow_none=True), data_key="messages", allow_none=True)
    r""" Errors and warnings returned/displayed during migration."""

    point_of_no_return = marshmallow_fields.Boolean(
        data_key="point_of_no_return",
        allow_none=True,
    )
    r""" Indicates if the migration has progressed beyond the point of no return. When true, the migration cannot be aborted or paused. When false, the migration can be paused or aborted."""

    restart_count = Size(
        data_key="restart_count",
        allow_none=True,
    )
    r""" Number of times migrate restarted the transfer, for example, rollback to transfer after starting the cutover."""

    source = marshmallow_fields.Nested("netapp_ontap.models.svm_migration_source.SvmMigrationSourceSchema", data_key="source", unknown=EXCLUDE, allow_none=True)
    r""" Source cluster details for the SVM migration."""

    state = marshmallow_fields.Str(
        data_key="state",
        allow_none=True,
    )
    r""" The state field of the svm_migration."""

    throttle = Size(
        data_key="throttle",
        allow_none=True,
    )
    r""" Optional property to specify a throttle value in KB/s for each individual volume transfer. Defaults to 0 if not set, which is interpreted as unlimited. The minimum throttle value is 4 KB/s, so if you specify a throttle value between 1 and 4, it will be treated as if you specified 4."""

    time_metrics = marshmallow_fields.Nested("netapp_ontap.models.svm_migration_time_metrics.SvmMigrationTimeMetricsSchema", data_key="time_metrics", unknown=EXCLUDE, allow_none=True)
    r""" Various time metrics details"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" SVM migration UUID

Example: 4ea7a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return SvmMigration

    gettable_fields = [
        "auto_cutover",
        "auto_source_cleanup",
        "current_operation",
        "destination",
        "ip_interface_placement",
        "last_failed_state",
        "last_operation",
        "messages",
        "point_of_no_return",
        "restart_count",
        "source",
        "state",
        "throttle",
        "time_metrics",
        "uuid",
    ]
    """auto_cutover,auto_source_cleanup,current_operation,destination,ip_interface_placement,last_failed_state,last_operation,messages,point_of_no_return,restart_count,source,state,throttle,time_metrics,uuid,"""

    patchable_fields = [
        "destination",
        "ip_interface_placement",
        "source",
        "throttle",
    ]
    """destination,ip_interface_placement,source,throttle,"""

    postable_fields = [
        "auto_cutover",
        "auto_source_cleanup",
        "check_only",
        "destination",
        "ip_interface_placement",
        "source",
        "throttle",
    ]
    """auto_cutover,auto_source_cleanup,check_only,destination,ip_interface_placement,source,throttle,"""

class SvmMigration(Resource):
    r""" Provides information on SVM migration, default and user specified configurations, the state of the migration, and volume transfer metrics. """

    _schema = SvmMigrationSchema
    _path = "/api/svm/migrations"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the SVM migration status.
### Related ONTAP commands
* `vserver migrate show`

### Learn more
* [`DOC /svm/migrations`](#docs-svm-svm_migrations)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SvmMigration resources that match the provided query"""
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
        """Returns a list of RawResources that represent SvmMigration resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["SvmMigration"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Actions that can be performed during an SVM migration.
### Related ONTAP commands
* `vserver migrate pause`
* `vserver migrate resume`
* `vserver migrate cutover`
* `vserver migrate source-cleanup`

### Learn more
* [`DOC /svm/migrations`](#docs-svm-svm_migrations)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["SvmMigration"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SvmMigration"], NetAppResponse]:
        r"""Creates an SVM migration operation. This API must be executed on the destination cluster. This API creates an SVM on the destination cluster and preserves the SVM's identity specified in the source cluster.
Optionally, you can specify the aggregate list for creating the volumes, and IPspace. You can perform pre-checks to verify if SVM migration is possible, by setting the "check-only" option to "true". By default the values for auto-source-cleanup and auto-cutover is true.
### Required properties
* `source.svm.name` or `source.svm.uuid` - Source SVM name or source SVM UUID.
* `source.cluster.name` or `source.cluster.uuid` - Source cluster name or source cluster UUID
### Optional properties
* `destination.ipspace.name` or `destination.ipspace.uuid` - Destination IP Space name or UUID where the vserver will be migrated to.
* `destination.volume_placement.aggregates` - List of aggregates where the migrating volumes should go on the destination.
* `destination.volume_placement.volume_aggregate_pairs` - List of volume aggregate pairs indicating where the migrating volumes should go on the destination.
* `ip_interface_placement` -  List of source SVM's IP interface and port pairs on the destination for migrating the SVM's IP interfaces.
* `auto_cutover` - Option to specify whether to perform cutover automatically. Default is true.
* `auto_source_cleanup` - Option to specify whether to perform source cleanup automatically. Default is true.
* `check_only` - Option to perform all the prechecks for migrate without actually starting the migrate. Default is false.
* `throttle` - Option to specify a throttle value in KB/s. Defaults to unlimited.
### Related ONTAP commands
* `vserver migrate start`

### Learn more
* [`DOC /svm/migrations`](#docs-svm-svm_migrations)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["SvmMigration"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the SVM migration.
### Related ONTAP commands
* `vserver migrate abort`

### Learn more
* [`DOC /svm/migrations`](#docs-svm-svm_migrations)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the SVM migration status.
### Related ONTAP commands
* `vserver migrate show`

### Learn more
* [`DOC /svm/migrations`](#docs-svm-svm_migrations)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the migration status of an individual SVM.
### Important notes
* The "migrations" object includes a large set of fields and can be expensive to retrieve.
* REST APIs only expose a data SVM as an SVM.
* There are subsystem specific errors that can be returned from this endpoint. If a subsystem specific error is returned and this is the first migrate operation attempt, it is embedded in one of the following errors. If a subsystem specific error is returned and this is not the first migrate operation attempt, the subsystem specific error is returned directly.
### Example
    Retrieving an individual SVM migration status.
    <br/>
    ```
    GET "/api/svm/migrations/a14ae39f-8d85-11e9-b4a7-00505682dc8b/svms/f16f0935-5281-11e8-b94d-005056b46485"
    ```
    <br/>

### Learn more
* [`DOC /svm/migrations`](#docs-svm-svm_migrations)"""
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
        r"""Creates an SVM migration operation. This API must be executed on the destination cluster. This API creates an SVM on the destination cluster and preserves the SVM's identity specified in the source cluster.
Optionally, you can specify the aggregate list for creating the volumes, and IPspace. You can perform pre-checks to verify if SVM migration is possible, by setting the "check-only" option to "true". By default the values for auto-source-cleanup and auto-cutover is true.
### Required properties
* `source.svm.name` or `source.svm.uuid` - Source SVM name or source SVM UUID.
* `source.cluster.name` or `source.cluster.uuid` - Source cluster name or source cluster UUID
### Optional properties
* `destination.ipspace.name` or `destination.ipspace.uuid` - Destination IP Space name or UUID where the vserver will be migrated to.
* `destination.volume_placement.aggregates` - List of aggregates where the migrating volumes should go on the destination.
* `destination.volume_placement.volume_aggregate_pairs` - List of volume aggregate pairs indicating where the migrating volumes should go on the destination.
* `ip_interface_placement` -  List of source SVM's IP interface and port pairs on the destination for migrating the SVM's IP interfaces.
* `auto_cutover` - Option to specify whether to perform cutover automatically. Default is true.
* `auto_source_cleanup` - Option to specify whether to perform source cleanup automatically. Default is true.
* `check_only` - Option to perform all the prechecks for migrate without actually starting the migrate. Default is false.
* `throttle` - Option to specify a throttle value in KB/s. Defaults to unlimited.
### Related ONTAP commands
* `vserver migrate start`

### Learn more
* [`DOC /svm/migrations`](#docs-svm-svm_migrations)"""
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
        r"""Actions that can be performed during an SVM migration.
### Related ONTAP commands
* `vserver migrate pause`
* `vserver migrate resume`
* `vserver migrate cutover`
* `vserver migrate source-cleanup`

### Learn more
* [`DOC /svm/migrations`](#docs-svm-svm_migrations)"""
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
        r"""Deletes the SVM migration.
### Related ONTAP commands
* `vserver migrate abort`

### Learn more
* [`DOC /svm/migrations`](#docs-svm-svm_migrations)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


