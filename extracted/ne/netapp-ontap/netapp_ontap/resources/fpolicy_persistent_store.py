r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
- The FPolicy Persistent Store feature enables the configuration of a Persistent Store.
  This includes:
  - setting up a store to retain event notifications
  - specifying the volume created for FPolicy Persistent Store
  - defining the size of the volume
  - defining the autosize mode for the volume.
- Each SVM can only have one Persistent Store. The same Persistent Store can be used by multiple policies within the same SVM. Once a Persistent Store is created, it can be utilized in the FPolicy policy configuration for the async and non-mandatory engine.
## Examples
### Creating an FPolicy Persistent Store with all required parameters
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyPersistentStore

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyPersistentStore("4f643fb4-fd21-11e8-ae49-0050568e2c1e")
    resource.name = "ps1"
    resource.volume = "psvol"
    resource.size = 1073741824
    resource.autosize_mode = "off"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
FpolicyPersistentStore(
    {"volume": "psvol", "name": "ps1", "autosize_mode": "off", "size": 1073741824}
)

```
</div>
</div>

---
### Creating an FPolicy Persistent Store with the minimum required fields
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyPersistentStore

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyPersistentStore("4f643fb4-fd21-11e8-ae49-0050568e2c1e")
    resource.name = "ps1"
    resource.volume = "psvol"
    resource.size = 1073741824
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
FpolicyPersistentStore({"volume": "psvol", "name": "ps1", "size": 1073741824})

```
</div>
</div>

---
### Retrieving an FPolicy Persistent Store configuration for a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyPersistentStore

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            FpolicyPersistentStore.get_collection(
                "4f643fb4-fd21-11e8-ae49-0050568e2c1e", return_timeout=15
            )
        )
    )

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[FpolicyPersistentStore({"name": "ps1"})]

```
</div>
</div>

---
### Retrieving a specific FPolicy Persistent Store configuration for a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyPersistentStore

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyPersistentStore(
        "4f643fb4-fd21-11e8-ae49-0050568e2c1e", name="persistent_fpolicy"
    )
    resource.get(fields="*", return_timeout=15)
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
FpolicyPersistentStore(
    {
        "volume": "psvol",
        "name": "ps1",
        "autosize_mode": "off",
        "svm": {"uuid": "4f643fb4-fd21-11e8-ae49-0050568e2c1e"},
        "size": 1073741824,
    }
)

```
</div>
</div>

---
### Updating an FPolicy Persistent Store for an SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyPersistentStore

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyPersistentStore(
        "4f643fb4-fd21-11e8-ae49-0050568e2c1e", name="persistent_fpolicy"
    )
    resource.volume = "psvol"
    resource.size = 1073741824
    resource.patch()

```

---
### Deleting a specific FPolicy Persistent Store configuration for a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyPersistentStore

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyPersistentStore(
        "4f643fb4-fd21-11e8-ae49-0050568e2c1e", name="persistent_fpolicy"
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


__all__ = ["FpolicyPersistentStore", "FpolicyPersistentStoreSchema"]
__pdoc__ = {
    "FpolicyPersistentStoreSchema.resource": False,
    "FpolicyPersistentStoreSchema.opts": False,
}


class FpolicyPersistentStoreSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FpolicyPersistentStore object"""

    autosize_mode = marshmallow_fields.Str(
        data_key="autosize_mode",
        validate=enum_validation(['grow', 'grow_shrink', 'off']),
        allow_none=True,
    )
    r""" Autosize mode for the volume.<br>grow &dash; Volume automatically grows in response to the amount of space used.<br>grow_shrink &dash; Volume grows or shrinks in response to the amount of space used.<br>off &dash; Autosizing of the volume is disabled.

Valid choices:

* grow
* grow_shrink
* off"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The name specified for the FPolicy Persistent Store.

Example: ps1"""

    size = Size(
        data_key="size",
        allow_none=True,
    )
    r""" The size of the Persistent Store volume, in bytes.

Example: 100M"""

    svm = marshmallow_fields.Nested("netapp_ontap.models.fpolicy_engine_svm.FpolicyEngineSvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the fpolicy_persistent_store."""

    volume = marshmallow_fields.Str(
        data_key="volume",
        allow_none=True,
    )
    r""" The specified volume to store the events for the FPolicy Persistent Store.

Example: psvol"""

    @property
    def resource(self):
        return FpolicyPersistentStore

    gettable_fields = [
        "autosize_mode",
        "name",
        "size",
        "svm",
        "volume",
    ]
    """autosize_mode,name,size,svm,volume,"""

    patchable_fields = [
        "size",
        "volume",
    ]
    """size,volume,"""

    postable_fields = [
        "autosize_mode",
        "name",
        "size",
        "volume",
    ]
    """autosize_mode,name,size,volume,"""

class FpolicyPersistentStore(Resource):
    r""" The information that an FPolicy process needs in order to configure a Persistent Store. """

    _schema = FpolicyPersistentStoreSchema
    _path = "/api/protocols/fpolicy/{svm[uuid]}/persistent-stores"
    _keys = ["svm.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves FPolicy Persistent Store configurations for a specified SVM.
### Related ONTAP commands
* `fpolicy persistent-store show`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/persistent-stores`](#docs-NAS-protocols_fpolicy_{svm.uuid}_persistent-stores)
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
        """Returns a count of all FpolicyPersistentStore resources that match the provided query"""
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
        """Returns a list of RawResources that represent FpolicyPersistentStore resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["FpolicyPersistentStore"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a specific FPolicy Persistent Store configuration for an SVM.
</br>Important notes:
* If the volume exists, it is set to the size specified and the snapshot policy is set to "none". Otherwise, a new volume is created.
* The autosize parameter is not available in PATCH operations for this endpoint, use the the "autosize" parameter in PATCH for the "/storage/volumes/{uuid}" endpoint instead.
* When the Persistent Store is updated with a new volume, the previous volume is not automatically deleted. An option is provided to delete the previous volume.
### Related ONTAP commands
* `fpolicy persistent-store modify`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/persistent-stores`](#docs-NAS-protocols_fpolicy_{svm.uuid}_persistent-stores)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["FpolicyPersistentStore"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["FpolicyPersistentStore"], NetAppResponse]:
        r"""Creates an FPolicy Persistent Store configuration for a specified SVM.
</br>Important notes:
* FPolicy Persistent Store creation is allowed only on data SVMs.
* In persistent mode, when the Persistent Store is full, event notifications are dropped.
* There is flexibility to provide an existing volume or create a new volume for the persistent storage. The creation of new volume is handled internally.
* For existing volumes, the snapshot policy is set to 'none' and the size is adjusted to the specified value.
### Required properties
* `svm.uuid` - Existing SVM in which to create the FPolicy Persistent Store.
* `name` - Name of the FPolicy Persistent Store.
* `volume` - Volume specified for Persistent Store (only FlexVol volumes of type RW are supported).
### Optional properties
* `size` - Size of the Persistent Store volume.
* `autosize-mode` - Autosize mode for the Persistent Store volume.
### Related ONTAP commands
* `fpolicy persistent-store create`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/persistent-stores`](#docs-NAS-protocols_fpolicy_{svm.uuid}_persistent-stores)
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
        records: Iterable["FpolicyPersistentStore"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a specific FPolicy Persistent Store configuration for an SVM.
</br>Important notes:
An option has been provided to delete the associated volume.
### Related ONTAP commands
* `fpolicy persistent-store delete`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/persistent-stores`](#docs-NAS-protocols_fpolicy_{svm.uuid}_persistent-stores)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves FPolicy Persistent Store configurations for a specified SVM.
### Related ONTAP commands
* `fpolicy persistent-store show`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/persistent-stores`](#docs-NAS-protocols_fpolicy_{svm.uuid}_persistent-stores)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific FPolicy Persistent Store configuration for an SVM.
### Related ONTAP commands
* `fpolicy persistent-store show`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/persistent-stores`](#docs-NAS-protocols_fpolicy_{svm.uuid}_persistent-stores)
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
        r"""Creates an FPolicy Persistent Store configuration for a specified SVM.
</br>Important notes:
* FPolicy Persistent Store creation is allowed only on data SVMs.
* In persistent mode, when the Persistent Store is full, event notifications are dropped.
* There is flexibility to provide an existing volume or create a new volume for the persistent storage. The creation of new volume is handled internally.
* For existing volumes, the snapshot policy is set to 'none' and the size is adjusted to the specified value.
### Required properties
* `svm.uuid` - Existing SVM in which to create the FPolicy Persistent Store.
* `name` - Name of the FPolicy Persistent Store.
* `volume` - Volume specified for Persistent Store (only FlexVol volumes of type RW are supported).
### Optional properties
* `size` - Size of the Persistent Store volume.
* `autosize-mode` - Autosize mode for the Persistent Store volume.
### Related ONTAP commands
* `fpolicy persistent-store create`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/persistent-stores`](#docs-NAS-protocols_fpolicy_{svm.uuid}_persistent-stores)
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
        r"""Updates a specific FPolicy Persistent Store configuration for an SVM.
</br>Important notes:
* If the volume exists, it is set to the size specified and the snapshot policy is set to "none". Otherwise, a new volume is created.
* The autosize parameter is not available in PATCH operations for this endpoint, use the the "autosize" parameter in PATCH for the "/storage/volumes/{uuid}" endpoint instead.
* When the Persistent Store is updated with a new volume, the previous volume is not automatically deleted. An option is provided to delete the previous volume.
### Related ONTAP commands
* `fpolicy persistent-store modify`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/persistent-stores`](#docs-NAS-protocols_fpolicy_{svm.uuid}_persistent-stores)
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
        r"""Deletes a specific FPolicy Persistent Store configuration for an SVM.
</br>Important notes:
An option has been provided to delete the associated volume.
### Related ONTAP commands
* `fpolicy persistent-store delete`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/persistent-stores`](#docs-NAS-protocols_fpolicy_{svm.uuid}_persistent-stores)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


