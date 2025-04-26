r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
LDAP servers are used to centrally maintain user information. LDAP configurations must be set up
to lookup information stored in the LDAP directory on the external LDAP servers. This API is used to retrieve and manage
LDAP server configurations.
## Retrieving LDAP information
The LDAP GET endpoint retrieves all of the LDAP configurations in the cluster.
## Examples
### Retrieving all of the fields for all LDAP configurations
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LdapService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(LdapService.get_collection(fields="**")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    LdapService(
        {
            "query_timeout": 3,
            "servers": ["10.10.10.10", "domainB.example.com"],
            "schema": "ad_idmu",
            "_links": {
                "self": {
                    "href": "/api/name-services/ldap/179d3c85-7053-11e8-b9b8-005056b41bd1"
                }
            },
            "netgroup_byhost_scope": "subtree",
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/179d3c85-7053-11e8-b9b8-005056b41bd1"
                    }
                },
                "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
            },
            "group_scope": "subtree",
            "use_start_tls": True,
            "netgroup_scope": "subtree",
            "restrict_discovery_to_site": False,
            "base_dn": "dc=domainA,dc=example,dc=com",
            "group_membership_filter": "",
            "session_security": "none",
            "try_channel_binding": True,
            "bind_as_cifs_server": False,
            "base_scope": "subtree",
            "is_netgroup_byhost_enabled": False,
            "bind_dn": "cn=Administrators,cn=users,dc=domainA,dc=example,dc=com",
            "min_bind_level": "anonymous",
            "user_scope": "subtree",
            "status": {
                "code": 4915258,
                "dn_message": ["No LDAP DN configured"],
                "message": "The LDAP configuration is invalid. Verify that the AD domain or servers are reachable and that the network configuration is correct",
                "ipv6_state": "down",
                "state": "down",
                "ipv4_state": "down",
            },
            "is_owner": True,
            "ldaps_enabled": False,
            "referral_enabled": False,
            "port": 389,
        }
    ),
    LdapService(
        {
            "query_timeout": 0,
            "schema": "rfc_2307",
            "_links": {
                "self": {
                    "href": "/api/name-services/ldap/6a52023b-7066-11e8-b9b8-005056b41bd1"
                }
            },
            "netgroup_byhost_scope": "subtree",
            "svm": {
                "name": "vs2",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/6a52023b-7066-11e8-b9b8-005056b41bd1"
                    }
                },
                "uuid": "6a52023b-7066-11e8-b9b8-005056b41bd1",
            },
            "group_scope": "subtree",
            "use_start_tls": True,
            "netgroup_scope": "subtree",
            "restrict_discovery_to_site": True,
            "base_dn": "dc=domainB,dc=example,dc=com",
            "group_membership_filter": "",
            "session_security": "sign",
            "try_channel_binding": True,
            "bind_as_cifs_server": False,
            "ad_domain": "example.com",
            "base_scope": "subtree",
            "is_netgroup_byhost_enabled": False,
            "bind_dn": "cn=Administrators,cn=users,dc=domainB,dc=example,dc=com",
            "min_bind_level": "simple",
            "user_scope": "subtree",
            "status": {
                "code": 0,
                "dn_message": ["All the configured DNs are available."],
                "message": 'Successfully connected to LDAP server "172.20.192.44". Successfully connected to LDAP server "fd20:8b1e:b255:5056:999:d9:516c:bf69".',
                "ipv6_state": "up",
                "state": "up",
                "ipv4_state": "up",
            },
            "is_owner": True,
            "ldaps_enabled": False,
            "referral_enabled": False,
            "port": 389,
        }
    ),
]

```
</div>
</div>

---
### Retrieving all of the LDAP configurations that have the *use_start_tls* set to *true*
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LdapService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(LdapService.get_collection(use_start_tls=True)))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    LdapService(
        {
            "_links": {
                "self": {
                    "href": "/api/name-services/ldap/6a52023b-7066-11e8-b9b8-005056b41bd1"
                }
            },
            "svm": {
                "name": "vs2",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/6a52023b-7066-11e8-b9b8-005056b41bd1"
                    }
                },
                "uuid": "6a52023b-7066-11e8-b9b8-005056b41bd1",
            },
            "use_start_tls": True,
        }
    )
]

```
</div>
</div>

---
### Retrieving the LDAP configuration of a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LdapService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LdapService(**{"svm.uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"})
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
LdapService(
    {
        "query_timeout": 3,
        "servers": ["10.10.10.10", "domainB.example.com"],
        "schema": "ad_idmu",
        "_links": {
            "self": {
                "href": "/api/name-services/ldap/179d3c85-7053-11e8-b9b8-005056b41bd1"
            }
        },
        "svm": {
            "name": "vs1",
            "_links": {
                "self": {"href": "/api/svm/svms/179d3c85-7053-11e8-b9b8-005056b41bd1"}
            },
            "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
        },
        "use_start_tls": True,
        "restrict_discovery_to_site": False,
        "base_dn": "dc=domainA,dc=example,dc=com",
        "session_security": "none",
        "try_channel_binding": True,
        "bind_as_cifs_server": True,
        "base_scope": "subtree",
        "bind_dn": "cn=Administrators,cn=users,dc=domainA,dc=example,dc=com",
        "min_bind_level": "anonymous",
        "is_owner": True,
        "ldaps_enabled": False,
        "referral_enabled": False,
        "port": 389,
    }
)

```
</div>
</div>

---
### Retrieving all the fields of the LDAP configuration of a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LdapService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LdapService(**{"svm.uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"})
    resource.get(fields="**")
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
LdapService(
    {
        "query_timeout": 3,
        "servers": ["10.10.10.10", "domainB.example.com"],
        "schema": "ad_idmu",
        "_links": {
            "self": {
                "href": "/api/name-services/ldap/179d3c85-7053-11e8-b9b8-005056b41bd1"
            }
        },
        "netgroup_byhost_scope": "subtree",
        "svm": {
            "name": "vs1",
            "_links": {
                "self": {"href": "/api/svm/svms/179d3c85-7053-11e8-b9b8-005056b41bd1"}
            },
            "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
        },
        "group_scope": "subtree",
        "use_start_tls": True,
        "netgroup_scope": "subtree",
        "restrict_discovery_to_site": False,
        "base_dn": "dc=domainA,dc=example,dc=com",
        "group_membership_filter": "",
        "session_security": "none",
        "try_channel_binding": True,
        "bind_as_cifs_server": True,
        "base_scope": "subtree",
        "is_netgroup_byhost_enabled": False,
        "bind_dn": "cn=Administrators,cn=users,dc=domainA,dc=example,dc=com",
        "min_bind_level": "anonymous",
        "user_scope": "subtree",
        "status": {
            "code": 4915258,
            "dn_message": ["No LDAP DN configured"],
            "message": "The LDAP configuration is invalid. Verify that the AD domain or servers are reachable and that the network configuration is correct",
            "ipv6_state": "down",
            "state": "down",
            "ipv4_state": "down",
        },
        "is_owner": True,
        "ldaps_enabled": False,
        "referral_enabled": False,
        "port": 389,
    }
)

```
</div>
</div>

---
### Retrieving the LDAP server status of a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LdapService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LdapService(**{"svm.uuid": "9e4a2e3b-f66f-11ea-aec8-0050568e155c"})
    resource.get(fields="status")
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
LdapService(
    {
        "svm": {"name": "vs2", "uuid": "9e4a2e3b-f66f-11ea-aec8-0050568e155c"},
        "status": {
            "code": 0,
            "message": 'Successfully connected to LDAP server "172.20.192.44". Successfully connected to LDAP server "fd20:8b1e:b255:5056:999:d9:516c:bf69".',
            "ipv6_state": "up",
            "state": "up",
            "ipv4_state": "up",
        },
    }
)

```
</div>
</div>

---
### Retrieving all of the LDAP configurations that have the *restrict_discovery_to_site* set to *true*
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LdapService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(LdapService.get_collection(restrict_discovery_to_site=True)))

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
[
    LdapService(
        {
            "_links": {
                "self": {
                    "href": "/api/name-services/ldap/6a52023b-7066-11e8-b9b8-005056b41bd1"
                }
            },
            "svm": {
                "name": "vs2",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/6a52023b-7066-11e8-b9b8-005056b41bd1"
                    }
                },
                "uuid": "6a52023b-7066-11e8-b9b8-005056b41bd1",
            },
            "restrict_discovery_to_site": True,
        }
    )
]

```
</div>
</div>

---
## Creating an LDAP configuration
The LDAP POST endpoint creates an LDAP configuration for the specified SVM.
## Examples
### Creating an LDAP configuration with all the fields specified
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LdapService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LdapService()
    resource.svm = {"uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"}
    resource.servers = ["10.10.10.10", "domainB.example.com"]
    resource.schema = "ad_idmu"
    resource.port = 389
    resource.ldaps_enabled = False
    resource.min_bind_level = "anonymous"
    resource.bind_dn = "cn=Administrators,cn=users,dc=domainA,dc=example,dc=com"
    resource.bind_password = "abc"
    resource.base_dn = "dc=domainA,dc=example,dc=com"
    resource.base_scope = "subtree"
    resource.use_start_tls = False
    resource.session_security = "none"
    resource.referral_enabled = False
    resource.bind_as_cifs_server = False
    resource.query_timeout = 4
    resource.user_dn = "cn=abc,users,dc=com"
    resource.user_scope = "subtree"
    resource.group_dn = "cn=abc,users,dc=com"
    resource.group_scope = "subtree"
    resource.netgroup_dn = "cn=abc,users,dc=com"
    resource.netgroup_scope = "subtree"
    resource.netgroup_byhost_dn = "cn=abc,users,dc=com"
    resource.netgroup_byhost_scope = "subtree"
    resource.is_netgroup_byhost_enabled = False
    resource.group_membership_filter = ""
    resource.skip_config_validation = False
    resource.post(hydrate=True)
    print(resource)

```

---
### Creating an LDAP configuration with Active Directory domain and preferred Active Directory servers specified
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LdapService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LdapService()
    resource.svm = {"name": "vs2"}
    resource.ad_domain = "domainA.example.com"
    resource.preferred_ad_servers = ["11.11.11.11"]
    resource.port = 389
    resource.ldaps_enabled = False
    resource.bind_dn = "cn=Administrators,cn=users,dc=domainA,dc=example,dc=com"
    resource.bind_password = "abc"
    resource.base_dn = "dc=domainA,dc=example,dc=com"
    resource.session_security = "none"
    resource.referral_enabled = False
    resource.query_timeout = 3
    resource.post(hydrate=True)
    print(resource)

```

---
### Creating an LDAP configuration with a number of optional fields not specified
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LdapService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LdapService()
    resource.svm = {"name": "vs2"}
    resource.servers = ["11.11.11.11"]
    resource.port = 389
    resource.bind_dn = "cn=Administrators,cn=users,dc=domainA,dc=example,dc=com"
    resource.bind_password = "abc"
    resource.base_dn = "dc=domainA,dc=example,dc=com"
    resource.session_security = "none"
    resource.post(hydrate=True)
    print(resource)

```

---
### Creating an LDAP configuration with Active Directory domain specified and *restrict_discovery_to_site* set to *true*
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LdapService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LdapService()
    resource.svm = {"name": "vs2"}
    resource.ad_domain = "example.com"
    resource.port = 389
    resource.bind_dn = "cn=Administrators,cn=users,dc=domainA,dc=example,dc=com"
    resource.bind_password = "abc"
    resource.base_dn = "dc=domainA,dc=example,dc=com"
    resource.session_security = "none"
    resource.restrict_discovery_to_site = True
    resource.post(hydrate=True)
    print(resource)

```

---
## Updating an LDAP configuration
The LDAP PATCH endpoint updates the LDAP configuration for the specified SVM. The following example shows a PATCH operation:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LdapService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LdapService(**{"svm.uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"})
    resource.servers = ["55.55.55.55"]
    resource.schema = "ad_idmu"
    resource.port = 636
    resource.ldaps_enabled = True
    resource.use_start_tls = False
    resource.referral_enabled = False
    resource.restrict_discovery_to_site = False
    resource.patch()

```

---
## Deleting an LDAP configuration
The LDAP DELETE endpoint deletes the LDAP configuration for the specified SVM. The following example shows a DELETE operation:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LdapService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LdapService(**{"svm.uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"})
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


__all__ = ["LdapService", "LdapServiceSchema"]
__pdoc__ = {
    "LdapServiceSchema.resource": False,
    "LdapServiceSchema.opts": False,
}


class LdapServiceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LdapService object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the ldap_service."""

    ad_domain = marshmallow_fields.Str(
        data_key="ad_domain",
        allow_none=True,
    )
    r""" This parameter specifies the name of the Active Directory domain
used to discover LDAP servers for use by this client.
This is mutually exclusive with `servers` during POST and PATCH.


Example: example.com"""

    base_dn = marshmallow_fields.Str(
        data_key="base_dn",
        allow_none=True,
    )
    r""" Specifies the default base DN for all searches.

Example: dc=domainB,dc=example,dc=com"""

    base_scope = marshmallow_fields.Str(
        data_key="base_scope",
        validate=enum_validation(['base', 'onelevel', 'subtree']),
        allow_none=True,
    )
    r""" Specifies the default search scope for LDAP queries:

* base - search the named entry only
* onelevel - search all entries immediately below the DN
* subtree - search the named DN entry and the entire subtree below the DN


Valid choices:

* base
* onelevel
* subtree"""

    bind_as_cifs_server = marshmallow_fields.Boolean(
        data_key="bind_as_cifs_server",
        allow_none=True,
    )
    r""" Specifies whether or not CIFS server's credentials are used to bind to the LDAP server."""

    bind_dn = marshmallow_fields.Str(
        data_key="bind_dn",
        allow_none=True,
    )
    r""" Specifies the user that binds to the LDAP servers.

Example: cn=Administrators,cn=users,dc=domainB,dc=example,dc=com"""

    bind_password = marshmallow_fields.Str(
        data_key="bind_password",
        allow_none=True,
    )
    r""" Specifies the bind password for the LDAP servers.

Example: abc"""

    group_dn = marshmallow_fields.Str(
        data_key="group_dn",
        allow_none=True,
    )
    r""" Specifies the group Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for group lookups.

Example: cn=abc,users,dc=com"""

    group_membership_filter = marshmallow_fields.Str(
        data_key="group_membership_filter",
        allow_none=True,
    )
    r""" Specifies the custom filter used for group membership lookups from an LDAP server.


Example:"""

    group_scope = marshmallow_fields.Str(
        data_key="group_scope",
        validate=enum_validation(['base', 'onelevel', 'subtree']),
        allow_none=True,
    )
    r""" Specifies the default search scope for LDAP for group lookups:

* base - search the named entry only
* onelevel - search all entries immediately below the DN
* subtree - search the named DN entry and the entire subtree below the DN


Valid choices:

* base
* onelevel
* subtree"""

    is_netgroup_byhost_enabled = marshmallow_fields.Boolean(
        data_key="is_netgroup_byhost_enabled",
        allow_none=True,
    )
    r""" Specifies whether or not netgroup by host querying is enabled."""

    is_owner = marshmallow_fields.Boolean(
        data_key="is_owner",
        allow_none=True,
    )
    r""" Specifies whether or not the SVM owns the LDAP client configuration."""

    ldaps_enabled = marshmallow_fields.Boolean(
        data_key="ldaps_enabled",
        allow_none=True,
    )
    r""" Specifies whether or not LDAPS is enabled."""

    min_bind_level = marshmallow_fields.Str(
        data_key="min_bind_level",
        validate=enum_validation(['anonymous', 'simple', 'sasl']),
        allow_none=True,
    )
    r""" The minimum bind authentication level. Possible values are:

* anonymous - anonymous bind
* simple - simple bind
* sasl - Simple Authentication and Security Layer (SASL) bind


Valid choices:

* anonymous
* simple
* sasl"""

    netgroup_byhost_dn = marshmallow_fields.Str(
        data_key="netgroup_byhost_dn",
        allow_none=True,
    )
    r""" Specifies the netgroup Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for netgroup by host lookups.

Example: cn=abc,users,dc=com"""

    netgroup_byhost_scope = marshmallow_fields.Str(
        data_key="netgroup_byhost_scope",
        validate=enum_validation(['base', 'onelevel', 'subtree']),
        allow_none=True,
    )
    r""" Specifies the default search scope for LDAP for netgroup by host lookups:

* base - search the named entry only
* onelevel - search all entries immediately below the DN
* subtree - search the named DN entry and the entire subtree below the DN


Valid choices:

* base
* onelevel
* subtree"""

    netgroup_dn = marshmallow_fields.Str(
        data_key="netgroup_dn",
        allow_none=True,
    )
    r""" Specifies the netgroup Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for netgroup lookups.

Example: cn=abc,users,dc=com"""

    netgroup_scope = marshmallow_fields.Str(
        data_key="netgroup_scope",
        validate=enum_validation(['base', 'onelevel', 'subtree']),
        allow_none=True,
    )
    r""" Specifies the default search scope for LDAP for netgroup lookups:

* base - search the named entry only
* onelevel - search all entries immediately below the DN
* subtree - search the named DN entry and the entire subtree below the DN


Valid choices:

* base
* onelevel
* subtree"""

    port = Size(
        data_key="port",
        validate=integer_validation(minimum=1, maximum=65535),
        allow_none=True,
    )
    r""" The port used to connect to the LDAP Servers.

Example: 389"""

    preferred_ad_servers = marshmallow_fields.List(marshmallow_fields.Str, data_key="preferred_ad_servers", allow_none=True)
    r""" The preferred_ad_servers field of the ldap_service."""

    query_timeout = Size(
        data_key="query_timeout",
        allow_none=True,
    )
    r""" Specifies the maximum time to wait for a query response from the LDAP server, in seconds."""

    referral_enabled = marshmallow_fields.Boolean(
        data_key="referral_enabled",
        allow_none=True,
    )
    r""" Specifies whether or not LDAP referral is enabled."""

    restrict_discovery_to_site = marshmallow_fields.Boolean(
        data_key="restrict_discovery_to_site",
        allow_none=True,
    )
    r""" Specifies whether or not LDAP server discovery is restricted to site-scope."""

    schema = marshmallow_fields.Str(
        data_key="schema",
        allow_none=True,
    )
    r""" The name of the schema template used by the SVM.

* AD-IDMU - Active Directory Identity Management for UNIX
* AD-SFU - Active Directory Services for UNIX
* MS-AD-BIS - Active Directory Identity Management for UNIX
* RFC-2307 - Schema based on RFC 2307
* Custom schema


Example: ad_idmu"""

    servers = marshmallow_fields.List(marshmallow_fields.Str, data_key="servers", allow_none=True)
    r""" The servers field of the ldap_service."""

    session_security = marshmallow_fields.Str(
        data_key="session_security",
        validate=enum_validation(['none', 'sign', 'seal']),
        allow_none=True,
    )
    r""" Specifies the level of security to be used for LDAP communications:

* none - no signing or sealing
* sign - sign LDAP traffic
* seal - seal and sign LDAP traffic


Valid choices:

* none
* sign
* seal"""

    skip_config_validation = marshmallow_fields.Boolean(
        data_key="skip_config_validation",
        allow_none=True,
    )
    r""" Indicates whether or not the validation for the specified LDAP configuration is disabled."""

    status = marshmallow_fields.Nested("netapp_ontap.models.ldap_status.LdapStatusSchema", data_key="status", unknown=EXCLUDE, allow_none=True)
    r""" The status field of the ldap_service."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the ldap_service."""

    try_channel_binding = marshmallow_fields.Boolean(
        data_key="try_channel_binding",
        allow_none=True,
    )
    r""" Specifies whether or not channel binding is attempted in the case of TLS/LDAPS."""

    use_start_tls = marshmallow_fields.Boolean(
        data_key="use_start_tls",
        allow_none=True,
    )
    r""" Specifies whether or not to use Start TLS over LDAP connections."""

    user_dn = marshmallow_fields.Str(
        data_key="user_dn",
        allow_none=True,
    )
    r""" Specifies the user Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for user lookups.

Example: cn=abc,users,dc=com"""

    user_scope = marshmallow_fields.Str(
        data_key="user_scope",
        validate=enum_validation(['base', 'onelevel', 'subtree']),
        allow_none=True,
    )
    r""" Specifies the default search scope for LDAP for user lookups:

* base - search the named entry only
* onelevel - search all entries immediately below the DN
* subtree - search the named DN entry and the entire subtree below the DN


Valid choices:

* base
* onelevel
* subtree"""

    @property
    def resource(self):
        return LdapService

    gettable_fields = [
        "links",
        "ad_domain",
        "base_dn",
        "base_scope",
        "bind_as_cifs_server",
        "bind_dn",
        "group_dn",
        "group_membership_filter",
        "group_scope",
        "is_netgroup_byhost_enabled",
        "is_owner",
        "ldaps_enabled",
        "min_bind_level",
        "netgroup_byhost_dn",
        "netgroup_byhost_scope",
        "netgroup_dn",
        "netgroup_scope",
        "port",
        "preferred_ad_servers",
        "query_timeout",
        "referral_enabled",
        "restrict_discovery_to_site",
        "schema",
        "servers",
        "session_security",
        "status",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "try_channel_binding",
        "use_start_tls",
        "user_dn",
        "user_scope",
    ]
    """links,ad_domain,base_dn,base_scope,bind_as_cifs_server,bind_dn,group_dn,group_membership_filter,group_scope,is_netgroup_byhost_enabled,is_owner,ldaps_enabled,min_bind_level,netgroup_byhost_dn,netgroup_byhost_scope,netgroup_dn,netgroup_scope,port,preferred_ad_servers,query_timeout,referral_enabled,restrict_discovery_to_site,schema,servers,session_security,status,svm.links,svm.name,svm.uuid,try_channel_binding,use_start_tls,user_dn,user_scope,"""

    patchable_fields = [
        "ad_domain",
        "base_dn",
        "base_scope",
        "bind_as_cifs_server",
        "bind_dn",
        "bind_password",
        "group_dn",
        "group_membership_filter",
        "group_scope",
        "is_netgroup_byhost_enabled",
        "ldaps_enabled",
        "min_bind_level",
        "netgroup_byhost_dn",
        "netgroup_byhost_scope",
        "netgroup_dn",
        "netgroup_scope",
        "port",
        "preferred_ad_servers",
        "query_timeout",
        "referral_enabled",
        "restrict_discovery_to_site",
        "schema",
        "servers",
        "session_security",
        "skip_config_validation",
        "try_channel_binding",
        "use_start_tls",
        "user_dn",
        "user_scope",
    ]
    """ad_domain,base_dn,base_scope,bind_as_cifs_server,bind_dn,bind_password,group_dn,group_membership_filter,group_scope,is_netgroup_byhost_enabled,ldaps_enabled,min_bind_level,netgroup_byhost_dn,netgroup_byhost_scope,netgroup_dn,netgroup_scope,port,preferred_ad_servers,query_timeout,referral_enabled,restrict_discovery_to_site,schema,servers,session_security,skip_config_validation,try_channel_binding,use_start_tls,user_dn,user_scope,"""

    postable_fields = [
        "ad_domain",
        "base_dn",
        "base_scope",
        "bind_as_cifs_server",
        "bind_dn",
        "bind_password",
        "group_dn",
        "group_membership_filter",
        "group_scope",
        "is_netgroup_byhost_enabled",
        "ldaps_enabled",
        "min_bind_level",
        "netgroup_byhost_dn",
        "netgroup_byhost_scope",
        "netgroup_dn",
        "netgroup_scope",
        "port",
        "preferred_ad_servers",
        "query_timeout",
        "referral_enabled",
        "restrict_discovery_to_site",
        "schema",
        "servers",
        "session_security",
        "skip_config_validation",
        "svm.name",
        "svm.uuid",
        "try_channel_binding",
        "use_start_tls",
        "user_dn",
        "user_scope",
    ]
    """ad_domain,base_dn,base_scope,bind_as_cifs_server,bind_dn,bind_password,group_dn,group_membership_filter,group_scope,is_netgroup_byhost_enabled,ldaps_enabled,min_bind_level,netgroup_byhost_dn,netgroup_byhost_scope,netgroup_dn,netgroup_scope,port,preferred_ad_servers,query_timeout,referral_enabled,restrict_discovery_to_site,schema,servers,session_security,skip_config_validation,svm.name,svm.uuid,try_channel_binding,use_start_tls,user_dn,user_scope,"""

class LdapService(Resource):
    """Allows interaction with LdapService objects on the host"""

    _schema = LdapServiceSchema
    _path = "/api/name-services/ldap"
    _keys = ["svm.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the LDAP configurations for all SVMs.
### Related ONTAP commands
  * `ldap show`
  * `ldap check -vserver vs0`
  * `ldap check-ipv6 -vserver vs0`
### Important notes
  * The status.code, status.dn_message, status.message, and status.state fields have the same status fields that are returned using the "ldap check" CLI command.
  * Refer to the ipv4 or ipv6 objects available in the status field to get specific information about the code, dn_messages, or message and state information for ipv4 or ipv6.

### Learn more
* [`DOC /name-services/ldap`](#docs-name-services-name-services_ldap)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all LdapService resources that match the provided query"""
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
        """Returns a list of RawResources that represent LdapService resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["LdapService"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates an LDAP configuration of an SVM.
### Important notes
* Both mandatory and optional parameters of the LDAP configuration can be updated.
* The LDAP servers and Active Directory domain are mutually exclusive fields. These fields cannot be empty. At any point in time, either the LDAP servers or Active Directory domain must be populated.
* IPv6 must be enabled if IPv6 family addresses are specified.<br/>
</br>Configuring more than one LDAP server is recommended to avoid a single point of failure.
Both FQDNs and IP addresses are supported for the "servers" field.
The Active Directory domain or LDAP servers are validated as part of this operation.<br/>
LDAP validation fails in the following scenarios:<br/>
1. The server does not have LDAP installed.
2. The server or Active Directory domain is invalid.
3. The server or Active Directory domain is unreachable<br/>

### Learn more
* [`DOC /name-services/ldap`](#docs-name-services-name-services_ldap)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["LdapService"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["LdapService"], NetAppResponse]:
        r"""Creates an LDAP configuration for an SVM.
### Important notes
* Each SVM can have one LDAP configuration.
* The LDAP servers and Active Directory domain are mutually exclusive fields. These fields cannot be empty. At any point in time, either the LDAP servers or Active Directory domain must be populated.
* LDAP configuration with Active Directory domain cannot be created on an admin SVM.
* IPv6 must be enabled if IPv6 family addresses are specified.</br>
#### The following parameters are optional:
- preferred AD servers
- schema
- port
- ldaps_enabled
- min_bind_level
- bind_password
- base_scope
- use_start_tls
- session_security
- referral_enabled
- bind_as_cifs_server
- query_timeout
- user_dn
- user_scope
- group_dn
- group_scope
- netgroup_dn
- netgroup_scope
- netgroup_byhost_dn
- netgroup_byhost_scope
- is_netgroup_byhost_enabled
- group_membership_filter
- skip_config_validation
- try_channel_binding
- restrict_discovery_to_site</br>
Configuring more than one LDAP server is recommended to avoid a single point of failure.
Both FQDNs and IP addresses are supported for the "servers" field.
The Active Directory domain or LDAP servers are validated as part of this operation.</br>
LDAP validation fails in the following scenarios:<br/>
1. The server does not have LDAP installed.
2. The server or Active Directory domain is invalid.
3. The server or Active Directory domain is unreachable.<br/>

### Learn more
* [`DOC /name-services/ldap`](#docs-name-services-name-services_ldap)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["LdapService"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the LDAP configuration of the specified SVM. LDAP can be removed as a source from the ns-switch if LDAP is not used as a source for lookups.

### Learn more
* [`DOC /name-services/ldap`](#docs-name-services-name-services_ldap)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the LDAP configurations for all SVMs.
### Related ONTAP commands
  * `ldap show`
  * `ldap check -vserver vs0`
  * `ldap check-ipv6 -vserver vs0`
### Important notes
  * The status.code, status.dn_message, status.message, and status.state fields have the same status fields that are returned using the "ldap check" CLI command.
  * Refer to the ipv4 or ipv6 objects available in the status field to get specific information about the code, dn_messages, or message and state information for ipv4 or ipv6.

### Learn more
* [`DOC /name-services/ldap`](#docs-name-services-name-services_ldap)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves LDAP configuration for an SVM. All parameters for the LDAP configuration are displayed by default.
### Related ONTAP commands
  * `ldap show`
  * `ldap check -vserver vs0`
  * `ldap check-ipv6 -vserver vs0`
### Important notes
  * The status.code, status.dn_message, status.message, and status.state fields have the same status fields that are returned using the "ldap check" CLI command.
  * Refer to the ipv4 or ipv6 objects available in the status field to get specific information about the code, dn_messages, or message and state information for ipv4 or ipv6.

### Learn more
* [`DOC /name-services/ldap`](#docs-name-services-name-services_ldap)"""
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
        r"""Creates an LDAP configuration for an SVM.
### Important notes
* Each SVM can have one LDAP configuration.
* The LDAP servers and Active Directory domain are mutually exclusive fields. These fields cannot be empty. At any point in time, either the LDAP servers or Active Directory domain must be populated.
* LDAP configuration with Active Directory domain cannot be created on an admin SVM.
* IPv6 must be enabled if IPv6 family addresses are specified.</br>
#### The following parameters are optional:
- preferred AD servers
- schema
- port
- ldaps_enabled
- min_bind_level
- bind_password
- base_scope
- use_start_tls
- session_security
- referral_enabled
- bind_as_cifs_server
- query_timeout
- user_dn
- user_scope
- group_dn
- group_scope
- netgroup_dn
- netgroup_scope
- netgroup_byhost_dn
- netgroup_byhost_scope
- is_netgroup_byhost_enabled
- group_membership_filter
- skip_config_validation
- try_channel_binding
- restrict_discovery_to_site</br>
Configuring more than one LDAP server is recommended to avoid a single point of failure.
Both FQDNs and IP addresses are supported for the "servers" field.
The Active Directory domain or LDAP servers are validated as part of this operation.</br>
LDAP validation fails in the following scenarios:<br/>
1. The server does not have LDAP installed.
2. The server or Active Directory domain is invalid.
3. The server or Active Directory domain is unreachable.<br/>

### Learn more
* [`DOC /name-services/ldap`](#docs-name-services-name-services_ldap)"""
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
        r"""Updates an LDAP configuration of an SVM.
### Important notes
* Both mandatory and optional parameters of the LDAP configuration can be updated.
* The LDAP servers and Active Directory domain are mutually exclusive fields. These fields cannot be empty. At any point in time, either the LDAP servers or Active Directory domain must be populated.
* IPv6 must be enabled if IPv6 family addresses are specified.<br/>
</br>Configuring more than one LDAP server is recommended to avoid a single point of failure.
Both FQDNs and IP addresses are supported for the "servers" field.
The Active Directory domain or LDAP servers are validated as part of this operation.<br/>
LDAP validation fails in the following scenarios:<br/>
1. The server does not have LDAP installed.
2. The server or Active Directory domain is invalid.
3. The server or Active Directory domain is unreachable<br/>

### Learn more
* [`DOC /name-services/ldap`](#docs-name-services-name-services_ldap)"""
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
        r"""Deletes the LDAP configuration of the specified SVM. LDAP can be removed as a source from the ns-switch if LDAP is not used as a source for lookups.

### Learn more
* [`DOC /name-services/ldap`](#docs-name-services-name-services_ldap)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


