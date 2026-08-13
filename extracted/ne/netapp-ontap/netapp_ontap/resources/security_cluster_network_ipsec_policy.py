r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use the security cluster-network ipsec policy API endpoints to
view the IPsec policy configuration for cluster network security.
The following operations are supported:

* GET to retrieve IPsec policy configurations for cluster network security: GET security/cluster-network/ipsec/policies
* GET to retrieve a specific IPsec policy by UUID for a given node: GET security/cluster-network/ipsec/policies/{node.uuid}/{uuid}
## Examples
### Retrieving all IPsec policies for cluster network security
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityClusterNetworkIpsecPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(SecurityClusterNetworkIpsecPolicy.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    SecurityClusterNetworkIpsecPolicy(
        {
            "remote_ip": {"address": "192.168.1.2", "netmask": 24},
            "action": "esp_transport",
            "uuid": "b3c9e220-74af-11e3-9c7d-00505682a1a0",
            "authentication_method": "pki",
            "name": "policy1",
            "_links": {
                "self": {
                    "href": "/api/security/cluster-network/ipsec/policies/4ea7a442-86d1-11e0-ae1c-123478563412/b3c9e220-74af-11e3-9c7d-00505682a1a0"
                }
            },
            "node": {"uuid": "4ea7a442-86d1-11e0-ae1c-123478563412", "name": "node1"},
            "local_ip": {"address": "192.168.1.1", "netmask": 24},
            "certificate": {
                "uuid": "1cd8a442-86d1-11e0-ae1c-123478563412",
                "name": "cluster_network_cert_1",
            },
        }
    )
]

```
</div>
</div>

### Retrieving a specific IPsec policy for a given node
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityClusterNetworkIpsecPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityClusterNetworkIpsecPolicy(
        uuid="b3c9e220-74af-11e3-9c7d-00505682a1a0",
        **{"node.uuid": "4ea7a442-86d1-11e0-ae1c-123478563412"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
SecurityClusterNetworkIpsecPolicy(
    {
        "remote_ip": {"address": "192.168.1.2", "netmask": 24},
        "action": "esp_transport",
        "uuid": "b3c9e220-74af-11e3-9c7d-00505682a1a0",
        "authentication_method": "pki",
        "name": "policy1",
        "node": {"uuid": "4ea7a442-86d1-11e0-ae1c-123478563412", "name": "node1"},
        "local_ip": {"address": "192.168.1.1", "netmask": 24},
        "certificate": {
            "uuid": "1cd8a442-86d1-11e0-ae1c-123478563412",
            "name": "cluster_network_cert_1",
        },
    }
)

```
</div>
</div>
"""

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


__all__ = ["SecurityClusterNetworkIpsecPolicy", "SecurityClusterNetworkIpsecPolicySchema"]
__pdoc__ = {
    "SecurityClusterNetworkIpsecPolicySchema.resource": False,
    "SecurityClusterNetworkIpsecPolicySchema.opts": False,
}

class SecurityClusterNetworkIpsecPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityClusterNetworkIpsecPolicy object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the security_cluster_network_ipsec_policy."""

    action = marshmallow_fields.Str(
        data_key="action",
        validate=enum_validation(['bypass', 'discard', 'esp_transport', 'esp_udp']),
        allow_none=True,
    )
    r""" Action for the IPsec policy.

Valid choices:

* bypass
* discard
* esp_transport
* esp_udp"""

    authentication_method = marshmallow_fields.Str(
        data_key="authentication_method",
        validate=enum_validation(['pki']),
        allow_none=True,
    )
    r""" Authentication method for the IPsec policy. Must be PKI for cluster security.

Valid choices:

* pki"""

    certificate = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.security_certificate", "SecurityCertificateSchema"),
                data_key="certificate",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The certificate field of the security_cluster_network_ipsec_policy."""

    local_ip = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.security_cluster_network_ipsec_policy_local_ip", "SecurityClusterNetworkIpsecPolicyLocalIpSchema"),
                data_key="local_ip",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Local IP endpoint for the IPsec policy."""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=64),
        allow_none=True,
    )
    r""" IPsec policy name.

Example: policy1"""

    node = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.node", "NodeSchema"),
                data_key="node",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The node field of the security_cluster_network_ipsec_policy."""

    remote_ip = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.security_cluster_network_ipsec_policy_remote_ip", "SecurityClusterNetworkIpsecPolicyRemoteIpSchema"),
                data_key="remote_ip",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Remote IP endpoint for the IPsec policy."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier for the IPsec policy.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return SecurityClusterNetworkIpsecPolicy

    gettable_fields = [
        "links",
        "action",
        "authentication_method",
        "certificate.links",
        "certificate.name",
        "certificate.uuid",
        "local_ip",
        "name",
        "node.links",
        "node.name",
        "node.uuid",
        "remote_ip",
        "uuid",
    ]
    """links,action,authentication_method,certificate.links,certificate.name,certificate.uuid,local_ip,name,node.links,node.name,node.uuid,remote_ip,uuid,"""

    patchable_fields = [
        "certificate.name",
        "certificate.uuid",
        "node.name",
        "node.uuid",
    ]
    """certificate.name,certificate.uuid,node.name,node.uuid,"""

    postable_fields = [
        "certificate.name",
        "certificate.uuid",
        "node.name",
        "node.uuid",
    ]
    """certificate.name,certificate.uuid,node.name,node.uuid,"""

class SecurityClusterNetworkIpsecPolicy(Resource):
    r""" Cluster network security IPsec policy configuration (read-only). """

    _schema = SecurityClusterNetworkIpsecPolicySchema
    _path = "/api/security/cluster-network/ipsec/policies"
    _keys = ["node.uuid", "uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the IPsec policy configurations used for cluster network security.
### Related ONTAP commands
* 'security cluster-network ipsec policy show'

### Learn more
* [`DOC /security/cluster-network/ipsec/policies`](#docs-security-security_cluster-network_ipsec_policies)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SecurityClusterNetworkIpsecPolicy resources that match the provided query"""
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
        """Returns a list of RawResources that represent SecurityClusterNetworkIpsecPolicy resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the IPsec policy configurations used for cluster network security.
### Related ONTAP commands
* 'security cluster-network ipsec policy show'

### Learn more
* [`DOC /security/cluster-network/ipsec/policies`](#docs-security-security_cluster-network_ipsec_policies)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the IPsec policy configuration for cluster network security for a given node and policy UUID.
### Related ONTAP commands
* 'security cluster-network ipsec policy show'

### Learn more
* [`DOC /security/cluster-network/ipsec/policies`](#docs-security-security_cluster-network_ipsec_policies)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





