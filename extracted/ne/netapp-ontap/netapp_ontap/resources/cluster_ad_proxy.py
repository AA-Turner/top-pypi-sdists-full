r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API configures data SVM account information at the Active Directory. For Active Directory domain-based authentication for cluster accounts, a data SVM must be configured and registered as a machine account at the Active Directory. All authentication requests are proxied through this SVM.
## Examples
### Creating a data SVM proxy for domain-based authentication for cluster accounts
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterAdProxy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterAdProxy()
    resource.svm.uuid = "13f87d78-70c7-11e9-b722-0050568ec89f"
    resource.post(hydrate=True)
    print(resource)

```

### Updating a data SVM proxy for domain-based authentication for cluster accounts
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterAdProxy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterAdProxy()
    resource.svm.uuid = "13f87d78-70c7-11e9-b722-0050568ec89f"
    resource.patch()

```

### Retrieving a data SVM proxy for domain-based authentication for cluster accounts
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterAdProxy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterAdProxy()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
ClusterAdProxy(
    {
        "svm": {
            "name": "vs2",
            "_links": {
                "self": {"href": "/api/svm/svms/512eab7a-6bf9-11e9-a896-005056bb9ce1"}
            },
            "uuid": "512eab7a-6bf9-11e9-a896-005056bb9ce1",
        },
        "_links": {"self": {"href": "/api/security/authentication/cluster/ad-proxy"}},
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
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["ClusterAdProxy", "ClusterAdProxySchema"]
__pdoc__ = {
    "ClusterAdProxySchema.resource": False,
    "ClusterAdProxySchema.opts": False,
}


class ClusterAdProxySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterAdProxy object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the cluster_ad_proxy."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the cluster_ad_proxy."""

    @property
    def resource(self):
        return ClusterAdProxy

    gettable_fields = [
        "links",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "svm.name",
        "svm.uuid",
    ]
    """svm.name,svm.uuid,"""

    postable_fields = [
        "svm.name",
        "svm.uuid",
    ]
    """svm.name,svm.uuid,"""

class ClusterAdProxy(Resource):
    r""" The SVM configured as proxy for Active Directory authentication of cluster accounts. """

    _schema = ClusterAdProxySchema
    _path = "/api/security/authentication/cluster/ad-proxy"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves SVM information configured as an Active Directory domain-tunnel.
### Related ONTAP commands
* `security login domain-tunnel show`
### Learn more
* [`DOC /security/authentication/cluster/ad-proxy`](#docs-security-security_authentication_cluster_ad-proxy)
* [`DOC /security/accounts`](#docs-security-security_accounts)
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
        r"""Configures a data SVM as a proxy for Active Directory based authentication for cluster user accounts.
### Required properties
* `svm.name` or `svm.uuid` - Name and UUID of the SVM for a cluster user account.
### Related ONTAP commands
* `security login domain-tunnel create`
### Learn more
* [`DOC /security/authentication/cluster/ad-proxy`](#docs-security-security_authentication_cluster_ad-proxy)
* [`DOC /security/accounts`](#docs-security-security_accounts)
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
        r"""Updates the data SVM configured as a tunnel for Active Directory based authentication for cluster user accounts.
### Related ONTAP commands
* `security login domain-tunnel modify`
### Learn more
* [`DOC /security/authentication/cluster/ad-proxy`](#docs-security-security_authentication_cluster_ad-proxy)
* [`DOC /security/accounts`](#docs-security-security_accounts)
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
        r"""Deletes the data SVM configured as a tunnel for Active Directory based authentication for cluster user accounts.
### Related ONTAP commands
* `security login domain-tunnel delete`
### Learn more
* [`DOC /security/authentication/cluster/ad-proxy`](#docs-security-security_authentication_cluster_ad-proxy)
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


