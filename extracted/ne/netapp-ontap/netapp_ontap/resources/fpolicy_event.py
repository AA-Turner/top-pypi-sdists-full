r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
FPolicy events configurations allow you to specify which file access is monitored. As part of an FPolicy event, you can configure the SVM for which the events are generated, the name of the event configuration, the protocol (cifs, nfsv3/nfsv4) for which the events are generated, the file operations which are monitored, and filters that can be used to filter the unwanted notification generation for a specified protocol and file operation.</br>
Each protocol has a set of supported file operations and filters. An SVM can have multiple events. A single FPolicy policy can have multiple FPolicy events.</br>
FPolicy events can also be configured to monitor file operations which fail due to lack of permissions. You can specify which file operation to monitor for failure. However, filters can not be used to filter failed file operations.
## Examples
### Creating an FPolicy event for a CIFS protocol with all the supported file operations and filters
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyEvent

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyEvent("4f643fb4-fd21-11e8-ae49-0050568e2c1e")
    resource.file_operations = {
        "close": True,
        "create": True,
        "create_dir": True,
        "delete": True,
        "delete_dir": True,
        "getattr": True,
        "open": True,
        "read": True,
        "rename": True,
        "rename_dir": True,
        "setattr": True,
        "write": True,
    }
    resource.filters = {
        "close_with_modification": True,
        "close_with_read": True,
        "close_without_modification": True,
        "first_read": True,
        "first_write": True,
        "monitor_ads": True,
        "offline_bit": True,
        "open_with_delete_intent": True,
        "open_with_write_intent": True,
        "write_with_size_change": True,
    }
    resource.name = "event_cifs"
    resource.protocol = "cifs"
    resource.volume_monitoring = True
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
FpolicyEvent(
    {
        "file_operations": {
            "rename_dir": True,
            "read": True,
            "delete": True,
            "getattr": True,
            "open": True,
            "create": True,
            "delete_dir": True,
            "rename": True,
            "setattr": True,
            "write": True,
            "close": True,
            "create_dir": True,
        },
        "volume_monitoring": True,
        "filters": {
            "monitor_ads": True,
            "offline_bit": True,
            "first_read": True,
            "open_with_write_intent": True,
            "close_without_modification": True,
            "close_with_modification": True,
            "close_with_read": True,
            "open_with_delete_intent": True,
            "write_with_size_change": True,
            "first_write": True,
        },
        "protocol": "cifs",
        "name": "event_cifs",
        "monitor_fileop_failure": False,
    }
)

```
</div>
</div>

---
### Creating an FPolicy event for an NFS protocol with all the supported file operations and filters
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyEvent

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyEvent("4f643fb4-fd21-11e8-ae49-0050568e2c1e")
    resource.file_operations = {
        "create": True,
        "create_dir": True,
        "delete": True,
        "delete_dir": True,
        "link": True,
        "lookup": True,
        "read": True,
        "rename": True,
        "rename_dir": True,
        "setattr": True,
        "symlink": True,
        "write": True,
    }
    resource.filters = {"offline_bit": True, "write_with_size_change": True}
    resource.name = "event_nfsv3"
    resource.protocol = "nfsv3"
    resource.volume_monitoring = False
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
FpolicyEvent(
    {
        "file_operations": {
            "rename_dir": True,
            "read": True,
            "delete": True,
            "link": True,
            "lookup": True,
            "create": True,
            "delete_dir": True,
            "rename": True,
            "setattr": True,
            "symlink": True,
            "write": True,
            "create_dir": True,
        },
        "volume_monitoring": False,
        "filters": {"offline_bit": True, "write_with_size_change": True},
        "protocol": "nfsv3",
        "name": "event_nfsv3",
        "monitor_fileop_failure": False,
    }
)

```
</div>
</div>

---
### Creating an FPolicy event to monitor failed file operations for an NFS protocol with all the supported file operations
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyEvent

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyEvent("b5087518-40b3-11ed-b3eb-005056bbe901")
    resource.file_operations = {
        "create": True,
        "create_dir": True,
        "delete": True,
        "delete_dir": True,
        "link": True,
        "read": True,
        "rename": True,
        "rename_dir": True,
        "write": True,
    }
    resource.name = "nfs_failed_op"
    resource.protocol = "nfsv3"
    resource.monitor_fileop_failure = True
    resource.volume_monitoring = False
    resource.post(hydrate=True, return_records=False)
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
FpolicyEvent(
    {
        "file_operations": {
            "rename_dir": True,
            "read": True,
            "delete": True,
            "link": True,
            "create": True,
            "delete_dir": True,
            "rename": True,
            "write": True,
            "create_dir": True,
        },
        "volume_monitoring": False,
        "protocol": "nfsv3",
        "name": "nfs_failed_op",
        "monitor_fileop_failure": True,
    }
)

```
</div>
</div>

---
### Retrieving all of the FPolicy event configurations configured to monitor failed file operations for a specified SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyEvent

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            FpolicyEvent.get_collection(
                "b5087518-40b3-11ed-b3eb-005056bbe901",
                monitor_fileop_failure=True,
                fields="*",
                return_timeout=15,
            )
        )
    )

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
[
    FpolicyEvent(
        {
            "file_operations": {
                "rename_dir": False,
                "read": False,
                "delete": False,
                "link": False,
                "getattr": False,
                "lookup": False,
                "open": True,
                "create": False,
                "delete_dir": False,
                "rename": False,
                "setattr": False,
                "symlink": False,
                "write": False,
                "close": False,
                "create_dir": False,
            },
            "volume_monitoring": False,
            "protocol": "cifs",
            "name": "fo_event",
            "svm": {"uuid": "b5087518-40b3-11ed-b3eb-005056bbe901"},
            "monitor_fileop_failure": True,
        }
    )
]

```
</div>
</div>

---
### Retrieving all of the FPolicy event configurations for a specified SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyEvent

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            FpolicyEvent.get_collection(
                "4f643fb4-fd21-11e8-ae49-0050568e2c1e", fields="*", return_timeout=15
            )
        )
    )

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
[
    FpolicyEvent(
        {
            "file_operations": {
                "rename_dir": False,
                "read": False,
                "delete": False,
                "link": False,
                "getattr": False,
                "lookup": False,
                "open": False,
                "create": False,
                "delete_dir": False,
                "rename": False,
                "setattr": False,
                "symlink": False,
                "write": False,
                "close": True,
                "create_dir": False,
            },
            "volume_monitoring": False,
            "filters": {
                "monitor_ads": False,
                "offline_bit": False,
                "first_read": False,
                "open_with_write_intent": False,
                "setattr_with_dacl_change": False,
                "close_without_modification": False,
                "setattr_with_mode_change": False,
                "setattr_with_allocation_size_change": False,
                "close_with_modification": False,
                "close_with_read": True,
                "open_with_delete_intent": False,
                "setattr_with_size_change": False,
                "write_with_size_change": False,
                "first_write": False,
                "setattr_with_owner_change": False,
                "setattr_with_access_time_change": False,
                "setattr_with_creation_time_change": False,
                "exclude_directory": False,
                "setattr_with_group_change": False,
                "setattr_with_sacl_change": False,
                "setattr_with_modify_time_change": False,
            },
            "protocol": "cifs",
            "name": "cluster",
            "svm": {"uuid": "4f643fb4-fd21-11e8-ae49-0050568e2c1e"},
            "monitor_fileop_failure": False,
        }
    ),
    FpolicyEvent(
        {
            "file_operations": {
                "rename_dir": True,
                "read": True,
                "delete": True,
                "link": False,
                "getattr": True,
                "lookup": False,
                "open": True,
                "create": True,
                "delete_dir": True,
                "rename": True,
                "setattr": True,
                "symlink": False,
                "write": True,
                "close": True,
                "create_dir": True,
            },
            "volume_monitoring": True,
            "filters": {
                "monitor_ads": True,
                "offline_bit": True,
                "first_read": True,
                "open_with_write_intent": True,
                "setattr_with_dacl_change": False,
                "close_without_modification": True,
                "setattr_with_mode_change": False,
                "setattr_with_allocation_size_change": False,
                "close_with_modification": True,
                "close_with_read": True,
                "open_with_delete_intent": True,
                "setattr_with_size_change": False,
                "write_with_size_change": True,
                "first_write": True,
                "setattr_with_owner_change": False,
                "setattr_with_access_time_change": False,
                "setattr_with_creation_time_change": False,
                "exclude_directory": False,
                "setattr_with_group_change": False,
                "setattr_with_sacl_change": False,
                "setattr_with_modify_time_change": False,
            },
            "protocol": "cifs",
            "name": "event_cifs",
            "svm": {"uuid": "4f643fb4-fd21-11e8-ae49-0050568e2c1e"},
            "monitor_fileop_failure": False,
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific FPolicy event configuration for an SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyEvent

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyEvent("4f643fb4-fd21-11e8-ae49-0050568e2c1e", name="event_cifs")
    resource.get(fields="*", return_timeout=15)
    print(resource)

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
FpolicyEvent(
    {
        "file_operations": {
            "rename_dir": True,
            "read": True,
            "delete": True,
            "link": False,
            "getattr": True,
            "lookup": False,
            "open": True,
            "create": True,
            "delete_dir": True,
            "rename": True,
            "setattr": True,
            "symlink": False,
            "write": True,
            "close": True,
            "create_dir": True,
        },
        "volume_monitoring": True,
        "filters": {
            "monitor_ads": True,
            "offline_bit": True,
            "first_read": True,
            "open_with_write_intent": True,
            "setattr_with_dacl_change": False,
            "close_without_modification": True,
            "setattr_with_mode_change": False,
            "setattr_with_allocation_size_change": False,
            "close_with_modification": True,
            "close_with_read": True,
            "open_with_delete_intent": True,
            "setattr_with_size_change": False,
            "write_with_size_change": True,
            "first_write": True,
            "setattr_with_owner_change": False,
            "setattr_with_access_time_change": False,
            "setattr_with_creation_time_change": False,
            "exclude_directory": False,
            "setattr_with_group_change": False,
            "setattr_with_sacl_change": False,
            "setattr_with_modify_time_change": False,
        },
        "protocol": "cifs",
        "name": "event_cifs",
        "svm": {"uuid": "4f643fb4-fd21-11e8-ae49-0050568e2c1e"},
        "monitor_fileop_failure": False,
    }
)

```
</div>
</div>

---
### Updating a specific FPolicy event configuration for a specified SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyEvent

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyEvent("4f643fb4-fd21-11e8-ae49-0050568e2c1e", name="event_cifs")
    resource.file_operations = {"close": False, "create": False, "read": True}
    resource.filters = {
        "close_with_modification": False,
        "close_with_read": False,
        "close_without_modification": False,
    }
    resource.protocol = "cifs"
    resource.volume_monitoring = False
    resource.patch()

```

---
### Deleting a specific FPolicy event configuration for a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyEvent

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyEvent("4f643fb4-fd21-11e8-ae49-0050568e2c1e", name="event_cifs")
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


__all__ = ["FpolicyEvent", "FpolicyEventSchema"]
__pdoc__ = {
    "FpolicyEventSchema.resource": False,
    "FpolicyEventSchema.opts": False,
}


class FpolicyEventSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FpolicyEvent object"""

    file_operations = marshmallow_fields.Nested("netapp_ontap.models.fpolicy_event_file_operations.FpolicyEventFileOperationsSchema", data_key="file_operations", unknown=EXCLUDE, allow_none=True)
    r""" Specifies the file operations for the FPolicy event. You must specify a valid protocol in the protocol parameter.
The event will check the operations specified from all client requests using the protocol."""

    filters = marshmallow_fields.Nested("netapp_ontap.models.fpolicy_event_filters.FpolicyEventFiltersSchema", data_key="filters", unknown=EXCLUDE, allow_none=True)
    r""" Specifies the list of filters for a given file operation for the specified protocol.
When you specify the filters, you must specify the valid protocols and a valid file operations."""

    monitor_fileop_failure = marshmallow_fields.Boolean(
        data_key="monitor_fileop_failure",
        allow_none=True,
    )
    r""" Specifies whether failed file operations monitoring is required."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Specifies the name of the FPolicy event.

Example: event_cifs"""

    protocol = marshmallow_fields.Str(
        data_key="protocol",
        validate=enum_validation(['cifs', 'nfsv3', 'nfsv4']),
        allow_none=True,
    )
    r""" Protocol for which event is created. If you specify protocol, then you
must also specify a valid value for the file operation parameters.
  The value of this parameter must be one of the following:

    * cifs  - for the CIFS protocol.
    * nfsv3 - for the NFSv3 protocol.
    * nfsv4 - for the NFSv4 protocol.


Valid choices:

* cifs
* nfsv3
* nfsv4"""

    svm = marshmallow_fields.Nested("netapp_ontap.models.fpolicy_engine_svm.FpolicyEngineSvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the fpolicy_event."""

    volume_monitoring = marshmallow_fields.Boolean(
        data_key="volume_monitoring",
        allow_none=True,
    )
    r""" Specifies whether volume operation monitoring is required."""

    @property
    def resource(self):
        return FpolicyEvent

    gettable_fields = [
        "file_operations",
        "filters",
        "monitor_fileop_failure",
        "name",
        "protocol",
        "svm",
        "volume_monitoring",
    ]
    """file_operations,filters,monitor_fileop_failure,name,protocol,svm,volume_monitoring,"""

    patchable_fields = [
        "file_operations",
        "filters",
        "monitor_fileop_failure",
        "protocol",
        "volume_monitoring",
    ]
    """file_operations,filters,monitor_fileop_failure,protocol,volume_monitoring,"""

    postable_fields = [
        "file_operations",
        "filters",
        "monitor_fileop_failure",
        "name",
        "protocol",
        "volume_monitoring",
    ]
    """file_operations,filters,monitor_fileop_failure,name,protocol,volume_monitoring,"""

class FpolicyEvent(Resource):
    r""" The information that a FPolicy process needs to determine what file access operations to monitor and for which of the monitored events notifications should be sent to the external FPolicy server. """

    _schema = FpolicyEventSchema
    _path = "/api/protocols/fpolicy/{svm[uuid]}/events"
    _keys = ["svm.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves FPolicy event configurations for all events for a specified SVM. ONTAP allows the creation of cluster-level FPolicy events that act as a template for all the data SVMs belonging to the cluster. These cluster-level FPolicy events are also retrieved for the specified SVM.
### Related ONTAP commands
* `fpolicy policy event show`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/events`](#docs-NAS-protocols_fpolicy_{svm.uuid}_events)
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
        """Returns a count of all FpolicyEvent resources that match the provided query"""
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
        """Returns a list of RawResources that represent FpolicyEvent resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["FpolicyEvent"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a specific FPolicy event configuration for an SVM. A cluster-level FPolicy event configuration cannot be modified for a data SVM through REST. When the file operations and filters fields are modified, the previous values are retained and new values are added to the list of previous values. To remove a particular file operation or filter, set its value to false in the request.
### Related ONTAP commands
* `fpolicy policy event modify`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/events`](#docs-NAS-protocols_fpolicy_{svm.uuid}_events)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["FpolicyEvent"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["FpolicyEvent"], NetAppResponse]:
        r"""Creates an FPolicy event configuration for a specified SVM. FPolicy event creation is allowed only on data SVMs. When a protocol is specified, you must specify a file operation or a file operation and filters. When FPolicy event is configured to monitor failed file operations, you must specify protocol and file operations. Filters are not supported when failed file operations are monitored.
### Required properties
* `svm.uuid` - Existing SVM in which to create the FPolicy event.
* `name` - Name of the FPolicy event.
### Recommended optional properties
* `file-operations` - List of file operations to monitor.
* `protocol` - Protocol for which the file operations should be monitored.
* `filters` - List of filters for the specified file operations.
* `monitor-fileop-failure` - Enabled monitoring of failed file operations.
### Default property values
If not specified in POST, the following default property values are assigned:
* `file_operations.*` - _false_
* `filters.*` - _false_
* `volume-monitoring` - _false_
* `monitor-fileop-failure` - _false_
### Related ONTAP commands
* `fpolicy policy event create`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/events`](#docs-NAS-protocols_fpolicy_{svm.uuid}_events)
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
        records: Iterable["FpolicyEvent"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a specific FPolicy event configuration for an SVM. A cluster-level FPolicy event configuration cannot be modified for a data SVM through REST. An FPolicy event that is attached to an FPolicy policy cannot be deleted.
### Related ONTAP commands
* `fpolicy policy event delete`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/events`](#docs-NAS-protocols_fpolicy_{svm.uuid}_events)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves FPolicy event configurations for all events for a specified SVM. ONTAP allows the creation of cluster-level FPolicy events that act as a template for all the data SVMs belonging to the cluster. These cluster-level FPolicy events are also retrieved for the specified SVM.
### Related ONTAP commands
* `fpolicy policy event show`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/events`](#docs-NAS-protocols_fpolicy_{svm.uuid}_events)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific FPolicy event configuration for an SVM. A cluster-level FPolicy event configuration cannot be retrieved for a data SVM through a REST API.
### Related ONTAP commands
* `fpolicy policy event show`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/events`](#docs-NAS-protocols_fpolicy_{svm.uuid}_events)
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
        r"""Creates an FPolicy event configuration for a specified SVM. FPolicy event creation is allowed only on data SVMs. When a protocol is specified, you must specify a file operation or a file operation and filters. When FPolicy event is configured to monitor failed file operations, you must specify protocol and file operations. Filters are not supported when failed file operations are monitored.
### Required properties
* `svm.uuid` - Existing SVM in which to create the FPolicy event.
* `name` - Name of the FPolicy event.
### Recommended optional properties
* `file-operations` - List of file operations to monitor.
* `protocol` - Protocol for which the file operations should be monitored.
* `filters` - List of filters for the specified file operations.
* `monitor-fileop-failure` - Enabled monitoring of failed file operations.
### Default property values
If not specified in POST, the following default property values are assigned:
* `file_operations.*` - _false_
* `filters.*` - _false_
* `volume-monitoring` - _false_
* `monitor-fileop-failure` - _false_
### Related ONTAP commands
* `fpolicy policy event create`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/events`](#docs-NAS-protocols_fpolicy_{svm.uuid}_events)
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
        r"""Updates a specific FPolicy event configuration for an SVM. A cluster-level FPolicy event configuration cannot be modified for a data SVM through REST. When the file operations and filters fields are modified, the previous values are retained and new values are added to the list of previous values. To remove a particular file operation or filter, set its value to false in the request.
### Related ONTAP commands
* `fpolicy policy event modify`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/events`](#docs-NAS-protocols_fpolicy_{svm.uuid}_events)
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
        r"""Deletes a specific FPolicy event configuration for an SVM. A cluster-level FPolicy event configuration cannot be modified for a data SVM through REST. An FPolicy event that is attached to an FPolicy policy cannot be deleted.
### Related ONTAP commands
* `fpolicy policy event delete`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/events`](#docs-NAS-protocols_fpolicy_{svm.uuid}_events)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


