r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use the security cluster-network certificate API endpoints to
view and modify the certificate configuration for cluster network security.
The following operations are supported:

* GET to retrieve the certificate configuration for cluster network security: GET security/cluster-network/certificates
* PATCH to update the certificate configuration for cluster network security for a given node: PATCH security/cluster-network/certificates/{node.uuid}
* POST to specify the certificate configuration for cluster network security for a given node: POST security/cluster-network/certificates
* DELETE to remove the certificate configuration for cluster network security for a given node: DELETE security/cluster-network/certificates/{node.uuid}
## Examples
### Retrieving all certificate configurations for cluster network security
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityClusterNetworkCertificates

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(SecurityClusterNetworkCertificates.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    SecurityClusterNetworkCertificates(
        {
            "certificate": {
                "uuid": "1cd8a442-86d1-11e0-ae1c-123478563412",
                "name": "cluster_network_cert_1",
            },
            "_links": {
                "self": {
                    "href": "/api/security/cluster-network/certificates/4ea7a442-86d1-11e0-ae1c-123478563412"
                }
            },
            "node": {"uuid": "4ea7a442-86d1-11e0-ae1c-123478563412", "name": "node1"},
        }
    ),
    SecurityClusterNetworkCertificates(
        {
            "certificate": {
                "uuid": "2de9b553-97e2-22f1-bf2d-234589674523",
                "name": "cluster_network_cert_2",
            },
            "_links": {
                "self": {
                    "href": "/api/security/cluster-network/certificates/5fb8b553-97e2-22f1-bf2d-234589674523"
                }
            },
            "node": {"uuid": "5fb8b553-97e2-22f1-bf2d-234589674523", "name": "node2"},
        }
    ),
]

```
</div>
</div>

### Assigning a certificate to a node for cluster network security
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityClusterNetworkCertificates

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityClusterNetworkCertificates()
    resource.node = {"uuid": "4ea7a442-86d1-11e0-ae1c-123478563412"}
    resource.certificate = {"name": "cluster_network_cert_1"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
SecurityClusterNetworkCertificates(
    {
        "certificate": {
            "uuid": "1cd8a442-86d1-11e0-ae1c-123478563412",
            "name": "cluster_network_cert_1",
        },
        "node": {"uuid": "4ea7a442-86d1-11e0-ae1c-123478563412", "name": "node1"},
    }
)

```
</div>
</div>

### Updating the certificate for a specific node
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityClusterNetworkCertificates

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityClusterNetworkCertificates(
        **{"node.uuid": "4ea7a442-86d1-11e0-ae1c-123478563412"}
    )
    resource.certificate = {"name": "cluster_network_cert_new"}
    resource.patch()

```

### Deleting the certificate configuration for a specific node
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityClusterNetworkCertificates

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityClusterNetworkCertificates(
        **{"node.uuid": "4ea7a442-86d1-11e0-ae1c-123478563412"}
    )
    resource.delete()

```
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


__all__ = ["SecurityClusterNetworkCertificates", "SecurityClusterNetworkCertificatesSchema"]
__pdoc__ = {
    "SecurityClusterNetworkCertificatesSchema.resource": False,
    "SecurityClusterNetworkCertificatesSchema.opts": False,
}

class SecurityClusterNetworkCertificatesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityClusterNetworkCertificates object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the security_cluster_network_certificates."""

    certificate = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.security_certificate", "SecurityCertificateSchema"),
                data_key="certificate",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The certificate field of the security_cluster_network_certificates."""

    node = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.node", "NodeSchema"),
                data_key="node",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The node field of the security_cluster_network_certificates."""

    @property
    def resource(self):
        return SecurityClusterNetworkCertificates

    gettable_fields = [
        "links",
        "certificate.links",
        "certificate.name",
        "certificate.uuid",
        "node.links",
        "node.name",
        "node.uuid",
    ]
    """links,certificate.links,certificate.name,certificate.uuid,node.links,node.name,node.uuid,"""

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

class SecurityClusterNetworkCertificates(Resource):
    r""" Manages the cluster network security certificate configuration. """

    _schema = SecurityClusterNetworkCertificatesSchema
    _path = "/api/security/cluster-network/certificates"
    _keys = ["node.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the certificate configuration used for cluster network security.
### Related ONTAP commands
* 'security cluster-network certificate show'

### Learn more
* [`DOC /security/cluster-network/certificates`](#docs-security-security_cluster-network_certificates)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SecurityClusterNetworkCertificates resources that match the provided query"""
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
        """Returns a list of RawResources that represent SecurityClusterNetworkCertificates resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["SecurityClusterNetworkCertificates"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the certificate configuration for cluster network security for a given node.
### Required properties
* `certificate.name` - The name of the certificate to assign.
### Related ONTAP commands
* 'security cluster-network certificate modify'

### Learn more
* [`DOC /security/cluster-network/certificates`](#docs-security-security_cluster-network_certificates)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["SecurityClusterNetworkCertificates"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SecurityClusterNetworkCertificates"], NetAppResponse]:
        r"""Specifies the certificate configuration for cluster network security for a given node.
### Required properties
* `node.uuid` - The UUID of the node to which the certificate will be assigned.
* `certificate.name` -The certificate name.
### Related ONTAP commands
* 'security cluster-network certificate create'

### Learn more
* [`DOC /security/cluster-network/certificates`](#docs-security-security_cluster-network_certificates)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["SecurityClusterNetworkCertificates"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the certificate configuration for cluster network security for a given node.
### Required properties
* `node: Node UUID`
### Related ONTAP commands
* 'security cluster-network certificate delete'

### Learn more
* [`DOC /security/cluster-network/certificates`](#docs-security-security_cluster-network_certificates)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the certificate configuration used for cluster network security.
### Related ONTAP commands
* 'security cluster-network certificate show'

### Learn more
* [`DOC /security/cluster-network/certificates`](#docs-security-security_cluster-network_certificates)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the certificate configuration for cluster network security for a given node.
### Related ONTAP commands
* 'security cluster-network certificate show'

### Learn more
* [`DOC /security/cluster-network/certificates`](#docs-security-security_cluster-network_certificates)"""
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
        r"""Specifies the certificate configuration for cluster network security for a given node.
### Required properties
* `node.uuid` - The UUID of the node to which the certificate will be assigned.
* `certificate.name` -The certificate name.
### Related ONTAP commands
* 'security cluster-network certificate create'

### Learn more
* [`DOC /security/cluster-network/certificates`](#docs-security-security_cluster-network_certificates)"""
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
        r"""Updates the certificate configuration for cluster network security for a given node.
### Required properties
* `certificate.name` - The name of the certificate to assign.
### Related ONTAP commands
* 'security cluster-network certificate modify'

### Learn more
* [`DOC /security/cluster-network/certificates`](#docs-security-security_cluster-network_certificates)"""
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
        r"""Deletes the certificate configuration for cluster network security for a given node.
### Required properties
* `node: Node UUID`
### Related ONTAP commands
* 'security cluster-network certificate delete'

### Learn more
* [`DOC /security/cluster-network/certificates`](#docs-security-security_cluster-network_certificates)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


