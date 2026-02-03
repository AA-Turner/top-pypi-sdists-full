r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
A role can comprise of multiple tuples and each tuple consists of a REST API path or command/command directory path and its access level. If the tuple refers to a command/command directory path, it may optionally be associated with a query. These APIs can be used to retrieve or modify the associated access level and optional query. They can also be used to delete one of the constituent REST API paths or command/command directory paths within a role. The REST API path can be a resource-qualified endpoint. Currently, the only supported resource-qualified endpoints are the following&#58;<p/>
### Snapshots APIs

* <i>/api/storage/volumes/{volume.uuid}/snapshots</i><br/>
### File System Analytics APIs

* <i>/api/storage/volumes/{volume.uuid}/files</i>
* <i>/api/storage/volumes/{volume.uuid}/top-metrics/clients</i>
*  <i>/api/storage/volumes/{volume.uuid}/top-metrics/directories</i>
* <i>/api/storage/volumes/{volume.uuid}/top-metrics/files</i>
* <i>/api/storage/volumes/{volume.uuid}/top-metrics/users</i>
* <i>/api/svm/svms/{svm.uuid}/top-metrics/clients</i>
* <i>/api/svm/svms/{svm.uuid}/top-metrics/directories</i>
* <i>/api/svm/svms/{svm.uuid}/top-metrics/files</i>
* <i>/api/svm/svms/{svm.uuid}/top-metrics/users</i><br/>
#### ONTAP S3 APIs

* <i>/api/protocols/s3/services/{svm.uuid}/users</i><br/>
<personalities supports=aiml>
#### Artificial Intelligence Data Engine (AIDE) APIs
##### Data Compute Node (DCN) APIs

* <i>/api/dcn/cluster/nodes/{node.uuid}/metrics</i>
* <i>/api/dcn/network/ports/{port.uuid}/metrics</i><br/>
##### Data-Engine APIs

* <i>/api/data-engine/policies/{policy.uuid}/versions</i>
* <i>/api/data-engine/workspaces/{workspace.uuid}/acls</i>
* <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections</i>
* <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/acls</i>
* <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{entity.uuid}/entities</i>
* <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/search</i>
* <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/versions</i>
* <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/versions/{version.uuid}/diffs</i>
* <i>/api/data-engine/workspaces/{workspace.uuid}/data-sources</i>
* <i>/api/data-engine/workspaces/{workspace.uuid}/entities</i>
* <i>/api/data-engine/workspaces/{workspace.uuid}/entities/{entity.uuid}/custom-attributes</i>
* <i>/api/data-engine/workspaces/{workspace.uuid}/queries</i>
* <i>/api/data-engine/workspaces/{workspace.uuid}/queries/{query.uuid}/entities</i>
* <i>/api/data-engine/workspaces/{workspace.uuid}/versions</i>
* <i>/api/data-engine/workspaces/{workspace.uuid}/versions/{version.uuid}/diffs</i><br/>
When used in the context of data collection APIs, <i>{version.uuid}</i> refers to a data collection version. In the context of workspace APIs, it refers to a workspace version.<br/>
</personalities>
In the APIs above, and in the context of REST roles, the wildcard character &#42; can be used in place of <i>{volume.uuid}</i> or <i>{svm.uuid}</i> to represent <i>all</i> volumes or <i>all</i> SVMs, depending on whether the REST endpoint references volumes or SVMs. The <i>{volume.uuid}</i> corresponds to the <i>-instance-uuid</i> field in the output of the \"volume show\" command at the diagnostic privilege level. It can also be retrieved through the REST endpoint <i>/api/storage/volumes</i>.<br/>
<personalities supports=aiml>
In the AIDE APIs described above, and in the context of REST roles, the wildcard character &#42; can be used in place of variable components in the Uniform Resource Identifier (URI) path, such as <i>{node.uuid}</i>, <i>{port.uuid}</i>, <i>{policy.uuid}</i>, <i>{workspace.uuid}</i>, <i>{datacollection.uuid}</i>, <i>{entity.uuid}</i>, <i>{version.uuid}</i>, or <i>{query.uuid}</i>. The specific variable to be replaced depends on whether the REST endpoint references nodes, ports, policies, workspaces, data collections, entities, versions, or queries.<br/>
However, when using the wildcard character &#42; in place of a variable component in a URI path, it must replace <b>all</b> variable components in that path. Mixing wildcards and specific values for different variable components within the same URI path is not supported in REST roles. For example, a URI path such as <i>/api/data-engine/workspaces/c6e1b325-4125-11f0-abb5-bc2411f6fd43/data-collections/*/search</i> is not supported.<br/>
In summary, only the following two types of resource-qualified endpoints are supported in a REST role:
<ul>
  <li>All variable components in the URI path are specific values. Example: <i>/api/data-engine/workspaces/c6e1b325-4125-11f0-abb5-bc2411f6fd43/data-collections/b09b6d25-4126-11f0-abb5-bc2411f6fd43/search</i></li>
  <li>All variable components in the URI path are wildcards. Example: <i>/api/data-engine/workspaces/*/data-collections/*/search</i></li>
</ul><br/>
AIDE APIs are supported only in cluster-scoped REST roles, not in SVM-scoped REST roles.<br/>
</personalities>
The role can be SVM-scoped or cluster-scoped.<p/>
Specify the owner UUID and the role name in the URI path. The owner UUID corresponds to the UUID of the SVM for which the role has been created and can be obtained from the response body of a GET request performed on one of the following APIs&#58;
<i>/api/security/roles</i> for all roles
<i>/api/security/roles/?scope=svm</i> for SVM-scoped roles
<i>/api/security/roles/?owner.name=<svm-name></i> for roles in a specific SVM
This API response contains the complete URI for each tuple of the role and can be used for GET, PATCH, or DELETE operations.<p/>
Note: The access level for paths in pre-defined roles cannot be updated.
<br/>
## Examples
### Updating the access level for a REST API path in the privilege tuple of an existing role
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import RolePrivilege

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = RolePrivilege(
        "aaef7c38-4bd3-11e9-b238-0050568e2e25", "svm_role1", path="/api/protocols"
    )
    resource.access = "all"
    resource.patch()

```

### Updating the access level for a command/command directory path in the privilege tuple of an existing role
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import RolePrivilege

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = RolePrivilege(
        "aaef7c38-4bd3-11e9-b238-0050568e2e25", "svm_role1", path="netp port"
    )
    resource.access = "readonly"
    resource.query = "-type if-group|vlan"
    resource.patch()

```

### Updating the access level for a resource-qualified endpoint in the privilege tuple of an existing role
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import RolePrivilege

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = RolePrivilege(
        "aaef7c38-4bd3-11e9-b238-0050568e2e25",
        "svm_role1",
        path="/api/storage/volumes/742ef001-24f0-4d5a-9ec1-2fdaadb282f4/files",
    )
    resource.access = "readonly"
    resource.patch()

```

<personalities supports=aiml>
### Updating the access level for an AIDE resource-qualified endpoint in the privilege tuple of an existing role
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import RolePrivilege

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = RolePrivilege(
        "aaef7c38-4bd3-11e9-b238-0050568e2e25",
        "cluster_role1",
        path="/api/data-engine/policies/*/versions",
    )
    resource.access = "readonly"
    resource.patch()

```

</personalities>
### Retrieving the access level for a REST API path in the privilege tuple of an existing role
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import RolePrivilege

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = RolePrivilege(
        "aaef7c38-4bd3-11e9-b238-0050568e2e25", "svm_role1", path="/api/protocols"
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
RolePrivilege(
    {
        "access": "all",
        "_links": {
            "self": {
                "href": "/api/security/roles/aaef7c38-4bd3-11e9-b238-0050568e2e25/svm_role1/privileges/%2Fapi%2Fprotocols"
            }
        },
        "path": "/api/protocols",
    }
)

```
</div>
</div>

### Retrieving the access level for a command/command directory path in the privilege tuple of an existing role
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import RolePrivilege

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = RolePrivilege(
        "aaef7c38-4bd3-11e9-b238-0050568e2e25", "svm_role1", path="net port"
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
RolePrivilege(
    {
        "query": "-type if-group|vlan",
        "access": "readonly",
        "_links": {
            "self": {
                "href": "/api/security/roles/aaef7c38-4bd3-11e9-b238-0050568e2e25/svm_role1/privileges/net%20port"
            }
        },
        "path": "net port",
    }
)

```
</div>
</div>

### Retrieving the access level for a resource-qualified endpoint in the privilege tuple of an existing role
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import RolePrivilege

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = RolePrivilege(
        "aaef7c38-4bd3-11e9-b238-0050568e2e25",
        "svm_role1",
        path="/api/storage/volumes/d0f3b91a-4ce7-4de4-afb9-7eda668659dd//snapshots",
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
RolePrivilege(
    {
        "access": "all",
        "_links": {
            "self": {
                "href": "/api/security/roles/aaef7c38-4bd3-11e9-b238-0050568e2e25/svm_role1/privileges/%2Fapi%2Fstorage%2Fvolumes%2Fd0f3b91a-4ce7-4de4-afb9-7eda668659dd%2Fsnapshots"
            }
        },
        "path": "/api/storage/volumes/d0f3b91a-4ce7-4de4-afb9-7eda668659dd/snapshots",
    }
)

```
</div>
</div>

<personalities supports=aiml>
### Retrieving the access level for an AIDE resource-qualified endpoint in the privilege tuple of an existing role
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import RolePrivilege

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = RolePrivilege(
        "223e4567-e89b-12d3-a456-426614174000",
        "cluster_role1",
        path="/api/data-engine/workspaces/d0f3b91a-4ce7-4de4-afb9-7eda668659dd/entities",
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example7_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example7_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example7_result" class="try_it_out_content">
```
RolePrivilege(
    {
        "access": "readonly",
        "_links": {
            "self": {
                "href": "/api/security/roles/223e4567-e89b-12d3-a456-426614174000/cluster_role1/privileges/%2Fapi%2Fdata-engine%2Fworkspaces%2Fd0f3b91a-4ce7-4de4-afb9-7eda668659dd%2Fentities"
            }
        },
        "path": "/api/data-engine/workspaces/d0f3b91a-4ce7-4de4-afb9-7eda668659dd/entities",
    }
)

```
</div>
</div>

</personalities>
### Deleting a privilege tuple, containing a REST API path, from an existing role
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import RolePrivilege

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = RolePrivilege(
        "aaef7c38-4bd3-11e9-b238-0050568e2e25", "svm_role1", path="/api/protocols"
    )
    resource.delete()

```

### Deleting a privilege tuple, containing a command/command directory path, from an existing role
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import RolePrivilege

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = RolePrivilege(
        "aaef7c38-4bd3-11e9-b238-0050568e2e25", "svm_role1", path="net port"
    )
    resource.delete()

```

### Deleting a privilege tuple, containing a resource-qualified endpoint, from an existing role
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import RolePrivilege

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = RolePrivilege(
        "aaef7c38-4bd3-11e9-b238-0050568e2e25",
        "svm_role1",
        path="/api/storage/svm/6e000659-9a16-11ec-819e-005056bb1a7c/top-metrics/files",
    )
    resource.delete()

```

<personalities supports=aiml>
### Deleting a privilege tuple, containing an AIDE resource-qualified endpoint, from an existing role
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import RolePrivilege

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = RolePrivilege(
        "a6786ae5-93a0-411c-bcfd-16c53ecff612",
        "cluster_role1",
        path="/api/dcn/network/ports/91796b96-5207-4d0b-93fb-7a2062b8358e/metrics",
    )
    resource.delete()

```

</personalities>"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union
from marshmallow import fields as marshmallow_fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["RolePrivilege", "RolePrivilegeSchema"]
__pdoc__ = {
    "RolePrivilegeSchema.resource": False,
    "RolePrivilegeSchema.opts": False,
}

class RolePrivilegeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the RolePrivilege object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the role_privilege."""

    access = marshmallow_fields.Str(
        data_key="access",
        allow_none=True,
    )
    r""" The access field of the role_privilege."""

    path = marshmallow_fields.Str(
        data_key="path",
        allow_none=True,
    )
    r""" Either of REST URI/endpoint OR command/command directory path.

Example: volume move start"""

    query = marshmallow_fields.Str(
        data_key="query",
        allow_none=True,
    )
    r""" Optional attribute that can be specified only if the "path" attribute refers to a command/command directory path. The privilege tuple implicitly defines a set of objects the role can or cannot access at the specified access level. The query further reduces this set of objects to a subset of objects that the role is allowed to access. The query attribute must be applicable to the command/command directory specified by the "path" attribute. It is defined using one or more parameters of the command/command directory path specified by the "path" attribute.

Example: -vserver vs1|vs2|vs3 -destination-aggregate aggr1|aggr2"""

    @property
    def resource(self):
        return RolePrivilege

    gettable_fields = [
        "links",
        "access",
        "path",
        "query",
    ]
    """links,access,path,query,"""

    patchable_fields = [
        "access",
        "query",
    ]
    """access,query,"""

    postable_fields = [
        "access",
        "path",
        "query",
    ]
    """access,path,query,"""

class RolePrivilege(Resource):
    r""" A tuple containing a REST endpoint or a command/command directory path and the access level assigned to that endpoint or command/command directory. If the "path" attribute refers to a command/command directory path, the tuple could additionally contain an optional query. The REST endpoint can be a resource-qualified endpoint. At present, the only supported resource-qualified endpoints are the following<br/>
Snapshots APIs<br/><ul>
<li><i>/api/storage/volumes/{volume.uuid}/snapshots</i></li></ul><br/>
File System Analytics APIs<br/><ul>
<li><i>/api/storage/volumes/{volume.uuid}/files</i></li>
<li><i>/api/storage/volumes/{volume.uuid}/top-metrics/clients</i></li>
<li><i>/api/storage/volumes/{volume.uuid}/top-metrics/directories</i></li>
<li><i>/api/storage/volumes/{volume.uuid}/top-metrics/files</i></li>
<li><i>/api/storage/volumes/{volume.uuid}/top-metrics/users</i></li>
<li><i>/api/svm/svms/{svm.uuid}/top-metrics/clients</i></li>
<li><i>/api/svm/svms/{svm.uuid}/top-metrics/directories</i></li>
<li><i>/api/svm/svms/{svm.uuid}/top-metrics/files</i></li>
<li><i>/api/svm/svms/{svm.uuid}/top-metrics/users</i></li>
<li><i>/api/protocols/s3/services/{svm.uuid}/users</i></li><br/></ul><br/>
In the above APIs, wildcard character &#42; could be used in place of <i>{volume.uuid}</i> or <i>{svm.uuid}</i> to denote <i>all</i> volumes or <i>all</i> SVMs, depending upon whether the REST endpoint references volumes or SVMs. The <i>{volume.uuid}</i> refers to the <i>-instance-uuid</i> field value in the \"volume show\" command output at diagnostic privilege level. It can also be fetched through REST endpoint <i>/api/storage/volumes</i>. """

    _schema = RolePrivilegeSchema
    _path = "/api/security/roles/{owner[uuid]}/{role[name]}/privileges"
    _keys = ["owner.uuid", "role.name", "path"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves privilege details of the specified role.
### Related ONTAP commands
* `security login rest-role show`
* `security login role show`
### Learn more
* [`DOC /security/roles/{owner.uuid}/{name}/privileges`](#docs-security-security_roles_{owner.uuid}_{name}_privileges)
* [`DOC /security/roles`](#docs-security-security_roles)
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
        """Returns a count of all RolePrivilege resources that match the provided query"""
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
        """Returns a list of RawResources that represent RolePrivilege resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["RolePrivilege"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the access level for a REST API path or command/command directory path. Optionally updates the query, if 'path' refers to a command/command directory path. The REST API path can be a resource-qualified endpoint. Currently, the only supported resource-qualified endpoints are the following&#58;<p/>
### Snapshots APIs
&ndash; <i>/api/storage/volumes/{volume.uuid}/snapshots</i><br/>
### File System Analytics APIs
&ndash; <i>/api/storage/volumes/{volume.uuid}/files</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/clients</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/directories</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/files</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/users</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/clients</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/directories</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/files</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/users</i><br/>
#### ONTAP S3 APIs
&ndash; <i>/api/protocols/s3/services/{svm.uuid}/users</i><br/>
<personalities supports=aiml>
#### Artificial Intelligence Data Engine (AIDE) APIs
##### Data Compute Node (DCN) APIs
&ndash; <i>/api/dcn/cluster/nodes/{node.uuid}/metrics</i>
&ndash; <i>/api/dcn/network/ports/{port.uuid}/metrics</i><br/>
##### Data-Engine APIs
&ndash; <i>/api/data-engine/policies/{policy.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/acls</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/acls</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{entity.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/search</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/versions/{version.uuid}/diffs</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-sources</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/entities/{entity.uuid}/custom-attributes</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/queries</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/queries/{query.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/versions/{version.uuid}/diffs</i><br/>
When used in the context of data collection APIs, <i>{version.uuid}</i> refers to a data collection version. In the context of workspace APIs, it refers to a workspace version.<br/>
</personalities>
In the APIs above, and in the context of REST roles, the wildcard character &#42; can be used in place of <i>{volume.uuid}</i> or <i>{svm.uuid}</i> to represent <i>all</i> volumes or <i>all</i> SVMs, depending on whether the REST endpoint references volumes or SVMs. The <i>{volume.uuid}</i> corresponds to the <i>-instance-uuid</i> field in the output of the \"volume show\" command at the diagnostic privilege level. It can also be retrieved through the REST endpoint <i>/api/storage/volumes</i>.<br/>
<personalities supports=aiml>
In the AIDE APIs described above, and in the context of REST roles, the wildcard character &#42; can be used in place of variable components in the Uniform Resource Identifier (URI) path, such as <i>{node.uuid}</i>, <i>{port.uuid}</i>, <i>{policy.uuid}</i>, <i>{workspace.uuid}</i>, <i>{datacollection.uuid}</i>, <i>{entity.uuid}</i>, <i>{version.uuid}</i>, or <i>{query.uuid}</i>. The specific variable to be replaced depends on whether the REST endpoint references nodes, ports, policies, workspaces, data collections, entities, versions, or queries.<br/>
However, when using the wildcard character &#42; in place of a variable component in a URI path, it must replace <b>all</b> variable components in that path. Mixing wildcards and specific values for different variable components within the same URI path is not supported in REST roles. For example, a URI path such as <i>/api/data-engine/workspaces/c6e1b325-4125-11f0-abb5-bc2411f6fd43/data-collections/*/search</i> is not supported.<br/>
In summary, only the following two types of resource-qualified endpoints are supported in a REST role:
<ul>
  <li>All variable components in the URI path are specific values. Example: <i>/api/data-engine/workspaces/c6e1b325-4125-11f0-abb5-bc2411f6fd43/data-collections/b09b6d25-4126-11f0-abb5-bc2411f6fd43/search</i></li>
  <li>All variable components in the URI path are wildcards. Example: <i>/api/data-engine/workspaces/*/data-collections/*/search</i></li>
</ul><br/>
AIDE APIs are supported only in cluster-scoped REST roles, not in SVM-scoped REST roles.<br/>
</personalities>
### Required parameters
* `owner.uuid` - UUID of the SVM that houses this role.
* `name` - Name of the role to be updated.
* `path` - Constituent REST API path or command/command directory path, whose access level and/or query are/is to be updated. Can be a resource-qualified endpoint (example: <i>/api/storage/volumes/43256a71-be02-474d-a2a9-9642e12a6a2c/snapshots</i>). Currently, resource-qualified endpoints are limited to the <i>Snapshots</i>, <i>File System Analytics</i><personalities supports=aiml><i>, Artificial Intelligence Data Engine (AIDE)</i></personalities> and <i>ONTAP S3</i> endpoints listed above in the description.
### Optional parameters
* `access` - Access level for the path.
* `query` - Optional query, if the path refers to a command/command directory path.
### Related ONTAP commands
* `security login rest-role modify`
* `security login role modify`
### Learn more
* [`DOC /security/roles/{owner.uuid}/{name}/privileges/{path}`](#docs-security-security_roles_{owner.uuid}_{name}_privileges_{path})
* [`DOC /security/roles`](#docs-security-security_roles)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["RolePrivilege"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["RolePrivilege"], NetAppResponse]:
        r"""Adds a privilege tuple (of REST URI or command/command directory path, its access level and an optional query, if the "path" refers to a command/command directory path) to an existing role or creates a new role with the provided tuple.
### Required parameters
* `owner.uuid` - UUID of the SVM that houses this role.
* `name` - Name of the role to be updated.
* `path` - REST URI path (example: <i>/api/storage/volumes</i>) or command/command directory path (example: <i>snaplock compliance-clock</i>). Can be a resource-qualified endpoint (example: <i>/api/storage/volumes/43256a71-be02-474d-a2a9-9642e12a6a2c/snapshots</i>). Currently, resource-qualified endpoints are limited to the following&#58;
#### Snapshots APIs
&ndash; <i>/api/storage/volumes/{volume.uuid}/snapshots</i><br/>
#### File System Analytics APIs
&ndash; <i>/api/storage/volumes/{volume.uuid}/files</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/clients</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/directories</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/files</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/users</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/clients</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/directories</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/files</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/users</i><br/>
<personalities supports=aiml>
#### Artificial Intelligence Data Engine (AIDE) APIs
##### Data Compute Node (DCN) APIs
&ndash; <i>/api/dcn/cluster/nodes/{node.uuid}/metrics</i>
&ndash; <i>/api/dcn/network/ports/{port.uuid}/metrics</i><br/>
##### Data-Engine APIs
&ndash; <i>/api/data-engine/policies/{policy.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/acls</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/acls</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{entity.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/search</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/versions/{version.uuid}/diffs</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-sources</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/entities/{entity.uuid}/custom-attributes</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/queries</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/queries/{query.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/versions/{version.uuid}/diffs</i><br/>
When used in the context of data collection APIs, <i>{version.uuid}</i> refers to a data collection version. In the context of workspace APIs, it refers to a workspace version.<br/>
</personalities>
In the APIs above, and in the context of REST roles, the wildcard character &#42; can be used in place of <i>{volume.uuid}</i> or <i>{svm.uuid}</i> to represent <i>all</i> volumes or <i>all</i> SVMs, depending on whether the REST endpoint references volumes or SVMs. The <i>{volume.uuid}</i> corresponds to the <i>-instance-uuid</i> field in the output of the \"volume show\" command at the diagnostic privilege level. It can also be retrieved through the REST endpoint <i>/api/storage/volumes</i>.<br/>
<personalities supports=aiml>
In the AIDE APIs described above, and in the context of REST roles, the wildcard character &#42; can be used in place of variable components in the Uniform Resource Identifier (URI) path, such as <i>{node.uuid}</i>, <i>{port.uuid}</i>, <i>{policy.uuid}</i>, <i>{workspace.uuid}</i>, <i>{datacollection.uuid}</i>, <i>{entity.uuid}</i>, <i>{version.uuid}</i>, or <i>{query.uuid}</i>. The specific variable to be replaced depends on whether the REST endpoint references nodes, ports, policies, workspaces, data collections, entities, versions, or queries.<br/>
However, when using the wildcard character &#42; in place of a variable component in a URI path, it must replace <b>all</b> variable components in that path. Mixing wildcards and specific values for different variable components within the same URI path is not supported in REST roles. For example, a URI path such as <i>/api/data-engine/workspaces/c6e1b325-4125-11f0-abb5-bc2411f6fd43/data-collections/*/search</i> is not supported.<br/>
In summary, only the following two types of resource-qualified endpoints are supported in a REST role:
<ul>
  <li>All variable components in the URI path are specific values. Example: <i>/api/data-engine/workspaces/c6e1b325-4125-11f0-abb5-bc2411f6fd43/data-collections/b09b6d25-4126-11f0-abb5-bc2411f6fd43/search</i></li>
  <li>All variable components in the URI path are wildcards. Example: <i>/api/data-engine/workspaces/*/data-collections/*/search</i></li>
</ul><br/>
AIDE APIs are supported only in cluster-scoped REST roles, not in SVM-scoped REST roles.<br/>
</personalities>
* `access` - Desired access level for the REST URI path or command/command directory.
### Related ONTAP commands
* `security login rest-role create`
* `security login role create`
### Learn more
* [`DOC /security/roles/{owner.uuid}/{name}/privileges`](#docs-security-security_roles_{owner.uuid}_{name}_privileges)
* [`DOC /security/roles`](#docs-security-security_roles)
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
        records: Iterable["RolePrivilege"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a privilege tuple (of REST URI or command/command directory path, its access level and an optional query) from the role. The REST URI can be a resource-qualified endpoint. Currently, the only supported resource-qualified endpoints are the following&#58;<p/>
### Snapshots APIs
&ndash; <i>/api/storage/volumes/{volume.uuid}/snapshots</i><br/>
### File System Analytics APIs
&ndash; <i>/api/storage/volumes/{volume.uuid}/files</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/clients</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/directories</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/files</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/users</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/clients</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/directories</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/files</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/users</i><br/>
#### ONTAP S3 APIs
&ndash; <i>/api/protocols/s3/services/{svm.uuid}/users</i><br/>
<personalities supports=aiml>
#### Artificial Intelligence Data Engine (AIDE) APIs
##### Data Compute Node (DCN) APIs
&ndash; <i>/api/dcn/cluster/nodes/{node.uuid}/metrics</i>
&ndash; <i>/api/dcn/network/ports/{port.uuid}/metrics</i><br/>
##### Data-Engine APIs
&ndash; <i>/api/data-engine/policies/{policy.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/acls</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/acls</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{entity.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/search</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/versions/{version.uuid}/diffs</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-sources</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/entities/{entity.uuid}/custom-attributes</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/queries</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/queries/{query.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/versions/{version.uuid}/diffs</i><br/>
When used in the context of data collection APIs, <i>{version.uuid}</i> refers to a data collection version. In the context of workspace APIs, it refers to a workspace version.<br/>
</personalities>
In the APIs above, and in the context of REST roles, the wildcard character &#42; can be used in place of <i>{volume.uuid}</i> or <i>{svm.uuid}</i> to represent <i>all</i> volumes or <i>all</i> SVMs, depending on whether the REST endpoint references volumes or SVMs. The <i>{volume.uuid}</i> corresponds to the <i>-instance-uuid</i> field in the output of the \"volume show\" command at the diagnostic privilege level. It can also be retrieved through the REST endpoint <i>/api/storage/volumes</i>.<br/>
<personalities supports=aiml>
In the AIDE APIs described above, and in the context of REST roles, the wildcard character &#42; can be used in place of variable components in the Uniform Resource Identifier (URI) path, such as <i>{node.uuid}</i>, <i>{port.uuid}</i>, <i>{policy.uuid}</i>, <i>{workspace.uuid}</i>, <i>{datacollection.uuid}</i>, <i>{entity.uuid}</i>, <i>{version.uuid}</i>, or <i>{query.uuid}</i>. The specific variable to be replaced depends on whether the REST endpoint references nodes, ports, policies, workspaces, data collections, entities, versions, or queries.<br/>
However, when using the wildcard character &#42; in place of a variable component in a URI path, it must replace <b>all</b> variable components in that path. Mixing wildcards and specific values for different variable components within the same URI path is not supported in REST roles. For example, a URI path such as <i>/api/data-engine/workspaces/c6e1b325-4125-11f0-abb5-bc2411f6fd43/data-collections/*/search</i> is not supported.<br/>
In summary, only the following two types of resource-qualified endpoints are supported in a REST role:
<ul>
  <li>All variable components in the URI path are specific values. Example: <i>/api/data-engine/workspaces/c6e1b325-4125-11f0-abb5-bc2411f6fd43/data-collections/b09b6d25-4126-11f0-abb5-bc2411f6fd43/search</i></li>
  <li>All variable components in the URI path are wildcards. Example: <i>/api/data-engine/workspaces/*/data-collections/*/search</i></li>
</ul><br/>
AIDE APIs are supported only in cluster-scoped REST roles, not in SVM-scoped REST roles.<br/>
</personalities>
### Required parameters
* `owner.uuid` - UUID of the SVM which houses this role.
* `name` - Name of the role to be updated.
* `path` - Constituent REST API path or command/command directory path to be deleted from this role. Can be a resource-qualified endpoint (example: <i>/api/svm/svms/43256a71-be02-474d-a2a9-9642e12a6a2c/top-metrics/users</i>). Currently, resource-qualified endpoints are limited to the <i>Snapshots</i>, <i>File System Analytics</i><personalities supports=aiml><i>, Artificial Intelligence Data Engine (AIDE)</i></personalities> and <i>ONTAP S3</i> endpoints listed above in the description.
### Related ONTAP commands
* `security login rest-role delete`
* `security login role delete`
### Learn more
* [`DOC /security/roles/{owner.uuid}/{name}/privileges/{path}`](#docs-security-security_roles_{owner.uuid}_{name}_privileges_{path})
* [`DOC /security/roles`](#docs-security-security_roles)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves privilege details of the specified role.
### Related ONTAP commands
* `security login rest-role show`
* `security login role show`
### Learn more
* [`DOC /security/roles/{owner.uuid}/{name}/privileges`](#docs-security-security_roles_{owner.uuid}_{name}_privileges)
* [`DOC /security/roles`](#docs-security-security_roles)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the access level for a REST API path or command/command directory path for the specified role. Optionally retrieves the query, if 'path' refers to a command/command directory path. The REST API path can be a resource-qualified endpoint. Currently, the only supported resource-qualified endpoints are the following&#58;<p/>
### Snapshots APIs
&ndash; <i>/api/storage/volumes/{volume.uuid}/snapshots</i><br/>
### File System Analytics APIs
&ndash; <i>/api/storage/volumes/{volume.uuid}/files</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/clients</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/directories</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/files</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/users</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/clients</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/directories</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/files</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/users</i><br/>
#### ONTAP S3 APIs
&ndash; <i>/api/protocols/s3/services/{svm.uuid}/users</i><br/>
<personalities supports=aiml>
#### Artificial Intelligence Data Engine (AIDE) APIs
##### Data Compute Node (DCN) APIs
&ndash; <i>/api/dcn/cluster/nodes/{node.uuid}/metrics</i>
&ndash; <i>/api/dcn/network/ports/{port.uuid}/metrics</i><br/>
##### Data-Engine APIs
&ndash; <i>/api/data-engine/policies/{policy.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/acls</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/acls</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{entity.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/search</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/versions/{version.uuid}/diffs</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-sources</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/entities/{entity.uuid}/custom-attributes</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/queries</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/queries/{query.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/versions/{version.uuid}/diffs</i><br/>
When used in the context of data collection APIs, <i>{version.uuid}</i> refers to a data collection version. In the context of workspace APIs, it refers to a workspace version.<br/>
</personalities>
In the APIs above, and in the context of REST roles, the wildcard character &#42; can be used in place of <i>{volume.uuid}</i> or <i>{svm.uuid}</i> to represent <i>all</i> volumes or <i>all</i> SVMs, depending on whether the REST endpoint references volumes or SVMs. The <i>{volume.uuid}</i> corresponds to the <i>-instance-uuid</i> field in the output of the \"volume show\" command at the diagnostic privilege level. It can also be retrieved through the REST endpoint <i>/api/storage/volumes</i>.<br/>
<personalities supports=aiml>
In the AIDE APIs described above, and in the context of REST roles, the wildcard character &#42; can be used in place of variable components in the Uniform Resource Identifier (URI) path, such as <i>{node.uuid}</i>, <i>{port.uuid}</i>, <i>{policy.uuid}</i>, <i>{workspace.uuid}</i>, <i>{datacollection.uuid}</i>, <i>{entity.uuid}</i>, <i>{version.uuid}</i>, or <i>{query.uuid}</i>. The specific variable to be replaced depends on whether the REST endpoint references nodes, ports, policies, workspaces, data collections, entities, versions, or queries.<br/>
However, when using the wildcard character &#42; in place of a variable component in a URI path, it must replace <b>all</b> variable components in that path. Mixing wildcards and specific values for different variable components within the same URI path is not supported in REST roles. For example, a URI path such as <i>/api/data-engine/workspaces/c6e1b325-4125-11f0-abb5-bc2411f6fd43/data-collections/*/search</i> is not supported.<br/>
In summary, only the following two types of resource-qualified endpoints are supported in a REST role:
<ul>
  <li>All variable components in the URI path are specific values. Example: <i>/api/data-engine/workspaces/c6e1b325-4125-11f0-abb5-bc2411f6fd43/data-collections/b09b6d25-4126-11f0-abb5-bc2411f6fd43/search</i></li>
  <li>All variable components in the URI path are wildcards. Example: <i>/api/data-engine/workspaces/*/data-collections/*/search</i></li>
</ul><br/>
AIDE APIs are supported only in cluster-scoped REST roles, not in SVM-scoped REST roles.<br/>
</personalities>
### Related ONTAP commands
* `security login rest-role show`
* `security login role show`
### Learn more
* [`DOC /security/roles/{owner.uuid}/{name}/privileges/{path}`](#docs-security-security_roles_{owner.uuid}_{name}_privileges_{path})
* [`DOC /security/roles`](#docs-security-security_roles)
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
        r"""Adds a privilege tuple (of REST URI or command/command directory path, its access level and an optional query, if the "path" refers to a command/command directory path) to an existing role or creates a new role with the provided tuple.
### Required parameters
* `owner.uuid` - UUID of the SVM that houses this role.
* `name` - Name of the role to be updated.
* `path` - REST URI path (example: <i>/api/storage/volumes</i>) or command/command directory path (example: <i>snaplock compliance-clock</i>). Can be a resource-qualified endpoint (example: <i>/api/storage/volumes/43256a71-be02-474d-a2a9-9642e12a6a2c/snapshots</i>). Currently, resource-qualified endpoints are limited to the following&#58;
#### Snapshots APIs
&ndash; <i>/api/storage/volumes/{volume.uuid}/snapshots</i><br/>
#### File System Analytics APIs
&ndash; <i>/api/storage/volumes/{volume.uuid}/files</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/clients</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/directories</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/files</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/users</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/clients</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/directories</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/files</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/users</i><br/>
<personalities supports=aiml>
#### Artificial Intelligence Data Engine (AIDE) APIs
##### Data Compute Node (DCN) APIs
&ndash; <i>/api/dcn/cluster/nodes/{node.uuid}/metrics</i>
&ndash; <i>/api/dcn/network/ports/{port.uuid}/metrics</i><br/>
##### Data-Engine APIs
&ndash; <i>/api/data-engine/policies/{policy.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/acls</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/acls</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{entity.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/search</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/versions/{version.uuid}/diffs</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-sources</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/entities/{entity.uuid}/custom-attributes</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/queries</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/queries/{query.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/versions/{version.uuid}/diffs</i><br/>
When used in the context of data collection APIs, <i>{version.uuid}</i> refers to a data collection version. In the context of workspace APIs, it refers to a workspace version.<br/>
</personalities>
In the APIs above, and in the context of REST roles, the wildcard character &#42; can be used in place of <i>{volume.uuid}</i> or <i>{svm.uuid}</i> to represent <i>all</i> volumes or <i>all</i> SVMs, depending on whether the REST endpoint references volumes or SVMs. The <i>{volume.uuid}</i> corresponds to the <i>-instance-uuid</i> field in the output of the \"volume show\" command at the diagnostic privilege level. It can also be retrieved through the REST endpoint <i>/api/storage/volumes</i>.<br/>
<personalities supports=aiml>
In the AIDE APIs described above, and in the context of REST roles, the wildcard character &#42; can be used in place of variable components in the Uniform Resource Identifier (URI) path, such as <i>{node.uuid}</i>, <i>{port.uuid}</i>, <i>{policy.uuid}</i>, <i>{workspace.uuid}</i>, <i>{datacollection.uuid}</i>, <i>{entity.uuid}</i>, <i>{version.uuid}</i>, or <i>{query.uuid}</i>. The specific variable to be replaced depends on whether the REST endpoint references nodes, ports, policies, workspaces, data collections, entities, versions, or queries.<br/>
However, when using the wildcard character &#42; in place of a variable component in a URI path, it must replace <b>all</b> variable components in that path. Mixing wildcards and specific values for different variable components within the same URI path is not supported in REST roles. For example, a URI path such as <i>/api/data-engine/workspaces/c6e1b325-4125-11f0-abb5-bc2411f6fd43/data-collections/*/search</i> is not supported.<br/>
In summary, only the following two types of resource-qualified endpoints are supported in a REST role:
<ul>
  <li>All variable components in the URI path are specific values. Example: <i>/api/data-engine/workspaces/c6e1b325-4125-11f0-abb5-bc2411f6fd43/data-collections/b09b6d25-4126-11f0-abb5-bc2411f6fd43/search</i></li>
  <li>All variable components in the URI path are wildcards. Example: <i>/api/data-engine/workspaces/*/data-collections/*/search</i></li>
</ul><br/>
AIDE APIs are supported only in cluster-scoped REST roles, not in SVM-scoped REST roles.<br/>
</personalities>
* `access` - Desired access level for the REST URI path or command/command directory.
### Related ONTAP commands
* `security login rest-role create`
* `security login role create`
### Learn more
* [`DOC /security/roles/{owner.uuid}/{name}/privileges`](#docs-security-security_roles_{owner.uuid}_{name}_privileges)
* [`DOC /security/roles`](#docs-security-security_roles)
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
        r"""Updates the access level for a REST API path or command/command directory path. Optionally updates the query, if 'path' refers to a command/command directory path. The REST API path can be a resource-qualified endpoint. Currently, the only supported resource-qualified endpoints are the following&#58;<p/>
### Snapshots APIs
&ndash; <i>/api/storage/volumes/{volume.uuid}/snapshots</i><br/>
### File System Analytics APIs
&ndash; <i>/api/storage/volumes/{volume.uuid}/files</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/clients</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/directories</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/files</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/users</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/clients</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/directories</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/files</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/users</i><br/>
#### ONTAP S3 APIs
&ndash; <i>/api/protocols/s3/services/{svm.uuid}/users</i><br/>
<personalities supports=aiml>
#### Artificial Intelligence Data Engine (AIDE) APIs
##### Data Compute Node (DCN) APIs
&ndash; <i>/api/dcn/cluster/nodes/{node.uuid}/metrics</i>
&ndash; <i>/api/dcn/network/ports/{port.uuid}/metrics</i><br/>
##### Data-Engine APIs
&ndash; <i>/api/data-engine/policies/{policy.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/acls</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/acls</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{entity.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/search</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/versions/{version.uuid}/diffs</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-sources</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/entities/{entity.uuid}/custom-attributes</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/queries</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/queries/{query.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/versions/{version.uuid}/diffs</i><br/>
When used in the context of data collection APIs, <i>{version.uuid}</i> refers to a data collection version. In the context of workspace APIs, it refers to a workspace version.<br/>
</personalities>
In the APIs above, and in the context of REST roles, the wildcard character &#42; can be used in place of <i>{volume.uuid}</i> or <i>{svm.uuid}</i> to represent <i>all</i> volumes or <i>all</i> SVMs, depending on whether the REST endpoint references volumes or SVMs. The <i>{volume.uuid}</i> corresponds to the <i>-instance-uuid</i> field in the output of the \"volume show\" command at the diagnostic privilege level. It can also be retrieved through the REST endpoint <i>/api/storage/volumes</i>.<br/>
<personalities supports=aiml>
In the AIDE APIs described above, and in the context of REST roles, the wildcard character &#42; can be used in place of variable components in the Uniform Resource Identifier (URI) path, such as <i>{node.uuid}</i>, <i>{port.uuid}</i>, <i>{policy.uuid}</i>, <i>{workspace.uuid}</i>, <i>{datacollection.uuid}</i>, <i>{entity.uuid}</i>, <i>{version.uuid}</i>, or <i>{query.uuid}</i>. The specific variable to be replaced depends on whether the REST endpoint references nodes, ports, policies, workspaces, data collections, entities, versions, or queries.<br/>
However, when using the wildcard character &#42; in place of a variable component in a URI path, it must replace <b>all</b> variable components in that path. Mixing wildcards and specific values for different variable components within the same URI path is not supported in REST roles. For example, a URI path such as <i>/api/data-engine/workspaces/c6e1b325-4125-11f0-abb5-bc2411f6fd43/data-collections/*/search</i> is not supported.<br/>
In summary, only the following two types of resource-qualified endpoints are supported in a REST role:
<ul>
  <li>All variable components in the URI path are specific values. Example: <i>/api/data-engine/workspaces/c6e1b325-4125-11f0-abb5-bc2411f6fd43/data-collections/b09b6d25-4126-11f0-abb5-bc2411f6fd43/search</i></li>
  <li>All variable components in the URI path are wildcards. Example: <i>/api/data-engine/workspaces/*/data-collections/*/search</i></li>
</ul><br/>
AIDE APIs are supported only in cluster-scoped REST roles, not in SVM-scoped REST roles.<br/>
</personalities>
### Required parameters
* `owner.uuid` - UUID of the SVM that houses this role.
* `name` - Name of the role to be updated.
* `path` - Constituent REST API path or command/command directory path, whose access level and/or query are/is to be updated. Can be a resource-qualified endpoint (example: <i>/api/storage/volumes/43256a71-be02-474d-a2a9-9642e12a6a2c/snapshots</i>). Currently, resource-qualified endpoints are limited to the <i>Snapshots</i>, <i>File System Analytics</i><personalities supports=aiml><i>, Artificial Intelligence Data Engine (AIDE)</i></personalities> and <i>ONTAP S3</i> endpoints listed above in the description.
### Optional parameters
* `access` - Access level for the path.
* `query` - Optional query, if the path refers to a command/command directory path.
### Related ONTAP commands
* `security login rest-role modify`
* `security login role modify`
### Learn more
* [`DOC /security/roles/{owner.uuid}/{name}/privileges/{path}`](#docs-security-security_roles_{owner.uuid}_{name}_privileges_{path})
* [`DOC /security/roles`](#docs-security-security_roles)
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
        r"""Deletes a privilege tuple (of REST URI or command/command directory path, its access level and an optional query) from the role. The REST URI can be a resource-qualified endpoint. Currently, the only supported resource-qualified endpoints are the following&#58;<p/>
### Snapshots APIs
&ndash; <i>/api/storage/volumes/{volume.uuid}/snapshots</i><br/>
### File System Analytics APIs
&ndash; <i>/api/storage/volumes/{volume.uuid}/files</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/clients</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/directories</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/files</i>
&ndash; <i>/api/storage/volumes/{volume.uuid}/top-metrics/users</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/clients</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/directories</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/files</i>
&ndash; <i>/api/svm/svms/{svm.uuid}/top-metrics/users</i><br/>
#### ONTAP S3 APIs
&ndash; <i>/api/protocols/s3/services/{svm.uuid}/users</i><br/>
<personalities supports=aiml>
#### Artificial Intelligence Data Engine (AIDE) APIs
##### Data Compute Node (DCN) APIs
&ndash; <i>/api/dcn/cluster/nodes/{node.uuid}/metrics</i>
&ndash; <i>/api/dcn/network/ports/{port.uuid}/metrics</i><br/>
##### Data-Engine APIs
&ndash; <i>/api/data-engine/policies/{policy.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/acls</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/acls</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{entity.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/search</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-collections/{datacollection.uuid}/versions/{version.uuid}/diffs</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/data-sources</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/entities/{entity.uuid}/custom-attributes</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/queries</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/queries/{query.uuid}/entities</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/versions</i>
&ndash; <i>/api/data-engine/workspaces/{workspace.uuid}/versions/{version.uuid}/diffs</i><br/>
When used in the context of data collection APIs, <i>{version.uuid}</i> refers to a data collection version. In the context of workspace APIs, it refers to a workspace version.<br/>
</personalities>
In the APIs above, and in the context of REST roles, the wildcard character &#42; can be used in place of <i>{volume.uuid}</i> or <i>{svm.uuid}</i> to represent <i>all</i> volumes or <i>all</i> SVMs, depending on whether the REST endpoint references volumes or SVMs. The <i>{volume.uuid}</i> corresponds to the <i>-instance-uuid</i> field in the output of the \"volume show\" command at the diagnostic privilege level. It can also be retrieved through the REST endpoint <i>/api/storage/volumes</i>.<br/>
<personalities supports=aiml>
In the AIDE APIs described above, and in the context of REST roles, the wildcard character &#42; can be used in place of variable components in the Uniform Resource Identifier (URI) path, such as <i>{node.uuid}</i>, <i>{port.uuid}</i>, <i>{policy.uuid}</i>, <i>{workspace.uuid}</i>, <i>{datacollection.uuid}</i>, <i>{entity.uuid}</i>, <i>{version.uuid}</i>, or <i>{query.uuid}</i>. The specific variable to be replaced depends on whether the REST endpoint references nodes, ports, policies, workspaces, data collections, entities, versions, or queries.<br/>
However, when using the wildcard character &#42; in place of a variable component in a URI path, it must replace <b>all</b> variable components in that path. Mixing wildcards and specific values for different variable components within the same URI path is not supported in REST roles. For example, a URI path such as <i>/api/data-engine/workspaces/c6e1b325-4125-11f0-abb5-bc2411f6fd43/data-collections/*/search</i> is not supported.<br/>
In summary, only the following two types of resource-qualified endpoints are supported in a REST role:
<ul>
  <li>All variable components in the URI path are specific values. Example: <i>/api/data-engine/workspaces/c6e1b325-4125-11f0-abb5-bc2411f6fd43/data-collections/b09b6d25-4126-11f0-abb5-bc2411f6fd43/search</i></li>
  <li>All variable components in the URI path are wildcards. Example: <i>/api/data-engine/workspaces/*/data-collections/*/search</i></li>
</ul><br/>
AIDE APIs are supported only in cluster-scoped REST roles, not in SVM-scoped REST roles.<br/>
</personalities>
### Required parameters
* `owner.uuid` - UUID of the SVM which houses this role.
* `name` - Name of the role to be updated.
* `path` - Constituent REST API path or command/command directory path to be deleted from this role. Can be a resource-qualified endpoint (example: <i>/api/svm/svms/43256a71-be02-474d-a2a9-9642e12a6a2c/top-metrics/users</i>). Currently, resource-qualified endpoints are limited to the <i>Snapshots</i>, <i>File System Analytics</i><personalities supports=aiml><i>, Artificial Intelligence Data Engine (AIDE)</i></personalities> and <i>ONTAP S3</i> endpoints listed above in the description.
### Related ONTAP commands
* `security login rest-role delete`
* `security login role delete`
### Learn more
* [`DOC /security/roles/{owner.uuid}/{name}/privileges/{path}`](#docs-security-security_roles_{owner.uuid}_{name}_privileges_{path})
* [`DOC /security/roles`](#docs-security-security_roles)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


