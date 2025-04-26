r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Defines, retrieves, updates and deletes an individual SNMP user.
## Examples
### Retrieves the details of an SNMP user
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SnmpUser

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SnmpUser(
        name="snmpv1user2", engine_id="80000315056622e52625a9e911a981005056bb1dcb"
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
SnmpUser(
    {
        "engine_id": "80000315056622e52625a9e911a981005056bb1dcb",
        "name": "snmpv1user2",
        "_links": {
            "self": {
                "href": "/api/support/snmp/users/80000315056622e52625a9e911a981005056bb1dcb/snmpv1user2"
            }
        },
        "owner": {"name": "cluster-1", "uuid": "26e52266-a925-11e9-a981-005056bb1dcb"},
        "authentication_method": "community",
        "scope": "cluster",
    }
)

```
</div>
</div>

<br/>
### Updates the comment parameter for an individual SNMP user
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SnmpUser

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SnmpUser(
        name="public", engine_id="8000031505b67667a26975e9118a480050568e6f74"
    )
    resource.comment = "Default SNMP community"
    resource.patch()

```

### Deletes an individual SNMP user in the cluster
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SnmpUser

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SnmpUser(
        name="snmpuser", engine_id="8000031505b67667a26975e9118a480050568e6f74"
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
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["SnmpUser", "SnmpUserSchema"]
__pdoc__ = {
    "SnmpUserSchema.resource": False,
    "SnmpUserSchema.opts": False,
}


class SnmpUserSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnmpUser object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the snmp_user."""

    authentication_method = marshmallow_fields.Str(
        data_key="authentication_method",
        validate=enum_validation(['community', 'usm', 'both']),
        allow_none=True,
    )
    r""" Optional authentication method.

Valid choices:

* community
* usm
* both"""

    comment = marshmallow_fields.Str(
        data_key="comment",
        validate=len_validation(minimum=0, maximum=128),
        allow_none=True,
    )
    r""" Optional comment text.

Example: This is a comment."""

    engine_id = marshmallow_fields.Str(
        data_key="engine_id",
        allow_none=True,
    )
    r""" Optional SNMPv3 engine identifier. For a local SNMP user belonging to the administrative Storage Virtual Machine (SVM), the default value of this parameter is the SNMPv3 engine identifier for the administrative SVM. For a local SNMP user belonging to a data SVM, the default value of this parameter is the SNMPv3 engine identifier for that data SVM. For an SNMPv1/SNMPv2c community, this parameter should not be specified in "POST" method. For a remote switch SNMPv3 user, this parameter specifies the SNMPv3 engine identifier for the remote switch. This parameter can also optionally specify a custom engine identifier.

Example: 80000315055415ab26d4aae811ac4d005056bb792e"""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=0, maximum=32),
        allow_none=True,
    )
    r""" SNMP user name.

Example: snmpv3user2"""

    owner = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="owner", unknown=EXCLUDE, allow_none=True)
    r""" The owner field of the snmp_user."""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['svm', 'cluster']),
        allow_none=True,
    )
    r""" Set to "svm" for data Storage Virtual Machine (SVM) SNMP users and to "cluster" for administrative SVM SNMP users.

Valid choices:

* svm
* cluster"""

    snmpv3 = marshmallow_fields.Nested("netapp_ontap.models.usm.UsmSchema", data_key="snmpv3", unknown=EXCLUDE, allow_none=True)
    r""" User-based Security Model (USM) object defines SNMPv3-specific parameters required to configure an SNMPv3 user."""

    switch_address = marshmallow_fields.Str(
        data_key="switch_address",
        allow_none=True,
    )
    r""" Optional remote switch address. It can be an IPv4 address or an IPv6 address. A remote switch can be queried over SNMPv3 using ONTAP SNMP client functionality. Querying such a switch requires an SNMPv3 user (remote switch user) to be configured on the switch. Since ONTAP requires remote switch user's SNMPv3 credentials (to query it), this user must be configured in ONTAP as well. This parameter is specified when configuring such a user.

Example: 10.23.34.45"""

    @property
    def resource(self):
        return SnmpUser

    gettable_fields = [
        "links",
        "authentication_method",
        "comment",
        "engine_id",
        "name",
        "owner.links",
        "owner.name",
        "owner.uuid",
        "scope",
        "snmpv3",
        "switch_address",
    ]
    """links,authentication_method,comment,engine_id,name,owner.links,owner.name,owner.uuid,scope,snmpv3,switch_address,"""

    patchable_fields = [
        "comment",
    ]
    """comment,"""

    postable_fields = [
        "authentication_method",
        "comment",
        "engine_id",
        "name",
        "owner.name",
        "owner.uuid",
        "snmpv3",
        "switch_address",
    ]
    """authentication_method,comment,engine_id,name,owner.name,owner.uuid,snmpv3,switch_address,"""

class SnmpUser(Resource):
    r""" An SNMP user can be an SNMPv1/SNMPv2c user or an SNMPv3 user. SNMPv1/SNMPv2c user is also called a "community" user. An SNMPv3 user, also called a User-based Security Model (USM) user, can be a local SNMPv3 user or a remote SNMPv3 user. A local SNMPv3 user can be used for querying ONTAP SNMP server over SNMPv3 and/or for sending SNMPv3 traps. The local SNMPv3 user used for sending SNMPv3 traps must be configured with the same authentication and privacy credentials on the traphost receiver as well. A remote SNMPv3 user is also configured on a remote switch and used by ONTAP SNMP client functionality to query the remote switch over SNMPv3. An SNMP user is scoped to its owning Storage Virtual Machine (SVM). Owning SVM could be a data SVM or the administrative SVM. """

    _schema = SnmpUserSchema
    _path = "/api/support/snmp/users"
    _keys = ["engine_id", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the list of SNMP users on the cluster.
### Related ONTAP commands
* `security snmpusers`
* `security login show -application snmp`
### Learn more
* [`DOC /support/snmp/users`](#docs-support-support_snmp_users)
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
        """Returns a count of all SnmpUser resources that match the provided query"""
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
        """Returns a list of RawResources that represent SnmpUser resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["SnmpUser"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the comment parameter of an SNMP user.
### Optional properties
* `comment` - Comment text.
### Related ONTAP commands
* `security login modify`
### Learn more
* [`DOC /support/snmp/users/{engine_id}/{name}`](#docs-support-support_snmp_users_{engine_id}_{name})
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["SnmpUser"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SnmpUser"], NetAppResponse]:
        r"""Creates either a cluster-scoped or an SVM-scoped SNMP user. This user can be an SNMPv1 or SNMPv2c community user or an SNMPv3 user. An SNMPv3 user can be a local SNMPv3 user or a remote SNMPv3 user.
### Required properties
* `owner` - Name and UUID of owning SVM.
* `engine_id` - Engine ID of owning SVM or remote switch.
* `name` - SNMP user name
* `authentication_method` - Authentication method
### Optional properties
* `switch_address` - Optional remote switch address
* `snmpv3` - SNMPv3-specific credentials
* `comment` - Comment text
### Default property values
* `snmpv3.authentication_protocol` - none
* `snmpv3.privacy_protocol` - none
### Related ONTAP commands
* `security login create`
* `system snmp community add`
### Learn more
* [`DOC /support/snmp/users`](#docs-support-support_snmp_users)
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
        records: Iterable["SnmpUser"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an SNMP user. The engine ID can be the engine ID of the administrative SVM or a data SVM. It can also be the SNMPv3 engine ID of a remote switch.
### Related ONTAP commands
* `security login delete`
* `system snmp community delete`
### Learn more
* [`DOC /support/snmp/users/{engine_id}/{name}`](#docs-support-support_snmp_users_{engine_id}_{name})
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the list of SNMP users on the cluster.
### Related ONTAP commands
* `security snmpusers`
* `security login show -application snmp`
### Learn more
* [`DOC /support/snmp/users`](#docs-support-support_snmp_users)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the details of an SNMP user. The engine ID can be the engine ID of the administrative SVM or a data SVM. It can also be the SNMPv3 engine ID of a remote switch.
### Related ONTAP commands
* `security snmpusers -vserver <SVM Name> -username <User Name>`
* `security login show -application snmp -vserver <SVM Name> -user-or-group-name <User Name>`
### Learn more
* [`DOC /support/snmp/users/{engine_id}/{name}`](#docs-support-support_snmp_users_{engine_id}_{name})
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
        r"""Creates either a cluster-scoped or an SVM-scoped SNMP user. This user can be an SNMPv1 or SNMPv2c community user or an SNMPv3 user. An SNMPv3 user can be a local SNMPv3 user or a remote SNMPv3 user.
### Required properties
* `owner` - Name and UUID of owning SVM.
* `engine_id` - Engine ID of owning SVM or remote switch.
* `name` - SNMP user name
* `authentication_method` - Authentication method
### Optional properties
* `switch_address` - Optional remote switch address
* `snmpv3` - SNMPv3-specific credentials
* `comment` - Comment text
### Default property values
* `snmpv3.authentication_protocol` - none
* `snmpv3.privacy_protocol` - none
### Related ONTAP commands
* `security login create`
* `system snmp community add`
### Learn more
* [`DOC /support/snmp/users`](#docs-support-support_snmp_users)
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
        r"""Updates the comment parameter of an SNMP user.
### Optional properties
* `comment` - Comment text.
### Related ONTAP commands
* `security login modify`
### Learn more
* [`DOC /support/snmp/users/{engine_id}/{name}`](#docs-support-support_snmp_users_{engine_id}_{name})
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
        r"""Deletes an SNMP user. The engine ID can be the engine ID of the administrative SVM or a data SVM. It can also be the SNMPv3 engine ID of a remote switch.
### Related ONTAP commands
* `security login delete`
* `system snmp community delete`
### Learn more
* [`DOC /support/snmp/users/{engine_id}/{name}`](#docs-support-support_snmp_users_{engine_id}_{name})
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


