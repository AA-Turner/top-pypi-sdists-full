r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
The FPolicy policy acts as a container for different constituents of the FPolicy such as FPolicy events and the FPolicy engine. It also provides a platform for policy management functions, such as policy enabling and disabling. As part of FPolicy policy configuration, you can specify the name of policy, the SVM to which it belongs, the FPolicy events to monitor, the FPolicy engine to which the generated notifications are sent and the policy priority. FPolicy policy configuration also allows to you to configure the file access behavior when the primary and secondary servers are down. Under such circumstances, if the "mandatory" field is set to true, file access is denied.</br>
Each FPolicy policy is associated with a scope which allows you to restrain the scope of the policy to specified storage objects such as volume, shares and export or to a set of file extensions such as .txt, .jpeg. An FPolicy policy can be configured to send notifications, to the FPolicy server or for native file blocking which uses the file extension specified in the policy scope. An SVM can have multiple FPolicy policies which can be enabled or disabled independently of each other.
## Examples
### Creating an FPolicy policy
Use the following API to create an FPolicy policy configuration. Note that the <i>return_records=true</i> query parameter used to obtain the newly created entry in the response.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyPolicy("a00fac5d-0164-11e9-b64a-0050568eeb34")
    resource.engine = {"name": "engine1"}
    resource.events = [{"name": "cifs"}, {"name": "nfs"}]
    resource.mandatory = True
    resource.name = "FPolicy_policy_0"
    resource.passthrough_read = True
    resource.privileged_user = "mydomain\testuser"
    resource.scope = {
        "exclude_export_policies": ["export_pol1"],
        "exclude_extension": ["txt", "png"],
        "exclude_shares": ["sh1"],
        "exclude_volumes": ["vol0"],
        "include_export_policies": ["export_pol10"],
        "include_extension": ["pdf"],
        "include_shares": ["sh2", "sh3"],
        "include_volumes": ["vol1", "vol2"],
    }
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
FpolicyPolicy(
    {
        "passthrough_read": True,
        "name": "FPolicy_policy_0",
        "events": [{"name": "cifs"}, {"name": "nfs"}],
        "privileged_user": "mydomain\\testuser",
        "mandatory": True,
        "engine": {"name": "engine1"},
        "scope": {
            "exclude_export_policies": ["export_pol1"],
            "include_export_policies": ["export_pol10"],
            "include_volumes": ["vol1", "vol2"],
            "include_shares": ["sh2", "sh3"],
            "exclude_volumes": ["vol0"],
            "exclude_shares": ["sh1"],
            "include_extension": ["pdf"],
            "exclude_extension": ["txt", "png"],
        },
    }
)

```
</div>
</div>

---
### Creating and enable an FPolicy policy
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyPolicy("a00fac5d-0164-11e9-b64a-0050568eeb34")
    resource.priority = 1
    resource.engine = {"name": "engine1"}
    resource.events = [{"name": "cifs"}, {"name": "nfs"}]
    resource.mandatory = True
    resource.name = "FPolicy_policy_on"
    resource.passthrough_read = False
    resource.scope = {
        "exclude_export_policies": ["export_pol1"],
        "exclude_extension": ["txt", "png"],
        "exclude_shares": ["sh1"],
        "exclude_volumes": ["vol0"],
        "include_export_policies": ["export_pol10"],
        "include_extension": ["pdf"],
        "include_shares": ["sh2", "sh3"],
        "include_volumes": ["vol1", "vol2"],
    }
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
FpolicyPolicy(
    {
        "passthrough_read": True,
        "priority": 1,
        "name": "FPolicy_policy_0",
        "events": [{"name": "cifs"}, {"name": "nfs"}],
        "privileged_user": "mydomain\\testuser",
        "mandatory": True,
        "engine": {"name": "engine1"},
        "scope": {
            "exclude_export_policies": ["export_pol1"],
            "include_export_policies": ["export_pol10"],
            "include_volumes": ["vol1", "vol2"],
            "include_shares": ["sh2", "sh3"],
            "exclude_volumes": ["vol0"],
            "exclude_shares": ["sh1"],
            "include_extension": ["pdf"],
            "exclude_extension": ["txt", "png"],
        },
    }
)

```
</div>
</div>

---
### Creating an FPolicy policy with the minimum required fields and a native engine
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyPolicy("a00fac5d-0164-11e9-b64a-0050568eeb34")
    resource.events = [{"name": "cifs"}, {"name": "nfs"}]
    resource.name = "pol_minimum_fields"
    resource.scope = {"include_volumes": ["vol1", "vol2"]}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
FpolicyPolicy(
    {
        "name": "pol_minimum_fields",
        "events": [{"name": "cifs"}, {"name": "nfs"}],
        "scope": {"include_volumes": ["vol1", "vol2"]},
    }
)

```
</div>
</div>

---
### Retrieving all the FPolicy policy configurations for an SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            FpolicyPolicy.get_collection(
                "a00fac5d-0164-11e9-b64a-0050568eeb34", fields="*", return_timeout=15
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
    FpolicyPolicy(
        {
            "passthrough_read": False,
            "name": "pol0",
            "enabled": False,
            "events": [{"name": "cifs"}, {"name": "nfs"}],
            "persistent_store": "ps1",
            "svm": {"uuid": "a00fac5d-0164-11e9-b64a-0050568eeb34"},
            "mandatory": True,
            "allow_privileged_access": False,
            "engine": {"name": "engine1"},
            "scope": {
                "exclude_export_policies": ["export_pol1"],
                "include_export_policies": ["export_pol10"],
                "include_volumes": ["vol1", "vol2"],
                "include_shares": ["sh2", "sh3"],
                "exclude_volumes": ["vol0"],
                "exclude_shares": ["sh1"],
                "include_extension": ["pdf"],
                "exclude_extension": ["txt", "png"],
            },
        }
    ),
    FpolicyPolicy(
        {
            "passthrough_read": False,
            "priority": 1,
            "name": "FPolicy_policy_on",
            "enabled": True,
            "events": [{"name": "cifs"}, {"name": "nfs"}],
            "persistent_store": "ps1",
            "svm": {"uuid": "a00fac5d-0164-11e9-b64a-0050568eeb34"},
            "mandatory": True,
            "allow_privileged_access": False,
            "engine": {"name": "engine1"},
            "scope": {
                "exclude_export_policies": ["export_pol1"],
                "include_export_policies": ["export_pol10"],
                "include_volumes": ["vol1", "vol2"],
                "include_shares": ["sh2", "sh3"],
                "exclude_volumes": ["vol0"],
                "exclude_shares": ["sh1"],
                "include_extension": ["pdf"],
                "exclude_extension": ["txt", "png"],
            },
        }
    ),
    FpolicyPolicy(
        {
            "passthrough_read": False,
            "name": "cluster_pol",
            "enabled": False,
            "events": [{"name": "cluster"}],
            "persistent_store": "ps1",
            "svm": {"uuid": "a00fac5d-0164-11e9-b64a-0050568eeb34"},
            "mandatory": True,
            "allow_privileged_access": False,
            "engine": {"name": "native"},
        }
    ),
    FpolicyPolicy(
        {
            "passthrough_read": False,
            "name": "pol_minimum_fields",
            "enabled": False,
            "events": [{"name": "cifs"}, {"name": "nfs"}],
            "persistent_store": "ps1",
            "svm": {"uuid": "a00fac5d-0164-11e9-b64a-0050568eeb34"},
            "mandatory": True,
            "allow_privileged_access": False,
            "engine": {"name": "native"},
            "scope": {"include_volumes": ["vol1", "vol2"]},
        }
    ),
]

```
</div>
</div>

---
### Retrieving all of the FPolicy policy configurations for the FPolicy engine "engine1" for an SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            FpolicyPolicy.get_collection(
                "a00fac5d-0164-11e9-b64a-0050568eeb34",
                fields="*",
                return_timeout=15,
                **{"engine.name": "engine1"}
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
    FpolicyPolicy(
        {
            "passthrough_read": False,
            "name": "pol0",
            "enabled": False,
            "events": [{"name": "cifs"}, {"name": "nfs"}],
            "persistent_store": "ps1",
            "svm": {"uuid": "a00fac5d-0164-11e9-b64a-0050568eeb34"},
            "mandatory": True,
            "allow_privileged_access": False,
            "engine": {"name": "engine1"},
            "scope": {
                "exclude_export_policies": ["export_pol1"],
                "include_export_policies": ["export_pol10"],
                "include_extension": ["pdf"],
                "exclude_extension": ["txt", "png"],
            },
        }
    ),
    FpolicyPolicy(
        {
            "passthrough_read": False,
            "priority": 1,
            "name": "FPolicy_policy_on",
            "enabled": True,
            "events": [{"name": "cifs"}, {"name": "nfs"}],
            "persistent_store": "ps1",
            "svm": {"uuid": "a00fac5d-0164-11e9-b64a-0050568eeb34"},
            "mandatory": True,
            "allow_privileged_access": False,
            "engine": {"name": "engine1"},
            "scope": {
                "exclude_export_policies": ["export_pol1"],
                "include_export_policies": ["export_pol10"],
                "include_volumes": ["vol1", "vol2"],
                "include_shares": ["sh2", "sh3"],
                "exclude_volumes": ["vol0"],
                "exclude_shares": ["sh1"],
                "include_extension": ["pdf"],
                "exclude_extension": ["txt", "png"],
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving a particular FPolicy policy configuration for an SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyPolicy("a00fac5d-0164-11e9-b64a-0050568eeb34", name="pol0")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
FpolicyPolicy(
    {
        "passthrough_read": False,
        "name": "pol0",
        "enabled": False,
        "events": [{"name": "cifs"}, {"name": "nfs"}],
        "persistent_store": "ps1",
        "svm": {"uuid": "a00fac5d-0164-11e9-b64a-0050568eeb34"},
        "mandatory": True,
        "allow_privileged_access": False,
        "engine": {"name": "engine1"},
        "scope": {
            "exclude_export_policies": ["export_pol1"],
            "include_export_policies": ["export_pol10"],
            "include_volumes": ["vol1", "vol2"],
            "include_shares": ["sh2", "sh3"],
            "exclude_volumes": ["vol0"],
            "exclude_shares": ["sh1"],
            "include_extension": ["pdf"],
            "exclude_extension": ["txt", "png"],
        },
    }
)

```
</div>
</div>

---
### Updating a particular FPolicy policy
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyPolicy("a00fac5d-0164-11e9-b64a-0050568eeb34", name="pol0")
    resource.engine = {"name": "native"}
    resource.events = [{"name": "cifs"}]
    resource.mandatory = False
    resource.scope = {"include_volumes": ["*"]}
    resource.patch()

```

---
### Enabling a particular FPolicy policy
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyPolicy("a00fac5d-0164-11e9-b64a-0050568eeb34", name="pol0")
    resource.enabled = True
    resource.priority = 3
    resource.patch()

```

---
### Disabling a particular FPolicy policy
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyPolicy("a00fac5d-0164-11e9-b64a-0050568eeb34", name="pol0")
    resource.enabled = True
    resource.patch()

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


__all__ = ["FpolicyPolicy", "FpolicyPolicySchema"]
__pdoc__ = {
    "FpolicyPolicySchema.resource": False,
    "FpolicyPolicySchema.opts": False,
}


class FpolicyPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FpolicyPolicy object"""

    allow_privileged_access = marshmallow_fields.Boolean(
        data_key="allow_privileged_access",
        allow_none=True,
    )
    r""" Specifies whether privileged access is required for FPolicy servers.
Privileged access is used when the FPolicy server requires direct
access to the cluster nodes. When this parameter is set to true,
FPolicy servers can access files on the cluster using a separate
data channel with privileged access."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Specifies if the policy is enabled on the SVM or not. If no value is
mentioned for this field but priority is set, then this policy will be enabled."""

    engine = marshmallow_fields.Nested("netapp_ontap.resources.fpolicy_engine.FpolicyEngineSchema", data_key="engine", unknown=EXCLUDE, allow_none=True)
    r""" The engine field of the fpolicy_policy."""

    events = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.fpolicy_event.FpolicyEventSchema", unknown=EXCLUDE, allow_none=True), data_key="events", allow_none=True)
    r""" The events field of the fpolicy_policy.

Example: ["event_cifs","event_open"]"""

    mandatory = marshmallow_fields.Boolean(
        data_key="mandatory",
        allow_none=True,
    )
    r""" Specifies what action to take on a file access event in a case when all primary and secondary servers are down or no response is received from the FPolicy servers within a given timeout period. When this parameter is set to true, file access events will be denied under these circumstances."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Specifies the name of the policy.

Example: fp_policy_1"""

    passthrough_read = marshmallow_fields.Boolean(
        data_key="passthrough_read",
        allow_none=True,
    )
    r""" Specifies whether passthrough-read should be allowed for FPolicy servers
registered for the policy. Passthrough-read is a way to read data for
offline files without restoring the files to primary storage. Offline
files are files that have been moved to secondary storage."""

    persistent_store = marshmallow_fields.Str(
        data_key="persistent_store",
        allow_none=True,
    )
    r""" Specifies the persistent storage name. This can then be used
to enable persistent mode for FPolicy events.


Example: ps1"""

    priority = Size(
        data_key="priority",
        validate=integer_validation(minimum=1, maximum=10),
        allow_none=True,
    )
    r""" Specifies the priority that is assigned to this policy.

Example: 1"""

    privileged_user = marshmallow_fields.Str(
        data_key="privileged_user",
        allow_none=True,
    )
    r""" Specifies the privileged user name for accessing files on the cluster
using a separate data channel with privileged access. The input for
this field should be in "domain\username" format.


Example: mydomain\testuser"""

    scope = marshmallow_fields.Nested("netapp_ontap.models.fpolicy_policies_scope.FpolicyPoliciesScopeSchema", data_key="scope", unknown=EXCLUDE, allow_none=True)
    r""" The scope field of the fpolicy_policy."""

    svm = marshmallow_fields.Nested("netapp_ontap.models.fpolicy_engine_svm.FpolicyEngineSvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the fpolicy_policy."""

    @property
    def resource(self):
        return FpolicyPolicy

    gettable_fields = [
        "allow_privileged_access",
        "enabled",
        "engine.links",
        "engine.name",
        "events",
        "mandatory",
        "name",
        "passthrough_read",
        "persistent_store",
        "priority",
        "privileged_user",
        "scope",
        "svm",
    ]
    """allow_privileged_access,enabled,engine.links,engine.name,events,mandatory,name,passthrough_read,persistent_store,priority,privileged_user,scope,svm,"""

    patchable_fields = [
        "allow_privileged_access",
        "enabled",
        "engine.name",
        "events",
        "mandatory",
        "passthrough_read",
        "persistent_store",
        "priority",
        "privileged_user",
        "scope",
    ]
    """allow_privileged_access,enabled,engine.name,events,mandatory,passthrough_read,persistent_store,priority,privileged_user,scope,"""

    postable_fields = [
        "engine.name",
        "events",
        "mandatory",
        "name",
        "passthrough_read",
        "persistent_store",
        "priority",
        "privileged_user",
        "scope",
    ]
    """engine.name,events,mandatory,name,passthrough_read,persistent_store,priority,privileged_user,scope,"""

class FpolicyPolicy(Resource):
    """Allows interaction with FpolicyPolicy objects on the host"""

    _schema = FpolicyPolicySchema
    _path = "/api/protocols/fpolicy/{svm[uuid]}/policies"
    _keys = ["svm.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the FPolicy policy configuration of an SVM. ONTAP allows the creation of a cluster level FPolicy policy that acts as a template for all the data SVMs belonging to the cluster. This cluster level FPolicy policy is also retrieved for the specified SVM.
### Related ONTAP commands
* `fpolicy policy show`
* `fpolicy policy scope show`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/policies`](#docs-NAS-protocols_fpolicy_{svm.uuid}_policies)
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
        """Returns a count of all FpolicyPolicy resources that match the provided query"""
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
        """Returns a list of RawResources that represent FpolicyPolicy resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["FpolicyPolicy"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a particular FPolicy policy configuration for a specified SVM. PATCH can be used to enable or disable the policy. When enabling a policy, you must specify the policy priority. The policy priority of the policy is not required when disabling the policy. If the policy is enabled, the FPolicy policy cannot be modified.
### Related ONTAP commands
* `fpolicy policy modify`
* `fpolicy policy scope modify`
* `fpolicy enable`
* `fpolicy disable`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/policies`](#docs-NAS-protocols_fpolicy_{svm.uuid}_policies)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["FpolicyPolicy"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["FpolicyPolicy"], NetAppResponse]:
        r"""Creates an FPolicy policy configuration for the specified SVM. To create an FPolicy policy, you must specify the policy scope and the FPolicy events to be monitored.
</br>Important notes:
* A single policy can monitor multiple events.
* An FPolicy engine is an optional field whose default value is set to native. A native engine can be used to simply block the file access based on the file extensions specified in the policy scope.
* To enable a policy, the policy priority  must be specified. If the priority is not specified, the policy is created but it is not enabled.
* The "mandatory" field, if set to true, blocks the file access when the primary or secondary FPolicy servers are down.
### Required properties
* `svm.uuid` - Existing SVM in which to create the FPolicy policy.
* `events` - Name of the events to monitor.
* `name` - Name of the FPolicy policy.
* `scope` - Scope of the policy. Can be limited to exports, volumes, shares or file extensions.
* `priority`- Priority of the policy (ranging from 1 to 10).
### Default property values
* `mandatory` - _true_
* `engine` - _native_
### Related ONTAP commands
* `fpolicy policy scope create`
* `fpolicy policy create`
* `fpolicy enable`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/policies`](#docs-NAS-protocols_fpolicy_{svm.uuid}_policies)
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
        records: Iterable["FpolicyPolicy"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a particular FPolicy policy configuration for a specified SVM. To delete a policy, you must first disable the policy.
### Related ONTAP commands
* `fpolicy policy scope delete`
* `fpolicy policy delete`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/policies`](#docs-NAS-protocols_fpolicy_{svm.uuid}_policies)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the FPolicy policy configuration of an SVM. ONTAP allows the creation of a cluster level FPolicy policy that acts as a template for all the data SVMs belonging to the cluster. This cluster level FPolicy policy is also retrieved for the specified SVM.
### Related ONTAP commands
* `fpolicy policy show`
* `fpolicy policy scope show`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/policies`](#docs-NAS-protocols_fpolicy_{svm.uuid}_policies)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a particular FPolicy policy configuration for a specified SVM. Cluster-level FPolicy policy configuration details cannot be retrieved for a data SVM.
### Related ONTAP commands
* `fpolicy policy show`
* `fpolicy policy scope show`
* `fpolicy show`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/policies`](#docs-NAS-protocols_fpolicy_{svm.uuid}_policies)
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
        r"""Creates an FPolicy policy configuration for the specified SVM. To create an FPolicy policy, you must specify the policy scope and the FPolicy events to be monitored.
</br>Important notes:
* A single policy can monitor multiple events.
* An FPolicy engine is an optional field whose default value is set to native. A native engine can be used to simply block the file access based on the file extensions specified in the policy scope.
* To enable a policy, the policy priority  must be specified. If the priority is not specified, the policy is created but it is not enabled.
* The "mandatory" field, if set to true, blocks the file access when the primary or secondary FPolicy servers are down.
### Required properties
* `svm.uuid` - Existing SVM in which to create the FPolicy policy.
* `events` - Name of the events to monitor.
* `name` - Name of the FPolicy policy.
* `scope` - Scope of the policy. Can be limited to exports, volumes, shares or file extensions.
* `priority`- Priority of the policy (ranging from 1 to 10).
### Default property values
* `mandatory` - _true_
* `engine` - _native_
### Related ONTAP commands
* `fpolicy policy scope create`
* `fpolicy policy create`
* `fpolicy enable`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/policies`](#docs-NAS-protocols_fpolicy_{svm.uuid}_policies)
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
        r"""Updates a particular FPolicy policy configuration for a specified SVM. PATCH can be used to enable or disable the policy. When enabling a policy, you must specify the policy priority. The policy priority of the policy is not required when disabling the policy. If the policy is enabled, the FPolicy policy cannot be modified.
### Related ONTAP commands
* `fpolicy policy modify`
* `fpolicy policy scope modify`
* `fpolicy enable`
* `fpolicy disable`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/policies`](#docs-NAS-protocols_fpolicy_{svm.uuid}_policies)
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
        r"""Deletes a particular FPolicy policy configuration for a specified SVM. To delete a policy, you must first disable the policy.
### Related ONTAP commands
* `fpolicy policy scope delete`
* `fpolicy policy delete`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/policies`](#docs-NAS-protocols_fpolicy_{svm.uuid}_policies)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


