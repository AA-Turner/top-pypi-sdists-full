r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Displays CIFS domain-related information of the specified SVM.
## Examples
### Retrieving all the fields of CIFS domain configurations of a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsDomain

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsDomain(**{"svm.uuid": "6dd78167-c907-11eb-b2bf-0050568e7324"})
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
CifsDomain(
    {
        "server_discovery_mode": "all",
        "preferred_dcs": [{"fqdn": "server02.com", "server_ip": "192.168.20.1"}],
        "trust_relationships": [
            {
                "trusted_domains": ["SERVER02.COM"],
                "home_domain": "SERVER02.COM",
                "node": {
                    "name": "vsNode2",
                    "uuid": "4d9400f0-c84b-11eb-90ab-0050568e7324",
                },
            }
        ],
        "name_mapping": {"trusted_domains": ["SERVER03.COM", "SERVER04.COM"]},
        "svm": {"name": "vs2", "uuid": "6dd78167-c907-11eb-b2bf-0050568e7324"},
        "password_schedule": {
            "schedule_description": "Tue@1:00",
            "schedule_randomized_minute": 120,
            "schedule_enabled": False,
            "schedule_weekly_interval": 4,
        },
        "discovered_servers": [
            {
                "server_name": "scspb0659002001",
                "domain": "server02.com",
                "node": {
                    "name": "vsNode2",
                    "uuid": "4d9400f0-c84b-11eb-90ab-0050568e7324",
                },
                "server_ip": "192.168.20.1",
                "server_type": "kerberos",
                "state": "undetermined",
                "preference": "preferred",
            },
            {
                "server_name": "scspb0659002001",
                "domain": "server02.com",
                "node": {
                    "name": "vsNode2",
                    "uuid": "4d9400f0-c84b-11eb-90ab-0050568e7324",
                },
                "server_ip": "192.168.20.1",
                "server_type": "ms_ldap",
                "state": "undetermined",
                "preference": "preferred",
            },
            {
                "server_name": "scspb0659002001",
                "domain": "server02.com",
                "node": {
                    "name": "vsNode2",
                    "uuid": "4d9400f0-c84b-11eb-90ab-0050568e7324",
                },
                "server_ip": "192.168.20.1",
                "server_type": "ms_dc",
                "state": "undetermined",
                "preference": "preferred",
            },
        ],
    }
)

```
</div>
</div>

---
### Applying rediscover_trusts query parameter and retrieving all the fields of CIFS domain configurations
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsDomain

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsDomain(**{"svm.uuid": "6dd78167-c907-11eb-b2bf-0050568e7324"})
    resource.get(rediscover_trusts=True)
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
CifsDomain(
    {
        "server_discovery_mode": "all",
        "preferred_dcs": [{"fqdn": "server02.com", "server_ip": "192.168.20.1"}],
        "trust_relationships": [
            {
                "trusted_domains": ["SERVER02.COM"],
                "home_domain": "SERVER02.COM",
                "node": {
                    "name": "vsNode1",
                    "uuid": "a64c0906-c7dd-11eb-af15-0050568e403e",
                },
            },
            {
                "trusted_domains": ["SERVER02.COM"],
                "home_domain": "SERVER02.COM",
                "node": {
                    "name": "vsNode2",
                    "uuid": "4d9400f0-c84b-11eb-90ab-0050568e7324",
                },
            },
        ],
        "name_mapping": {"trusted_domains": ["SERVER03.COM", "SERVER04.COM"]},
        "svm": {"name": "vs2", "uuid": "6dd78167-c907-11eb-b2bf-0050568e7324"},
        "password_schedule": {
            "schedule_description": "Tue@1:00",
            "schedule_randomized_minute": 120,
            "schedule_enabled": False,
            "schedule_weekly_interval": 4,
        },
        "discovered_servers": [
            {
                "server_name": "scspb0659002001",
                "domain": "server02.com",
                "node": {
                    "name": "vsNode2",
                    "uuid": "4d9400f0-c84b-11eb-90ab-0050568e7324",
                },
                "server_ip": "192.168.20.1",
                "server_type": "kerberos",
                "state": "undetermined",
                "preference": "preferred",
            },
            {
                "server_name": "scspb0659002001",
                "domain": "server02.com",
                "node": {
                    "name": "vsNode2",
                    "uuid": "4d9400f0-c84b-11eb-90ab-0050568e7324",
                },
                "server_ip": "192.168.20.1",
                "server_type": "ms_ldap",
                "state": "undetermined",
                "preference": "preferred",
            },
            {
                "server_name": "scspb0659002001",
                "domain": "server02.com",
                "node": {
                    "name": "vsNode2",
                    "uuid": "4d9400f0-c84b-11eb-90ab-0050568e7324",
                },
                "server_ip": "192.168.20.1",
                "server_type": "ms_dc",
                "state": "undetermined",
                "preference": "preferred",
            },
        ],
    }
)

```
</div>
</div>

---
### Modifying the Password Schedule of CIFS domain configurations of a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsDomain

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsDomain(**{"svm.uuid": "a83f816a-c873-11ed-a3b2-0050568e278e"})
    resource.password_schedule = {"schedule_enabled": "true"}
    resource.patch()

```

---
### Modifying the discovery-mode of CIFS domain configurations of a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsDomain

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsDomain(**{"svm.uuid": "a83f816a-c873-11ed-a3b2-0050568e278e"})
    resource.server_discovery_mode = "site"
    resource.patch()

```

---
### Reset the CIFS domain password for a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsDomain

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsDomain(**{"svm.uuid": "a12f816a-c873-11ed-a3b2-0050568e278e"})
    resource.ad_domain = {"user": "administrator", "password": "admin_password"}
    resource.patch(hydrate=True, cifs_password_operation="reset")

```

---
### Reset the CIFS domain password for a specific SVM with hybrid auth user type
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsDomain

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsDomain(**{"svm.uuid": "a12f816a-c873-11ed-a3b2-0050568e278e"})
    resource.tenant_id = "ffffffff-ffff-ffff-ffff-ffffffffffff"
    resource.client_id = "ffffffff-zzzz-zzzz-zzzz-ffffffffffff"
    resource.client_certificate = "certificate added to the azure application"
    resource.patch(hydrate=True, cifs_password_operation="reset")

```

---
### Change the CIFS domain password for a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsDomain

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsDomain(**{"svm.uuid": "a12f816a-c873-11ed-a3b2-0050568e278e"})
    resource.patch(hydrate=True, cifs_password_operation="reset")

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


__all__ = ["CifsDomain", "CifsDomainSchema"]
__pdoc__ = {
    "CifsDomainSchema.resource": False,
    "CifsDomainSchema.opts": False,
}


class CifsDomainSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CifsDomain object"""

    ad_domain = marshmallow_fields.Nested("netapp_ontap.models.cifs_ad_domain.CifsAdDomainSchema", data_key="ad_domain", unknown=EXCLUDE, allow_none=True)
    r""" The ad_domain field of the cifs_domain."""

    client_certificate = marshmallow_fields.Str(
        data_key="client_certificate",
        allow_none=True,
    )
    r""" PKCS12 certificate used by the application to prove its identity to AKV.

Example: PEM Cert"""

    client_id = marshmallow_fields.Str(
        data_key="client_id",
        allow_none=True,
    )
    r""" Application client ID of the deployed Azure application with appropriate access to an AKV or EntraId.

Example: e959d1b5-5a63-4284-9268-851e30e3eceb"""

    discovered_servers = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.cifs_domain_discovered_server.CifsDomainDiscoveredServerSchema", unknown=EXCLUDE, allow_none=True), data_key="discovered_servers", allow_none=True)
    r""" Specifies the discovered servers records."""

    name_mapping = marshmallow_fields.Nested("netapp_ontap.models.cifs_domain_name_mapping.CifsDomainNameMappingSchema", data_key="name_mapping", unknown=EXCLUDE, allow_none=True)
    r""" The name_mapping field of the cifs_domain."""

    password_schedule = marshmallow_fields.Nested("netapp_ontap.models.cifs_domain_password_schedule.CifsDomainPasswordScheduleSchema", data_key="password_schedule", unknown=EXCLUDE, allow_none=True)
    r""" The password_schedule field of the cifs_domain."""

    preferred_dcs = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.preferred_dcs.PreferredDcsSchema", unknown=EXCLUDE, allow_none=True), data_key="preferred_dcs", allow_none=True)
    r""" Specifies the preferred DC records."""

    server_discovery_mode = marshmallow_fields.Str(
        data_key="server_discovery_mode",
        validate=enum_validation(['all', 'site', 'none']),
        allow_none=True,
    )
    r""" Specifies the mode of server discovery.


Valid choices:

* all
* site
* none"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the cifs_domain."""

    tenant_id = marshmallow_fields.Str(
        data_key="tenant_id",
        allow_none=True,
    )
    r""" Directory (tenant) ID of the deployed Azure application with appropriate access to an AKV or EntraId.

Example: c9f32fcb-4ab7-40fe-af1b-1850d46cfbbe"""

    trust_relationships = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.cifs_domain_trust.CifsDomainTrustSchema", unknown=EXCLUDE, allow_none=True), data_key="trust_relationships", allow_none=True)
    r""" Specifies the trusted domain records."""

    @property
    def resource(self):
        return CifsDomain

    gettable_fields = [
        "ad_domain",
        "client_id",
        "discovered_servers",
        "name_mapping",
        "password_schedule",
        "preferred_dcs",
        "server_discovery_mode",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "tenant_id",
        "trust_relationships",
    ]
    """ad_domain,client_id,discovered_servers,name_mapping,password_schedule,preferred_dcs,server_discovery_mode,svm.links,svm.name,svm.uuid,tenant_id,trust_relationships,"""

    patchable_fields = [
        "ad_domain",
        "client_certificate",
        "client_id",
        "password_schedule",
        "server_discovery_mode",
        "tenant_id",
    ]
    """ad_domain,client_certificate,client_id,password_schedule,server_discovery_mode,tenant_id,"""

    postable_fields = [
        "ad_domain",
        "client_certificate",
        "client_id",
        "password_schedule",
        "server_discovery_mode",
        "tenant_id",
    ]
    """ad_domain,client_certificate,client_id,password_schedule,server_discovery_mode,tenant_id,"""

class CifsDomain(Resource):
    """Allows interaction with CifsDomain objects on the host"""

    _schema = CifsDomainSchema
    _path = "/api/protocols/cifs/domains"
    _keys = ["svm.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the CIFS domain-related information of all SVMs.
### Related ONTAP commands
* `vserver cifs domain preferred-dc show`
* `vserver cifs domain trusts show`
* `vserver cifs domain discovered-servers show`
* `vserver cifs domain name-mapping-search show`
* `vserver cifs domain schedule show`
### Learn more
* [`DOC /protocols/cifs/domains`](#docs-NAS-protocols_cifs_domains)
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
        """Returns a count of all CifsDomain resources that match the provided query"""
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
        """Returns a list of RawResources that represent CifsDomain resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["CifsDomain"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Modifies the CIFS domain-related information of the specified SVM.
### Related ONTAP commands
* `vserver cifs domain password schedule modify`
* `vserver cifs domain discovered-servers discovery-mode modify`
* `vserver cifs domain password reset`
* `vserver cifs domain password change`
### Important notes
* If the query is set to cifs_password_operation=reset and ad_domain_user and ad_domain_password is included in the body,a CIFS password reset is executed.
* If the query is set to cifs_password_operation=reset and tenant_id, client_id and client_certificate is included in the body,a CIFS password reset is executed in Azure EntraId for hybrid user.
* If the body is empty when the query is set to cifs_password_operation=reset, a CIFS password change is executed.
### Learn more
* [`DOC /protocols/cifs/domains/{svm.uuid}`](#docs-NAS-protocols_cifs_domains_{svm.uuid})
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the CIFS domain-related information of all SVMs.
### Related ONTAP commands
* `vserver cifs domain preferred-dc show`
* `vserver cifs domain trusts show`
* `vserver cifs domain discovered-servers show`
* `vserver cifs domain name-mapping-search show`
* `vserver cifs domain schedule show`
### Learn more
* [`DOC /protocols/cifs/domains`](#docs-NAS-protocols_cifs_domains)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the CIFS domain-related information of the specified SVM.
### Important notes
GET operation with query parameter `rediscover_trusts` and `reset_discovered_servers` returns available CIFS domain configurations and also triggers trusts rediscovery and discovered servers reset asynchronously for that SVM.
### Related ONTAP commands
* `vserver cifs domain preferred-dc show`
* `vserver cifs domain trusts show`
* `vserver cifs domain discovered-servers show`
* `vserver cifs domain name-mapping-search show`
* `vserver cifs domain password schedule show`
* `vserver cifs domain discovered-servers discovery-mode show`
### Learn more
* [`DOC /protocols/cifs/domains/{svm.uuid}`](#docs-NAS-protocols_cifs_domains_{svm.uuid})
"""
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
        r"""Modifies the CIFS domain-related information of the specified SVM.
### Related ONTAP commands
* `vserver cifs domain password schedule modify`
* `vserver cifs domain discovered-servers discovery-mode modify`
* `vserver cifs domain password reset`
* `vserver cifs domain password change`
### Important notes
* If the query is set to cifs_password_operation=reset and ad_domain_user and ad_domain_password is included in the body,a CIFS password reset is executed.
* If the query is set to cifs_password_operation=reset and tenant_id, client_id and client_certificate is included in the body,a CIFS password reset is executed in Azure EntraId for hybrid user.
* If the body is empty when the query is set to cifs_password_operation=reset, a CIFS password change is executed.
### Learn more
* [`DOC /protocols/cifs/domains/{svm.uuid}`](#docs-NAS-protocols_cifs_domains_{svm.uuid})
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



