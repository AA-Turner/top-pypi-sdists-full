r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Managing SVM peers
The SVM peer commands allow you to create and manage SVM peering relationships.
### SVM peer APIs
The following APIs are used to manage SVM peers:
- GET /api/svm/peers
- POST /api/svm/peers
- GET /api/svm/peers/{uuid}
- PATCH /api/svm/peers/{uuid}
- DELETE /api/svm/peers/{uuid}"""

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


__all__ = ["SvmPeer", "SvmPeerSchema"]
__pdoc__ = {
    "SvmPeerSchema.resource": False,
    "SvmPeerSchema.opts": False,
}


class SvmPeerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmPeer object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the svm_peer."""

    applications = marshmallow_fields.List(marshmallow_fields.Str, data_key="applications", allow_none=True)
    r""" A list of applications for an SVM peer relationship.

Example: ["snapmirror","lun_copy"]"""

    force = marshmallow_fields.Boolean(
        data_key="force",
        allow_none=True,
    )
    r""" Use this to suspend, resume or delete the SVM peer relationship even if the remote cluster is not accessible due to, for example, network connectivity issues."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" A peer SVM alias name to avoid a name conflict on the local cluster."""

    peer = marshmallow_fields.Nested("netapp_ontap.models.peer.PeerSchema", data_key="peer", unknown=EXCLUDE, allow_none=True)
    r""" The peer field of the svm_peer."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['peered', 'rejected', 'suspended', 'initiated', 'pending', 'initializing']),
        allow_none=True,
    )
    r""" SVM peering state. To accept a pending SVM peer request, PATCH the state to "peered". To reject a pending SVM peer request, PATCH the state to "rejected". To suspend a peered SVM peer relationship, PATCH the state to "suspended". To resume a suspended SVM peer relationship, PATCH the state to "peered". The states "initiated", "pending", and "initializing" are system-generated and cannot be used for PATCH.

Valid choices:

* peered
* rejected
* suspended
* initiated
* pending
* initializing"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the svm_peer."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" SVM peer relationship UUID"""

    @property
    def resource(self):
        return SvmPeer

    gettable_fields = [
        "links",
        "applications",
        "name",
        "peer.cluster",
        "peer.svm",
        "state",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """links,applications,name,peer.cluster,peer.svm,state,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
        "applications",
        "force",
        "name",
        "state",
    ]
    """applications,force,name,state,"""

    postable_fields = [
        "applications",
        "force",
        "name",
        "peer.cluster",
        "peer.svm",
        "svm.name",
        "svm.uuid",
    ]
    """applications,force,name,peer.cluster,peer.svm,svm.name,svm.uuid,"""

class SvmPeer(Resource):
    r""" An SVM peer relationship object. """

    _schema = SvmPeerSchema
    _path = "/api/svm/peers"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the list of SVM peer relationships.
### Related ONTAP commands
* `vserver peer show`
### Examples
The following examples show how to retrieve a collection of SVM peer relationships based on a query.
1. Retrieves a list of SVM peers of a specific local SVM
   <br/>
   ```
   GET "/api/svm/peers/?svm.name=VS1"
   ```
   <br/>
2. Retrieves a list of SVM peers of a specific cluster peer
   <br/>
   ```
   GET "/api/svm/peers/?peer.cluster.name=cluster2"
   ```
   <br/>
### Learn more
* [`DOC /svm/peers`](#docs-svm-svm_peers)
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
        """Returns a count of all SvmPeer resources that match the provided query"""
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
        """Returns a list of RawResources that represent SvmPeer resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["SvmPeer"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the SVM peer relationship.
### Related ONTAP commands
* `vserver peer modify`
### Examples
The following examples show how to update an SVM peer relationship. The input parameter 'name' refers to the local name of the peer SVM.
<br/>
1. Accepts an SVM peer relationship
   <br/>
   ```
   PATCH "/api/svm/peers/d3268a74-ee76-11e8-a9bb-005056ac6dc9" '{"state":"peered"}'
   ```
   <br/>
2. Updates the local name of an SVM peer relationship
   <br/>
   ```
   PATCH "/api/svm/peers/d3268a74-ee76-11e8-a9bb-005056ac6dc9" '{"name":"vs2"}'
   ```
   <br/>
2. Suspends an SVM peer relationship using force flag
   <br/>
   ```
   PATCH "/api/svm/peers/d3268a74-ee76-11e8-a9bb-005056ac6dc9" '{"state":"suspended", "force": "true"}'
   ```
   <br/>
### Learn more
* [`DOC /svm/peers`](#docs-svm-svm_peers)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["SvmPeer"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SvmPeer"], NetAppResponse]:
        r"""Creates a new SVM peer relationship.
### Important notes
  * The create request accepts peer SVM name as input instead of peer SVM UUID as the local cluster cannot validate peer SVM based on UUID.
  * The input parameter `name` refers to the local name of the peer SVM. The `peer cluster name` parameter is optional for creating intracluster SVM peer relationships.
### Required properties
* `svm.name` or `svm.uuid` - SVM name or SVM UUID
* `peer.svm.name` or `peer.svm.uuid` - Peer SVM name or Peer SVM UUID
* `peer.cluster.name` or `peer.cluster.uuid` - Peer cluster name or peer cluster UUID
* `applications` - Peering applications
### Related ONTAP commands
* `vserver peer create`
### Example
Creates a new SVM peer relationship.
<br/>
```
POST "/api/svm/peers" '{"svm":{"name":"vs1"}, "peer.cluster.name":"cluster2", "peer.svm.name":"VS1", "applications":["snapmirror"]}'
```
<br/>
### Learn more
* [`DOC /svm/peers`](#docs-svm-svm_peers)
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
        records: Iterable["SvmPeer"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the SVM peer relationship.
### Related ONTAP commands
* `vserver peer delete`
### Example
1. Deletes an SVM peer relationship.
   <br/>
   ```
   DELETE "/api/svm/peers/d3268a74-ee76-11e8-a9bb-005056ac6dc9"
   ```
   <br/>
2. Deletes an SVM peer relationship using force flag
   <br/>
   ```
   DELETE "/api/svm/peers/d3268a74-ee76-11e8-a9bb-005056ac6dc9" '{"force": "true"}'
   ```
   <br/>
### Learn more
* [`DOC /svm/peers`](#docs-svm-svm_peers)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the list of SVM peer relationships.
### Related ONTAP commands
* `vserver peer show`
### Examples
The following examples show how to retrieve a collection of SVM peer relationships based on a query.
1. Retrieves a list of SVM peers of a specific local SVM
   <br/>
   ```
   GET "/api/svm/peers/?svm.name=VS1"
   ```
   <br/>
2. Retrieves a list of SVM peers of a specific cluster peer
   <br/>
   ```
   GET "/api/svm/peers/?peer.cluster.name=cluster2"
   ```
   <br/>
### Learn more
* [`DOC /svm/peers`](#docs-svm-svm_peers)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the SVM peer relationship instance.
### Related ONTAP commands
* `vserver peer show`
### Example
Retrieves the parameters of an SVM peer relationship.
<br/>
```
GET "/api/svm/peers/d3268a74-ee76-11e8-a9bb-005056ac6dc9"
```
<br/>
### Learn more
* [`DOC /svm/peers`](#docs-svm-svm_peers)
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
        r"""Creates a new SVM peer relationship.
### Important notes
  * The create request accepts peer SVM name as input instead of peer SVM UUID as the local cluster cannot validate peer SVM based on UUID.
  * The input parameter `name` refers to the local name of the peer SVM. The `peer cluster name` parameter is optional for creating intracluster SVM peer relationships.
### Required properties
* `svm.name` or `svm.uuid` - SVM name or SVM UUID
* `peer.svm.name` or `peer.svm.uuid` - Peer SVM name or Peer SVM UUID
* `peer.cluster.name` or `peer.cluster.uuid` - Peer cluster name or peer cluster UUID
* `applications` - Peering applications
### Related ONTAP commands
* `vserver peer create`
### Example
Creates a new SVM peer relationship.
<br/>
```
POST "/api/svm/peers" '{"svm":{"name":"vs1"}, "peer.cluster.name":"cluster2", "peer.svm.name":"VS1", "applications":["snapmirror"]}'
```
<br/>
### Learn more
* [`DOC /svm/peers`](#docs-svm-svm_peers)
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
        r"""Updates the SVM peer relationship.
### Related ONTAP commands
* `vserver peer modify`
### Examples
The following examples show how to update an SVM peer relationship. The input parameter 'name' refers to the local name of the peer SVM.
<br/>
1. Accepts an SVM peer relationship
   <br/>
   ```
   PATCH "/api/svm/peers/d3268a74-ee76-11e8-a9bb-005056ac6dc9" '{"state":"peered"}'
   ```
   <br/>
2. Updates the local name of an SVM peer relationship
   <br/>
   ```
   PATCH "/api/svm/peers/d3268a74-ee76-11e8-a9bb-005056ac6dc9" '{"name":"vs2"}'
   ```
   <br/>
2. Suspends an SVM peer relationship using force flag
   <br/>
   ```
   PATCH "/api/svm/peers/d3268a74-ee76-11e8-a9bb-005056ac6dc9" '{"state":"suspended", "force": "true"}'
   ```
   <br/>
### Learn more
* [`DOC /svm/peers`](#docs-svm-svm_peers)
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
        r"""Deletes the SVM peer relationship.
### Related ONTAP commands
* `vserver peer delete`
### Example
1. Deletes an SVM peer relationship.
   <br/>
   ```
   DELETE "/api/svm/peers/d3268a74-ee76-11e8-a9bb-005056ac6dc9"
   ```
   <br/>
2. Deletes an SVM peer relationship using force flag
   <br/>
   ```
   DELETE "/api/svm/peers/d3268a74-ee76-11e8-a9bb-005056ac6dc9" '{"force": "true"}'
   ```
   <br/>
### Learn more
* [`DOC /svm/peers`](#docs-svm-svm_peers)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


