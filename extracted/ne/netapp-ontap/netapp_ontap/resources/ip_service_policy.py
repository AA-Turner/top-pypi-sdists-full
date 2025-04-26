r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Service policies are named groupings that define what services are supported by an IP interface.
The following operations are supported:

  * Creation: POST network/ip/service-policies
  * Collection Get: GET network/ip/service-policies
  * Instance Get: GET network/ip/service-policies/{uuid}
  * Instance Patch: PATCH network/ip/service-policies/{uuid}
  * Instance Delete: DELETE network/ip/service-polices/{uuid}
## Examples
### Retrieving all service policies in the cluster
The following output shows the collection of all service policies configured in a 2-node cluster. By default (without 'field=*' parameter), only the UUID and name fields are shown for each entry.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpServicePolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(IpServicePolicy.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    IpServicePolicy(
        {
            "name": "net-intercluster",
            "uuid": "e4e2f193-c1a3-11e8-bb9d-005056bb88c8",
            "_links": {
                "self": {
                    "href": "/api/network/ip/service-policies/e4e2f193-c1a3-11e8-bb9d-005056bb88c8"
                }
            },
        }
    ),
    IpServicePolicy(
        {
            "name": "net-route-announce",
            "uuid": "e4e3f6da-c1a3-11e8-bb9d-005056bb88c8",
            "_links": {
                "self": {
                    "href": "/api/network/ip/service-policies/e4e3f6da-c1a3-11e8-bb9d-005056bb88c8"
                }
            },
        }
    ),
    IpServicePolicy(
        {
            "name": "vserver-route-announce",
            "uuid": "e5111111-c1a3-11e8-bb9d-005056bb88c8",
            "_links": {
                "self": {
                    "href": "/api/network/ip/service-policies/e5111111-c1a3-11e8-bb9d-005056bb88c8"
                }
            },
        }
    ),
    IpServicePolicy(
        {
            "name": "data-route-announce",
            "uuid": "e6111111-c1a3-11e8-bb9d-005056bb88c8",
            "_links": {
                "self": {
                    "href": "/api/network/ip/service-policies/e6111111-c1a3-11e8-bb9d-005056bb88c8"
                }
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific service policy (scope=svm)
The following output displays the response when a specific "svm" scoped service policy is requested. Among other parameters, the response contains the svm parameters associated with the service policy. The system returns an error when there is no service policy with the requested UUID.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpServicePolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpServicePolicy(uuid="dad323ff-4ce0-11e9-9372-005056bb91a8")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
IpServicePolicy(
    {
        "is_built_in": True,
        "services": ["data_core", "data_nfs", "data_cifs", "data_flexcache"],
        "ipspace": {
            "name": "Default",
            "_links": {
                "self": {
                    "href": "/api/network/ipspaces/45ec2dee-4ce0-11e9-9372-005056bb91a8"
                }
            },
            "uuid": "45ec2dee-4ce0-11e9-9372-005056bb91a8",
        },
        "name": "default-data-files",
        "uuid": "dad323ff-4ce0-11e9-9372-005056bb91a8",
        "_links": {
            "self": {
                "href": "/api/network/ip/service-policies/dad323ff-4ce0-11e9-9372-005056bb91a8"
            }
        },
        "svm": {
            "name": "vs0",
            "_links": {
                "self": {"href": "/api/svm/svms/d9060680-4ce0-11e9-9372-005056bb91a8"}
            },
            "uuid": "d9060680-4ce0-11e9-9372-005056bb91a8",
        },
        "scope": "svm",
    }
)

```
</div>
</div>

---
### Retrieving a specific service policy (scope=svm) when requesting commonly used fields
The following output displays the response when commonly used fields are requested for a specific "svm" scoped service policy. Among other parameters, the response contains the svm parameters associated with the service policy. The system returns an error when there is no service policy with the requested UUID.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpServicePolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpServicePolicy(uuid="e0889ce6-1e6a-11e9-89d6-005056bbdc04")
    resource.get(fields="name,scope,svm.name,ipspace.name")
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
IpServicePolicy(
    {
        "ipspace": {"name": "Default"},
        "name": "test_policy",
        "uuid": "e0889ce6-1e6a-11e9-89d6-005056bbdc04",
        "_links": {
            "self": {
                "href": "/api/network/ip/service-policies/e0889ce6-1e6a-11e9-89d6-005056bbdc04"
            }
        },
        "svm": {"name": "vs0"},
        "scope": "svm",
    }
)

```
</div>
</div>

---
### Retrieving a specific service policy (scope=cluster)
The following output displays the response when a specific cluster-scoped service policy is requested. The SVM object is not included for cluster-scoped service policies. A service policy with a scope of "cluster" is associated with an IPspace. The system returns an error when there is no service policy with the requested UUID.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpServicePolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpServicePolicy(uuid="4c6b72b9-0f6c-11e9-875d-005056bb21b8")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
IpServicePolicy(
    {
        "is_built_in": False,
        "services": ["intercluster_core"],
        "ipspace": {
            "name": "Default",
            "_links": {
                "self": {
                    "href": "/api/network/ipspaces/4051f13e-0f6c-11e9-875d-005056bb21b8"
                }
            },
            "uuid": "4051f13e-0f6c-11e9-875d-005056bb21b8",
        },
        "name": "net-intercluster",
        "uuid": "4c6b72b9-0f6c-11e9-875d-005056bb21b8",
        "_links": {
            "self": {
                "href": "/api/network/ip/service-policies/4c6b72b9-0f6c-11e9-875d-005056bb21b8"
            }
        },
        "scope": "cluster",
    }
)

```
</div>
</div>

---
### Retrieving a specific service policy (scope=cluster) when requesting commonly used fields
The following output displays the response when commonly used fields are requested for a specific "cluster" scoped service policy. The SVM object is not included for cluster-scoped service policies. A service policy with a scope of "cluster" is associated with an IPspace. The system returns an error when there is no service policy with the requested UUID.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpServicePolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpServicePolicy(uuid="4c6b72b9-0f6c-11e9-875d-005056bb21b8")
    resource.get(fields="name,scope,ipspace.name")
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
IpServicePolicy(
    {
        "services": ["intercluster_core"],
        "ipspace": {"name": "Default"},
        "name": "net-intercluster",
        "uuid": "4c6b72b9-0f6c-11e9-875d-005056bb21b8",
        "_links": {
            "self": {
                "href": "/api/network/ip/service-policies/4c6b72b9-0f6c-11e9-875d-005056bb21b8"
            }
        },
        "scope": "cluster",
    }
)

```
</div>
</div>

---
## Creating service policies
You can use this API to create an SVM-scoped service policy by specifying the associated SVM, or a cluster-scoped service policy by specifying the associated IPspace. If the scope is not specified, it is inferred from the presence of the IPspace or SVM.
Cluster scoped service policies will operate on the IPspace "Default" unless IPspace is explicitly specified.
## Examples
### Creating a cluster-scoped service policy
The following output displays the response when creating a service policy with a scope of "cluster" and an IPspace of "Default".
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpServicePolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpServicePolicy()
    resource.name = "new-policy"
    resource.scope = "cluster"
    resource.ipspace = {"name": "Default"}
    resource.services = ["intercluster_core"]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
IpServicePolicy(
    {
        "is_built_in": False,
        "services": ["intercluster_core"],
        "ipspace": {
            "name": "Default",
            "_links": {
                "self": {
                    "href": "/api/network/ipspaces/ba556295-e912-11e9-a1c8-005056a7080e"
                }
            },
            "uuid": "ba556295-e912-11e9-a1c8-005056a7080e",
        },
        "name": "new-policy",
        "uuid": "74139267-f1aa-11e9-b5d7-005056a73e2e",
        "_links": {
            "self": {
                "href": "/api/network/ip/service-policies/74139267-f1aa-11e9-b5d7-005056a73e2e"
            }
        },
        "scope": "cluster",
    }
)

```
</div>
</div>

---
### Creating a cluster-scoped service policy without specifying IPspace
The following output displays the response when creating a service policy with a scope of "cluster" without specifying an IPspace".
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpServicePolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpServicePolicy()
    resource.name = "new-policy"
    resource.scope = "cluster"
    resource.services = ["intercluster_core"]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
IpServicePolicy(
    {
        "is_built_in": False,
        "services": ["intercluster_core"],
        "ipspace": {
            "name": "Default",
            "_links": {
                "self": {
                    "href": "/api/network/ipspaces/ba556295-e912-11e9-a1c8-005056a7080e"
                }
            },
            "uuid": "ba556295-e912-11e9-a1c8-005056a7080e",
        },
        "name": "new-policy",
        "uuid": "74139267-f1aa-11e9-b5d7-005056a73e2e",
        "_links": {
            "self": {
                "href": "/api/network/ip/service-policies/74139267-f1aa-11e9-b5d7-005056a73e2e"
            }
        },
        "scope": "cluster",
    }
)

```
</div>
</div>

---
### Creating a cluster-scoped service policy without specifying scope
The following output displays the response when creating a service policy in the "Default" IPspace without specifying the scope".
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpServicePolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpServicePolicy()
    resource.name = "new-policy2"
    resource.ipspace.name = "Default"
    resource.services = ["intercluster_core"]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example7_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example7_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example7_result" class="try_it_out_content">
```
IpServicePolicy(
    {
        "is_built_in": False,
        "services": ["intercluster_core"],
        "ipspace": {
            "name": "Default",
            "_links": {
                "self": {
                    "href": "/api/network/ipspaces/ba556295-e912-11e9-a1c8-005056a7080e"
                }
            },
            "uuid": "ba556295-e912-11e9-a1c8-005056a7080e",
        },
        "name": "new-policy2",
        "uuid": "59439267-f1aa-11e9-b5d7-005056a73e2e",
        "_links": {
            "self": {
                "href": "/api/network/ip/service-policies/74139267-f1aa-11e9-b5d7-005056a73e2e"
            }
        },
        "scope": "cluster",
    }
)

```
</div>
</div>

---
### Creating an SVM-scoped service policy
The following output displays the response when creating a service policy with a scope of "svm" in the SVM "vs0".
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpServicePolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpServicePolicy()
    resource.name = "new-policy"
    resource.scope = "svm"
    resource.svm = {"name": "vs0"}
    resource.services = ["data-nfs", "data-cifs"]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example8_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example8_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example8_result" class="try_it_out_content">
```
IpServicePolicy(
    {
        "is_built_in": False,
        "services": ["data_nfs", "data_cifs"],
        "ipspace": {
            "name": "Default",
            "_links": {
                "self": {
                    "href": "/api/network/ipspaces/1d3199d2-e906-11e9-a13a-005056a73e2e"
                }
            },
            "uuid": "1d3199d2-e906-11e9-a13a-005056a73e2e",
        },
        "name": "new-policy",
        "uuid": "f3901097-f2c4-11e9-b5d7-005056a73e2e",
        "_links": {
            "self": {
                "href": "/api/network/ip/service-policies/f3901097-f2c4-11e9-b5d7-005056a73e2e"
            }
        },
        "svm": {
            "name": "vs0",
            "_links": {
                "self": {"href": "/api/svm/svms/07df9cee-e912-11e9-a13a-005056a73e2e"}
            },
            "uuid": "07df9cee-e912-11e9-a13a-005056a73e2e",
        },
        "scope": "svm",
    }
)

```
</div>
</div>

---
### Creating an SVM-scoped service policy without specifying scope
The following output displays the response when creating a service policy with a SVM of "vs0" without specifying the scope.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpServicePolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpServicePolicy()
    resource.name = "new-policy"
    resource.svm = {"name": "vs0"}
    resource.services = ["data-nfs", "data-cifs"]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example9_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example9_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example9_result" class="try_it_out_content">
```
IpServicePolicy(
    {
        "is_built_in": False,
        "services": ["data_nfs", "data_cifs"],
        "ipspace": {
            "name": "Default",
            "_links": {
                "self": {
                    "href": "/api/network/ipspaces/1d3199d2-e906-11e9-a13a-005056a73e2e"
                }
            },
            "uuid": "1d3199d2-e906-11e9-a13a-005056a73e2e",
        },
        "name": "new-policy",
        "uuid": "f3901097-f2c4-11e9-b5d7-005056a73e2e",
        "_links": {
            "self": {
                "href": "/api/network/ip/service-policies/f3901097-f2c4-11e9-b5d7-005056a73e2e"
            }
        },
        "svm": {
            "name": "vs0",
            "_links": {
                "self": {"href": "/api/svm/svms/07df9cee-e912-11e9-a13a-005056a73e2e"}
            },
            "uuid": "07df9cee-e912-11e9-a13a-005056a73e2e",
        },
        "scope": "svm",
    }
)

```
</div>
</div>

---
### Updating the name of a service policy
The following example displays the command used to update the name of a service policy scoped to a specific "svm". The system returns an error when there is no
service policy associated with the UUID or the service policy cannot be renamed.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpServicePolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpServicePolicy(uuid="734eaf57-d2fe-11e9-9284-005056acaad4")
    resource.name = "new-name"
    resource.patch()

```

---
### Updating the services for a service policy
The following example displays the command used to update the services a service policy contains.
The specified services replace the existing services. To retain existing services, they must be included in the PATCH request.
The system returns an error when there is no
service policy associated with the UUID or the services cannot be applied.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpServicePolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpServicePolicy(uuid="734eaf57-d2fe-11e9-9284-005056acaad4")
    resource.services = ["data-nfs", "data-cifs"]
    resource.patch()

```

---
### Deleting a service policy
The following output displays the response for deleting a service policy.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpServicePolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpServicePolicy(uuid="757ed726-bdc1-11e9-8a92-005056a7bf25")
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


__all__ = ["IpServicePolicy", "IpServicePolicySchema"]
__pdoc__ = {
    "IpServicePolicySchema.resource": False,
    "IpServicePolicySchema.opts": False,
}


class IpServicePolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IpServicePolicy object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the ip_service_policy."""

    ipspace = marshmallow_fields.Nested("netapp_ontap.resources.ipspace.IpspaceSchema", data_key="ipspace", unknown=EXCLUDE, allow_none=True)
    r""" The ipspace field of the ip_service_policy."""

    is_built_in = marshmallow_fields.Boolean(
        data_key="is_built_in",
        allow_none=True,
    )
    r""" The is_built_in field of the ip_service_policy."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The name field of the ip_service_policy.

Example: default-intercluster"""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['svm', 'cluster']),
        allow_none=True,
    )
    r""" Set to "svm" for interfaces owned by an SVM. Otherwise, set to "cluster".

Valid choices:

* svm
* cluster"""

    services = marshmallow_fields.List(marshmallow_fields.Str, data_key="services", allow_none=True)
    r""" The services field of the ip_service_policy."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the ip_service_policy."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The uuid field of the ip_service_policy.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return IpServicePolicy

    gettable_fields = [
        "links",
        "ipspace.links",
        "ipspace.name",
        "ipspace.uuid",
        "is_built_in",
        "name",
        "scope",
        "services",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """links,ipspace.links,ipspace.name,ipspace.uuid,is_built_in,name,scope,services,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
        "name",
        "services",
    ]
    """name,services,"""

    postable_fields = [
        "ipspace.name",
        "ipspace.uuid",
        "name",
        "scope",
        "services",
        "svm.name",
        "svm.uuid",
    ]
    """ipspace.name,ipspace.uuid,name,scope,services,svm.name,svm.uuid,"""

class IpServicePolicy(Resource):
    """Allows interaction with IpServicePolicy objects on the host"""

    _schema = IpServicePolicySchema
    _path = "/api/network/ip/service-policies"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of service policies.
### Related ONTAP commands
* `network interface service-policy show`

### Learn more
* [`DOC /network/ip/service-policies`](#docs-networking-network_ip_service-policies)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all IpServicePolicy resources that match the provided query"""
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
        """Returns a list of RawResources that represent IpServicePolicy resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["IpServicePolicy"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a service policy for network interfaces.
### Related ONTAP commands
* `network interface service-policy add-service`
* `network interface service-policy modify-service`
* `network interface service-policy remove-service`
* `network interface service-policy rename`

### Learn more
* [`DOC /network/ip/service-policies`](#docs-networking-network_ip_service-policies)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["IpServicePolicy"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["IpServicePolicy"], NetAppResponse]:
        r"""Creates a service policy for network interfaces.
### Related ONTAP commands
* `network interface service-policy create`
### Required properties
* `name` - Name of the service policy to create.
* `ipspace.name` or `ipspace.uuid`
  * Required for cluster-scoped service policies.
  * Optional for SVM-scoped service policies.
* `svm.name` or `svm.uuid`
  * Required for SVM-scoped service policies.
  * Not valid for cluster-scoped service policies.
### Default property values
If not specified in POST, the following default property values are assigned:
* `scope`
  * svm if the svm parameter is specified
  * cluster if the svm parameter is not specified

### Learn more
* [`DOC /network/ip/service-policies`](#docs-networking-network_ip_service-policies)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["IpServicePolicy"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a service policy for network interfaces.
### Related ONTAP commands
* `network interface service-policy delete`

### Learn more
* [`DOC /network/ip/service-policies`](#docs-networking-network_ip_service-policies)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of service policies.
### Related ONTAP commands
* `network interface service-policy show`

### Learn more
* [`DOC /network/ip/service-policies`](#docs-networking-network_ip_service-policies)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific service policy.
### Related ONTAP commands
* `network interface service-policy show`

### Learn more
* [`DOC /network/ip/service-policies`](#docs-networking-network_ip_service-policies)"""
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
        r"""Creates a service policy for network interfaces.
### Related ONTAP commands
* `network interface service-policy create`
### Required properties
* `name` - Name of the service policy to create.
* `ipspace.name` or `ipspace.uuid`
  * Required for cluster-scoped service policies.
  * Optional for SVM-scoped service policies.
* `svm.name` or `svm.uuid`
  * Required for SVM-scoped service policies.
  * Not valid for cluster-scoped service policies.
### Default property values
If not specified in POST, the following default property values are assigned:
* `scope`
  * svm if the svm parameter is specified
  * cluster if the svm parameter is not specified

### Learn more
* [`DOC /network/ip/service-policies`](#docs-networking-network_ip_service-policies)"""
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
        r"""Updates a service policy for network interfaces.
### Related ONTAP commands
* `network interface service-policy add-service`
* `network interface service-policy modify-service`
* `network interface service-policy remove-service`
* `network interface service-policy rename`

### Learn more
* [`DOC /network/ip/service-policies`](#docs-networking-network_ip_service-policies)"""
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
        r"""Deletes a service policy for network interfaces.
### Related ONTAP commands
* `network interface service-policy delete`

### Learn more
* [`DOC /network/ip/service-policies`](#docs-networking-network_ip_service-policies)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


