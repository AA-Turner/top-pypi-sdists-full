r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Manages a specific instance of a destination. There are limits to the information that you can modify after a destination is created. For example, you cannot change a destination's type, but you can modify the underlying details of the type.
####
Note: The system defines default destinations that cannot be removed or modified. These destinations are specified by setting the "system_defined" field to "true".
####
See the documentation for [/support/ems/destinations](#/docs/support/support_ems_destinations) for details on the various properties in a destination.
## Connectivity Test
Optionally, you can request the connectivity object by specifically requesting the object in the fields query. This will perform an additional test to determine the state of the destination. The state response can include one of the following values:
- success
- fail
- not_supported
### success
If the connectivity object indicates a state of 'success', then the destination check passed.
####
Note: Currently, only the 'rest_api' destination type is supported. A successful result indicates that the server received the event.
### fail
If the connectivity object indicates a state of 'fail', then the destination check has not passed. The object will contain a 'error' object with additional information regarding the failure.
### not_supported
If the connectivity object indicates a state of 'not_supported', then the destination check is not available for the indicated destination type. This is not considered a failure condition.
####
Note: Currently, only the 'rest_api' destination type is supported for connectivity testing.
## Examples
### Retrieving a specific destination instance
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import EmsDestination

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = EmsDestination(name="snmp-traphost")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
EmsDestination(
    {
        "destination": "",
        "filters": [
            {
                "name": "default-trap-events",
                "_links": {
                    "self": {"href": "/api/support/ems/filters/default-trap-events"}
                },
            }
        ],
        "name": "snmp-traphost",
        "_links": {"self": {"href": "/api/support/ems/destinations/snmp-traphost"}},
        "type": "snmp",
    }
)

```
</div>
</div>

### Check whether a destination passes connectivity tests
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import EmsDestination

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = EmsDestination(name="rest-api-destination")
    resource.get(fields="name,connectivity.*")
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
EmsDestination(
    {
        "name": "rest-api-destination",
        "connectivity": {
            "errors": [
                {
                    "message": {
                        "message": "Cannot reach host mail@mail.com.",
                        "arguments": [{"message": "mail@mail.com", "code": "5"}],
                        "code": "4",
                    },
                    "node": {
                        "name": "node1",
                        "uuid": "1cd8a442-86d1-11e0-ae1c-123478563412",
                    },
                }
            ],
            "state": "fail",
        },
        "_links": {
            "self": {
                "href": "/api/support/ems/destinations/rest-api-destination?fields=name,connectivity.*"
            }
        },
    }
)

```
</div>
</div>

### Updating an existing destination (change of email address)
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import EmsDestination

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = EmsDestination()
    resource.destination = "support@mycompany.com"
    resource.post(hydrate=True)
    print(resource)

```

### Deleting an existing destination
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import EmsDestination

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = EmsDestination(name="test-destination")
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


__all__ = ["EmsDestination", "EmsDestinationSchema"]
__pdoc__ = {
    "EmsDestinationSchema.resource": False,
    "EmsDestinationSchema.opts": False,
}


class EmsDestinationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsDestination object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the ems_destination."""

    access_control_role = marshmallow_fields.Nested("netapp_ontap.resources.role.RoleSchema", data_key="access_control_role", unknown=EXCLUDE, allow_none=True)
    r""" The access_control_role field of the ems_destination."""

    certificate = marshmallow_fields.Nested("netapp_ontap.models.ems_certificate.EmsCertificateSchema", data_key="certificate", unknown=EXCLUDE, allow_none=True)
    r""" Specifies the client-side certificate used by the ONTAP system when mutual authentication is required. This object is only applicable for __rest_api__ type destinations. Both the `ca` and `serial_number` fields must be specified when configuring a certificate in a PATCH or POST request. The `name` field is read-only and cannot be used to configure a client-side certificate."""

    connectivity = marshmallow_fields.Nested("netapp_ontap.models.ems_destination_connectivity.EmsDestinationConnectivitySchema", data_key="connectivity", unknown=EXCLUDE, allow_none=True)
    r""" The connectivity field of the ems_destination."""

    destination = marshmallow_fields.Str(
        data_key="destination",
        allow_none=True,
    )
    r""" Event destination

Example: administrator@mycompany.com"""

    filters = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.ems_filter.EmsFilterSchema", unknown=EXCLUDE, allow_none=True), data_key="filters", allow_none=True)
    r""" The filters field of the ems_destination."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Destination name.  Valid in POST.

Example: Admin_Email"""

    syslog = marshmallow_fields.Nested("netapp_ontap.models.ems_syslog.EmsSyslogSchema", data_key="syslog", unknown=EXCLUDE, allow_none=True)
    r""" The syslog field of the ems_destination."""

    system_defined = marshmallow_fields.Boolean(
        data_key="system_defined",
        allow_none=True,
    )
    r""" Flag indicating system-defined destinations.

Example: true"""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['snmp', 'email', 'syslog', 'rest_api']),
        allow_none=True,
    )
    r""" Type of destination. Valid in POST.

Valid choices:

* snmp
* email
* syslog
* rest_api"""

    @property
    def resource(self):
        return EmsDestination

    gettable_fields = [
        "links",
        "access_control_role.links",
        "access_control_role.name",
        "certificate",
        "connectivity",
        "destination",
        "filters.links",
        "filters.name",
        "name",
        "syslog",
        "system_defined",
        "type",
    ]
    """links,access_control_role.links,access_control_role.name,certificate,connectivity,destination,filters.links,filters.name,name,syslog,system_defined,type,"""

    patchable_fields = [
        "certificate",
        "connectivity",
        "destination",
        "filters.name",
        "syslog",
    ]
    """certificate,connectivity,destination,filters.name,syslog,"""

    postable_fields = [
        "certificate",
        "connectivity",
        "destination",
        "filters.name",
        "name",
        "syslog",
        "type",
    ]
    """certificate,connectivity,destination,filters.name,name,syslog,type,"""

class EmsDestination(Resource):
    """Allows interaction with EmsDestination objects on the host"""

    _schema = EmsDestinationSchema
    _path = "/api/support/ems/destinations"
    _keys = ["name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of event destinations.
### Related ONTAP commands
* `event notification destination show`
* `event notification show`

### Learn more
* [`DOC /support/ems/destinations`](#docs-support-support_ems_destinations)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all EmsDestination resources that match the provided query"""
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
        """Returns a list of RawResources that represent EmsDestination resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["EmsDestination"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates an event destination.
### Recommended optional properties
* `filters.name` - New list of filters that should direct to this destination. The existing list is discarded.
* `certificate` - New certificate parameters when the destination type is `rest api`.
### Related ONTAP commands
* `event notification destination modify`
* `event notification modify`

### Learn more
* [`DOC /support/ems/destinations/{name}`](#docs-support-support_ems_destinations_{name})"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["EmsDestination"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["EmsDestination"], NetAppResponse]:
        r"""Creates an event destination.
### Required properties
* `name` - String that uniquely identifies the destination.
* `type` - Type of destination that is to be created.
* `destination` - String that identifies the destination. The contents of this property changes depending on type.
### Recommended optional properties
* `filters.name` - List of filter names that should direct to this destination.
* `certificate` - When specifying a rest api destination, a client certificate can be provided.
* `syslog` - When specifying a syslog destination, a port, transport protocol, message format, timestamp format and hostname format can be provided.
### Related ONTAP commands
* `event notification destination create`
* `event notification create`

### Learn more
* [`DOC /support/ems/destinations`](#docs-support-support_ems_destinations)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["EmsDestination"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an event destination.
### Related ONTAP commands
* `event notification destination delete`
* `event notification delete`

### Learn more
* [`DOC /support/ems/destinations/{name}`](#docs-support-support_ems_destinations_{name})"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of event destinations.
### Related ONTAP commands
* `event notification destination show`
* `event notification show`

### Learn more
* [`DOC /support/ems/destinations`](#docs-support-support_ems_destinations)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves event destinations.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter.
* `connectivity.*`
### Related ONTAP commands
* `event notification destination show`
* `event notification show`

### Learn more
* [`DOC /support/ems/destinations/{name}`](#docs-support-support_ems_destinations_{name})"""
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
        r"""Creates an event destination.
### Required properties
* `name` - String that uniquely identifies the destination.
* `type` - Type of destination that is to be created.
* `destination` - String that identifies the destination. The contents of this property changes depending on type.
### Recommended optional properties
* `filters.name` - List of filter names that should direct to this destination.
* `certificate` - When specifying a rest api destination, a client certificate can be provided.
* `syslog` - When specifying a syslog destination, a port, transport protocol, message format, timestamp format and hostname format can be provided.
### Related ONTAP commands
* `event notification destination create`
* `event notification create`

### Learn more
* [`DOC /support/ems/destinations`](#docs-support-support_ems_destinations)"""
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
        r"""Updates an event destination.
### Recommended optional properties
* `filters.name` - New list of filters that should direct to this destination. The existing list is discarded.
* `certificate` - New certificate parameters when the destination type is `rest api`.
### Related ONTAP commands
* `event notification destination modify`
* `event notification modify`

### Learn more
* [`DOC /support/ems/destinations/{name}`](#docs-support-support_ems_destinations_{name})"""
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
        r"""Deletes an event destination.
### Related ONTAP commands
* `event notification destination delete`
* `event notification delete`

### Learn more
* [`DOC /support/ems/destinations/{name}`](#docs-support-support_ems_destinations_{name})"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


