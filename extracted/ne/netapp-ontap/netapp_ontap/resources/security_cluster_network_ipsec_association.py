r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use the security cluster-network ipsec association API endpoints to
view IPsec and IKE (Internet Key Exchange) security associations for cluster network security.
The following operations are supported:

* Collection Get: Retrieve all IPsec/IKE associations: GET security/cluster-network/ipsec/associations
* Instance Get: Retrieve a specific association by UUID: GET security/cluster-network/ipsec/associations/{uuid}
## Examples
### Retrieving all IPsec and IKE security associations
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityClusterNetworkIpsecAssociation

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(SecurityClusterNetworkIpsecAssociation.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    SecurityClusterNetworkIpsecAssociation(
        {
            "type": "ipsec",
            "uuid": "a1b2c3d4-1234-5678-9abc-def012345678",
            "policy_name": "policy1",
            "local_address": "192.168.1.1",
            "lifetime": 28800,
            "cipher_suite": "suiteb_gcm256",
            "node": {"uuid": "4ea7a442-86d1-11e0-ae1c-123478563412", "name": "node1"},
            "ipsec": {
                "state": "installed",
                "outbound": {
                    "packets": 2048,
                    "security_parameter_index": "0x87654321",
                    "bytes": 2097152,
                },
                "action": "esp_transport",
                "inbound": {
                    "packets": 1024,
                    "security_parameter_index": "0x12345678",
                    "bytes": 1048576,
                },
            },
            "remote_address": "192.168.1.2",
        }
    ),
    SecurityClusterNetworkIpsecAssociation(
        {
            "type": "ike",
            "uuid": "b2c3d4e5-2345-6789-abcd-ef0123456789",
            "ike": {
                "version": 2,
                "authentication": "cert",
                "initiator_security_parameter_index": "0xaabbccdd",
                "responder_security_parameter_index": "0xddccbbaa",
                "is_initiator": True,
                "state": "established",
            },
            "policy_name": "policy1",
            "local_address": "192.168.1.1",
            "lifetime": 86400,
            "cipher_suite": "suiteb_gcm256",
            "node": {"uuid": "4ea7a442-86d1-11e0-ae1c-123478563412", "name": "node1"},
            "remote_address": "192.168.1.2",
        }
    ),
]

```
</div>
</div>

### Retrieving a specific security association by UUID
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityClusterNetworkIpsecAssociation

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityClusterNetworkIpsecAssociation(
        uuid="a1b2c3d4-1234-5678-9abc-def012345678"
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
SecurityClusterNetworkIpsecAssociation(
    {
        "type": "ipsec",
        "uuid": "a1b2c3d4-1234-5678-9abc-def012345678",
        "policy_name": "policy1",
        "local_address": "192.168.1.1",
        "lifetime": 28800,
        "cipher_suite": "suiteb_gcm256",
        "node": {"uuid": "4ea7a442-86d1-11e0-ae1c-123478563412", "name": "node1"},
        "ipsec": {
            "state": "installed",
            "outbound": {
                "packets": 2048,
                "security_parameter_index": "0x87654321",
                "bytes": 2097152,
            },
            "action": "esp_transport",
            "inbound": {
                "packets": 1024,
                "security_parameter_index": "0x12345678",
                "bytes": 1048576,
            },
        },
        "remote_address": "192.168.1.2",
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


__all__ = ["SecurityClusterNetworkIpsecAssociation", "SecurityClusterNetworkIpsecAssociationSchema"]
__pdoc__ = {
    "SecurityClusterNetworkIpsecAssociationSchema.resource": False,
    "SecurityClusterNetworkIpsecAssociationSchema.opts": False,
}

class SecurityClusterNetworkIpsecAssociationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityClusterNetworkIpsecAssociation object"""

    cipher_suite = marshmallow_fields.Str(
        data_key="cipher_suite",
        validate=enum_validation(['suite_aescbc', 'suiteb_gcm256', 'suiteb_gmac256']),
        allow_none=True,
    )
    r""" Cipher suite for the security association.

Valid choices:

* suite_aescbc
* suiteb_gcm256
* suiteb_gmac256"""

    ike = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.security_cluster_network_ipsec_association_ike", "SecurityClusterNetworkIpsecAssociationIkeSchema"),
                data_key="ike",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Objects containing parameters specific to IKE (Internet Key Exchange) security association for cluster network."""

    ipsec = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.security_cluster_network_ipsec_association_ipsec", "SecurityClusterNetworkIpsecAssociationIpsecSchema"),
                data_key="ipsec",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Objects containing parameters specific to IPsec security association for cluster network."""

    lifetime = Size(
        data_key="lifetime",
        allow_none=True,
    )
    r""" Lifetime for the security association in seconds."""

    local_address = marshmallow_fields.Str(
        data_key="local_address",
        allow_none=True,
    )
    r""" Local address of the security association."""

    node = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.node", "NodeSchema"),
                data_key="node",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The node field of the security_cluster_network_ipsec_association."""

    policy_name = marshmallow_fields.Str(
        data_key="policy_name",
        allow_none=True,
    )
    r""" Policy name for the security association."""

    remote_address = marshmallow_fields.Str(
        data_key="remote_address",
        allow_none=True,
    )
    r""" Remote address of the security association."""

    scope = marshmallow_fields.Str(
        data_key="scope",
        allow_none=True,
    )
    r""" The scope field of the security_cluster_network_ipsec_association."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['ipsec', 'ike']),
        allow_none=True,
    )
    r""" Type of security association, it can be IPsec or IKE (Internet Key Exchange).

Valid choices:

* ipsec
* ike"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier of the security association."""

    @property
    def resource(self):
        return SecurityClusterNetworkIpsecAssociation

    gettable_fields = [
        "cipher_suite",
        "ike",
        "ipsec",
        "lifetime",
        "local_address",
        "node.links",
        "node.name",
        "node.uuid",
        "policy_name",
        "remote_address",
        "scope",
        "type",
        "uuid",
    ]
    """cipher_suite,ike,ipsec,lifetime,local_address,node.links,node.name,node.uuid,policy_name,remote_address,scope,type,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class SecurityClusterNetworkIpsecAssociation(Resource):
    r""" Security association object for IPsec security association and IKE (Internet Key Exchange) security association for cluster network. """

    _schema = SecurityClusterNetworkIpsecAssociationSchema
    _path = "/api/security/cluster-network/ipsec/associations"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the IPsec and IKE (Internet Key Exchange) security associations for cluster network.
### Related ONTAP commands
* `security cluster-network ipsec show-ipsecsa`
* `security cluster-network ipsec show-ikesa`

### Learn more
* [`DOC /security/cluster-network/ipsec/associations`](#docs-security-security_cluster-network_ipsec_associations)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SecurityClusterNetworkIpsecAssociation resources that match the provided query"""
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
        """Returns a list of RawResources that represent SecurityClusterNetworkIpsecAssociation resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the IPsec and IKE (Internet Key Exchange) security associations for cluster network.
### Related ONTAP commands
* `security cluster-network ipsec show-ipsecsa`
* `security cluster-network ipsec show-ikesa`

### Learn more
* [`DOC /security/cluster-network/ipsec/associations`](#docs-security-security_cluster-network_ipsec_associations)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific IPsec or IKE (Internet Key Exchange) security association for cluster network.
### Related ONTAP commands
* `security cluster-network ipsec show-ipsecsa`
* `security cluster-network ipsec show-ikesa`

### Learn more
* [`DOC /security/cluster-network/ipsec/associations`](#docs-security-security_cluster-network_ipsec_associations)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





