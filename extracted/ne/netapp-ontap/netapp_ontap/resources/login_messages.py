r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to display and manage the login messages configuration. The GET request retrieves all of the login messages in the cluster. GET operations on /security/login/messages/{uuid} retrieve the login messages configuration by UUID. PATCH operations on /security/login/messages/{uuid} update the login messages configuration by UUID.
<br />
---
## Examples
### Retrieving all of the login messages in the cluster
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LoginMessages

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(LoginMessages.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    LoginMessages(
        {
            "banner": "*** WARNING: DO NOT PROCEED IF YOU ARE NOT AUTHORIZED! ****\n",
            "show_cluster_message": True,
            "message": "#### Welcome to Cluster X ####\n",
            "uuid": "2581e5aa-9fe3-11e8-b309-005056bbef18",
            "_links": {
                "self": {
                    "href": "/api/security/login/messages/2581e5aa-9fe3-11e8-b309-005056bbef18"
                }
            },
            "scope": "cluster",
        }
    ),
    LoginMessages(
        {
            "show_cluster_message": True,
            "message": "#### Welcome to SVM1 ####\n",
            "uuid": "7b1b3715-9ffa-11e8-a5dd-005056bbef18",
            "_links": {
                "self": {
                    "href": "/api/security/login/messages/7b1b3715-9ffa-11e8-a5dd-005056bbef18"
                }
            },
            "svm": {"name": "svm1", "uuid": "7b1b3715-9ffa-11e8-a5dd-005056bbef18"},
            "scope": "svm",
        }
    ),
    LoginMessages(
        {
            "banner": "*** WARNING: This system is for the use of authorized users only. ****\n",
            "uuid": "8ddee11e-a58c-11e8-85e0-005056bbef18",
            "_links": {
                "self": {
                    "href": "/api/security/login/messages/8ddee11e-a58c-11e8-85e0-005056bbef18"
                }
            },
            "svm": {"name": "svm3", "uuid": "8ddee11e-a58c-11e8-85e0-005056bbef18"},
            "scope": "svm",
        }
    ),
    LoginMessages(
        {
            "uuid": "f7e41c99-9ffa-11e8-a5dd-005056bbef18",
            "_links": {
                "self": {
                    "href": "/api/security/login/messages/f7e41c99-9ffa-11e8-a5dd-005056bbef18"
                }
            },
            "svm": {"name": "svm2", "uuid": "f7e41c99-9ffa-11e8-a5dd-005056bbef18"},
            "scope": "svm",
        }
    ),
]

```
</div>
</div>

---
### Retrieving the login messages configuration at the cluster scope
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LoginMessages

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(LoginMessages.get_collection(scope="cluster", fields="*")))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    LoginMessages(
        {
            "banner": "*** WARNING: DO NOT PROCEED IF YOU ARE NOT AUTHORIZED! ****\n",
            "show_cluster_message": True,
            "message": "#### Welcome to Cluster X ####\n",
            "uuid": "2581e5aa-9fe3-11e8-b309-005056bbef18",
            "_links": {
                "self": {
                    "href": "/api/security/login/messages/2581e5aa-9fe3-11e8-b309-005056bbef18"
                }
            },
            "scope": "cluster",
        }
    )
]

```
</div>
</div>

---
### Retrieving the login banner configured at the cluster scope
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LoginMessages

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(LoginMessages.get_collection(scope="cluster", fields="banner")))

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    LoginMessages(
        {
            "banner": "*** WARNING: DO NOT PROCEED IF YOU ARE NOT AUTHORIZED! ****\n",
            "uuid": "2581e5aa-9fe3-11e8-b309-005056bbef18",
            "_links": {
                "self": {
                    "href": "/api/security/login/messages/2581e5aa-9fe3-11e8-b309-005056bbef18"
                }
            },
            "scope": "cluster",
        }
    )
]

```
</div>
</div>

---
### Retrieving the login messages configuration of a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LoginMessages

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(LoginMessages.get_collection(fields="*", **{"svm.name": "svm1"})))

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
[
    LoginMessages(
        {
            "show_cluster_message": True,
            "message": "#### Welcome to SVM1 ####\n",
            "uuid": "7b1b3715-9ffa-11e8-a5dd-005056bbef18",
            "_links": {
                "self": {
                    "href": "/api/security/login/messages/7b1b3715-9ffa-11e8-a5dd-005056bbef18"
                }
            },
            "svm": {"name": "svm1", "uuid": "7b1b3715-9ffa-11e8-a5dd-005056bbef18"},
            "scope": "svm",
        }
    )
]

```
</div>
</div>

---
### Retrieving the login messages configuration by UUID, including all fields
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LoginMessages

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LoginMessages(uuid="7b1b3715-9ffa-11e8-a5dd-005056bbef18")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
LoginMessages(
    {
        "show_cluster_message": True,
        "message": "#### Welcome to SVM1 ####\n",
        "uuid": "7b1b3715-9ffa-11e8-a5dd-005056bbef18",
        "_links": {
            "self": {
                "href": "/api/security/login/messages/7b1b3715-9ffa-11e8-a5dd-005056bbef18"
            }
        },
        "svm": {"name": "svm1", "uuid": "7b1b3715-9ffa-11e8-a5dd-005056bbef18"},
        "scope": "svm",
    }
)

```
</div>
</div>

---
### Configuring the login banner in a cluster
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LoginMessages

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LoginMessages()
    resource.banner = "You are entering secure area."
    resource.patch(hydrate=True, scope="cluster")

```

---
### Configuring the message of the day (MOTD) in a cluster
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LoginMessages

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LoginMessages()
    resource.message = "Welcome to Cluster X"
    resource.show_cluster_message = True
    resource.patch(hydrate=True, scope="cluster")

```

---
### Clearing the login banner and message of the day (MOTD) in a cluster
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LoginMessages

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LoginMessages()
    resource.banner = ""
    resource.message = ""
    resource.patch(hydrate=True, scope="cluster")

```

---
### Configuring the login messages for a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LoginMessages

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LoginMessages()
    resource.banner = "AUTHORIZED ACCESS ONLY"
    resource.message = "WELCOME!"
    resource.patch(hydrate=True, **{"svm.name": "svm1"})

```

---
### Configuring the login messages by UUID
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LoginMessages

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LoginMessages(uuid="7b1b3715-9ffa-11e8-a5dd-005056bbef18")
    resource.banner = "AUTHORIZED ACCESS ONLY"
    resource.message = "WELCOME!"
    resource.patch()

```

---
### Clearing the login messages configuration by UUID
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LoginMessages

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LoginMessages(uuid="7b1b3715-9ffa-11e8-a5dd-005056bbef18")
    resource.banner = ""
    resource.message = ""
    resource.patch()

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


__all__ = ["LoginMessages", "LoginMessagesSchema"]
__pdoc__ = {
    "LoginMessagesSchema.resource": False,
    "LoginMessagesSchema.opts": False,
}


class LoginMessagesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LoginMessages object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the login_messages."""

    banner = marshmallow_fields.Str(
        data_key="banner",
        validate=len_validation(minimum=0, maximum=2048),
        allow_none=True,
    )
    r""" The login banner text. This message is displayed during SSH and console device
login just before the password prompt displays. When configured, a cluster-level
login banner is used for every incoming connection. Each data SVM can override
the cluster-level banner to instead display when you log into the SVM. To restore
the default setting for a data SVM, set the banner to an empty string.
New lines are supplied as either LF or CRLF but are always returned as LF.
Optional in the PATCH body."""

    message = marshmallow_fields.Str(
        data_key="message",
        validate=len_validation(minimum=0, maximum=2048),
        allow_none=True,
    )
    r""" The message of the day (MOTD). This message appears just before the clustershell
prompt after a successful login. When configured, the cluster message
displays first. If you log in as a data SVM administrator, the
SVM message is then printed. The cluster-level MOTD can be disabled
for a given data SVM using the "show_cluster_message" property.
New lines are supplied as either LF or CRLF but are always returned as LF.
Optional in the PATCH body."""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['svm', 'cluster']),
        allow_none=True,
    )
    r""" Set to "svm" for interfaces owned by an SVM. Otherwise, set to "cluster".

Valid choices:

* svm
* cluster"""

    show_cluster_message = marshmallow_fields.Boolean(
        data_key="show_cluster_message",
        allow_none=True,
    )
    r""" Specifies whether to show a cluster-level message before the SVM message
when logging in as an SVM administrator.
This setting can only be modified by cluster administrators.
Optional in the PATCH body."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the login_messages."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The unique identifier (ID) of the login messages configuration."""

    @property
    def resource(self):
        return LoginMessages

    gettable_fields = [
        "links",
        "banner",
        "message",
        "scope",
        "show_cluster_message",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """links,banner,message,scope,show_cluster_message,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
        "banner",
        "message",
        "show_cluster_message",
    ]
    """banner,message,show_cluster_message,"""

    postable_fields = [
        "banner",
        "message",
        "show_cluster_message",
        "svm.name",
        "svm.uuid",
    ]
    """banner,message,show_cluster_message,svm.name,svm.uuid,"""

class LoginMessages(Resource):
    r""" The login banner and message of the day (MOTD) configuration. """

    _schema = LoginMessagesSchema
    _path = "/api/security/login/messages"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the login banner and messages of the day (MOTD) configured in the cluster
and in specific SVMs.

### Learn more
* [`DOC /security/login/messages`](#docs-security-security_login_messages)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all LoginMessages resources that match the provided query"""
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
        """Returns a list of RawResources that represent LoginMessages resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["LoginMessages"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the login messages configuration.
There are no required fields. An empty body makes no modifications.

### Learn more
* [`DOC /security/login/messages`](#docs-security-security_login_messages)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the login banner and messages of the day (MOTD) configured in the cluster
and in specific SVMs.

### Learn more
* [`DOC /security/login/messages`](#docs-security-security_login_messages)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the login messages configuration by UUID.
### Learn more
* [`DOC /security/login/messages`](#docs-security-security_login_messages)"""
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
        r"""Updates the login messages configuration.
There are no required fields. An empty body makes no modifications.

### Learn more
* [`DOC /security/login/messages`](#docs-security-security_login_messages)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



