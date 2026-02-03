r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
FlexCache is a persistent cache of an origin volume. <br/>
FlexCache supports fan-out and more than one FlexCache can be created from one origin volume.
This API retrieves the connection status between cache and origin volumes.
## FlexCache APIs
The following APIs can be used to perform operations related to FlexCache connection status:

* GET       /api/storage/flexcache/connection-status
* GET       /api/storage/flexcache/connection-status/{node}/{svm}/{local_fg_msid}/{remote_svm_uuid}/{remote_vol_const_msid}
## Examples
### Retrieving flexcache connection-status of all volumes.
The GET request is used to retrieve connection-status between all origins and their corresponding FlexCache volumes.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConnectionStatus

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(ConnectionStatus.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    ConnectionStatus(
        {
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/connection-status/sti42-vsim-ucs511b/vs0/2150359768/a9161fea-73a0-11f0-85c5-005056a7bcdb/2150359767"
                }
            },
            "local_fg_msid": 2150359768,
            "remote_vol_const_msid": 2150359767,
            "node": "sti42-vsim-ucs511b",
            "remote_svm_uuid": "a9161fea-73a0-11f0-85c5-005056a7bcdb",
            "svm": "vs0",
        }
    ),
    ConnectionStatus(
        {
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/connection-status/sti42-vsim-ucs511d/vs0/2150359768/a9161fea-73a0-11f0-85c5-005056a7bcdb/2150359767"
                }
            },
            "local_fg_msid": 2150359768,
            "remote_vol_const_msid": 2150359767,
            "node": "sti42-vsim-ucs511d",
            "remote_svm_uuid": "a9161fea-73a0-11f0-85c5-005056a7bcdb",
            "svm": "vs0",
        }
    ),
    ConnectionStatus(
        {
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/connection-status/sti42-vsim-ucs511c/vs0/2150359767/a9161fea-73a0-11f0-85c5-005056a7bcdb/2150359769"
                }
            },
            "local_fg_msid": 2150359767,
            "remote_vol_const_msid": 2150359769,
            "node": "sti42-vsim-ucs511c",
            "remote_svm_uuid": "a9161fea-73a0-11f0-85c5-005056a7bcdb",
            "svm": "vs0",
        }
    ),
    ConnectionStatus(
        {
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/connection-status/sti42-vsim-ucs511c/vs0/2150359767/a9161fea-73a0-11f0-85c5-005056a7bcdb/2150359770"
                }
            },
            "local_fg_msid": 2150359767,
            "remote_vol_const_msid": 2150359770,
            "node": "sti42-vsim-ucs511c",
            "remote_svm_uuid": "a9161fea-73a0-11f0-85c5-005056a7bcdb",
            "svm": "vs0",
        }
    ),
    ConnectionStatus(
        {
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/connection-status/sti42-vsim-ucs511c/vs0/2150359767/a9161fea-73a0-11f0-85c5-005056a7bcdb/2150359771"
                }
            },
            "local_fg_msid": 2150359767,
            "remote_vol_const_msid": 2150359771,
            "node": "sti42-vsim-ucs511c",
            "remote_svm_uuid": "a9161fea-73a0-11f0-85c5-005056a7bcdb",
            "svm": "vs0",
        }
    ),
    ConnectionStatus(
        {
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/connection-status/sti42-vsim-ucs511c/vs0/2150359767/a9161fea-73a0-11f0-85c5-005056a7bcdb/2150359772"
                }
            },
            "local_fg_msid": 2150359767,
            "remote_vol_const_msid": 2150359772,
            "node": "sti42-vsim-ucs511c",
            "remote_svm_uuid": "a9161fea-73a0-11f0-85c5-005056a7bcdb",
            "svm": "vs0",
        }
    ),
    ConnectionStatus(
        {
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/connection-status/sti42-vsim-ucs511c/vs0/2150359767/a9161fea-73a0-11f0-85c5-005056a7bcdb/2150359773"
                }
            },
            "local_fg_msid": 2150359767,
            "remote_vol_const_msid": 2150359773,
            "node": "sti42-vsim-ucs511c",
            "remote_svm_uuid": "a9161fea-73a0-11f0-85c5-005056a7bcdb",
            "svm": "vs0",
        }
    ),
    ConnectionStatus(
        {
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/connection-status/sti42-vsim-ucs511c/vs0/2150359767/a9161fea-73a0-11f0-85c5-005056a7bcdb/2150359774"
                }
            },
            "local_fg_msid": 2150359767,
            "remote_vol_const_msid": 2150359774,
            "node": "sti42-vsim-ucs511c",
            "remote_svm_uuid": "a9161fea-73a0-11f0-85c5-005056a7bcdb",
            "svm": "vs0",
        }
    ),
    ConnectionStatus(
        {
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/connection-status/sti42-vsim-ucs511c/vs0/2150359767/a9161fea-73a0-11f0-85c5-005056a7bcdb/2150359775"
                }
            },
            "local_fg_msid": 2150359767,
            "remote_vol_const_msid": 2150359775,
            "node": "sti42-vsim-ucs511c",
            "remote_svm_uuid": "a9161fea-73a0-11f0-85c5-005056a7bcdb",
            "svm": "vs0",
        }
    ),
    ConnectionStatus(
        {
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/connection-status/sti42-vsim-ucs511c/vs0/2150359767/a9161fea-73a0-11f0-85c5-005056a7bcdb/2150359776"
                }
            },
            "local_fg_msid": 2150359767,
            "remote_vol_const_msid": 2150359776,
            "node": "sti42-vsim-ucs511c",
            "remote_svm_uuid": "a9161fea-73a0-11f0-85c5-005056a7bcdb",
            "svm": "vs0",
        }
    ),
    ConnectionStatus(
        {
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/connection-status/sti42-vsim-ucs511c/vs0/2150359767/a9161fea-73a0-11f0-85c5-005056a7bcdb/2150359777"
                }
            },
            "local_fg_msid": 2150359767,
            "remote_vol_const_msid": 2150359777,
            "node": "sti42-vsim-ucs511c",
            "remote_svm_uuid": "a9161fea-73a0-11f0-85c5-005056a7bcdb",
            "svm": "vs0",
        }
    ),
    ConnectionStatus(
        {
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/connection-status/sti42-vsim-ucs511c/vs0/2150359767/a9161fea-73a0-11f0-85c5-005056a7bcdb/2150359778"
                }
            },
            "local_fg_msid": 2150359767,
            "remote_vol_const_msid": 2150359778,
            "node": "sti42-vsim-ucs511c",
            "remote_svm_uuid": "a9161fea-73a0-11f0-85c5-005056a7bcdb",
            "svm": "vs0",
        }
    ),
    ConnectionStatus(
        {
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/connection-status/sti42-vsim-ucs511c/vs0/2150359767/a9161fea-73a0-11f0-85c5-005056a7bcdb/2150359779"
                }
            },
            "local_fg_msid": 2150359767,
            "remote_vol_const_msid": 2150359779,
            "node": "sti42-vsim-ucs511c",
            "remote_svm_uuid": "a9161fea-73a0-11f0-85c5-005056a7bcdb",
            "svm": "vs0",
        }
    ),
    ConnectionStatus(
        {
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/connection-status/sti42-vsim-ucs511c/vs0/2150359767/a9161fea-73a0-11f0-85c5-005056a7bcdb/2150359780"
                }
            },
            "local_fg_msid": 2150359767,
            "remote_vol_const_msid": 2150359780,
            "node": "sti42-vsim-ucs511c",
            "remote_svm_uuid": "a9161fea-73a0-11f0-85c5-005056a7bcdb",
            "svm": "vs0",
        }
    ),
    ConnectionStatus(
        {
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/connection-status/sti42-vsim-ucs511c/vs0/2150359768/a9161fea-73a0-11f0-85c5-005056a7bcdb/2150359767"
                }
            },
            "local_fg_msid": 2150359768,
            "remote_vol_const_msid": 2150359767,
            "node": "sti42-vsim-ucs511c",
            "remote_svm_uuid": "a9161fea-73a0-11f0-85c5-005056a7bcdb",
            "svm": "vs0",
        }
    ),
    ConnectionStatus(
        {
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/connection-status/sti42-vsim-ucs511a/vs0/2150359768/a9161fea-73a0-11f0-85c5-005056a7bcdb/2150359767"
                }
            },
            "local_fg_msid": 2150359768,
            "remote_vol_const_msid": 2150359767,
            "node": "sti42-vsim-ucs511a",
            "remote_svm_uuid": "a9161fea-73a0-11f0-85c5-005056a7bcdb",
            "svm": "vs0",
        }
    ),
]

```
</div>
</div>

### Retrieving a single flexcache connection status
The GET request is used to retrieve a specific connection status between 2 volumes.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConnectionStatus

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConnectionStatus(
        remote_vol_const_msid=2150359767,
        remote_svm_uuid="a9161fea-73a0-11f0-85c5-005056a7bcdb",
        local_fg_msid=2150359768,
        svm="vs0",
        node="sti42-vsim-ucs511c",
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
ConnectionStatus(
    {
        "_links": {
            "self": {
                "href": "/api/storage/flexcache/connection-status/sti42-vsim-ucs511c/vs0/2150359768/a9161fea-73a0-11f0-85c5-005056a7bcdb/2150359767"
            }
        },
        "local_fg_msid": 2150359768,
        "remote_svm": "vs0",
        "volume": "fc0",
        "remote_cluster": "C1_sti42-vsim-ucs511a_1754576895",
        "conn_state": "connected",
        "remote_vol_const_msid": 2150359767,
        "remote_volume": "vol0",
        "svm_uuid": "a9161fea-73a0-11f0-85c5-005056a7bcdb",
        "node": "sti42-vsim-ucs511c",
        "remote_endpoint": "origin",
        "last_update_time": "2025-08-07T11:39:31-04:00",
        "remote_svm_uuid": "a9161fea-73a0-11f0-85c5-005056a7bcdb",
        "svm": "vs0",
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


__all__ = ["ConnectionStatus", "ConnectionStatusSchema"]
__pdoc__ = {
    "ConnectionStatusSchema.resource": False,
    "ConnectionStatusSchema.opts": False,
}

class ConnectionStatusSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConnectionStatus object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the connection_status."""

    conn_state = marshmallow_fields.Str(
        data_key="conn_state",
        validate=enum_validation(['connected', 'disconnected', 'downrev', 'unknown']),
        allow_none=True,
    )
    r""" Connection Status between the Flexcache and Origin volumes.

Valid choices:

* connected
* disconnected
* downrev
* unknown"""

    last_update_time = ImpreciseDateTime(
        data_key="last_update_time",
        allow_none=True,
    )
    r""" Last update time of the connection status.

Example: 2018-06-04T19:00:00.000+0000"""

    local_fg_msid = Size(
        data_key="local_fg_msid",
        allow_none=True,
    )
    r""" The local volume's Master Set ID."""

    node = marshmallow_fields.Str(
        data_key="node",
        allow_none=True,
    )
    r""" Name of the node."""

    remote_cluster = marshmallow_fields.Str(
        data_key="remote_cluster",
        allow_none=True,
    )
    r""" Remote cluster."""

    remote_endpoint = marshmallow_fields.Str(
        data_key="remote_endpoint",
        validate=enum_validation(['cache', 'none', 'origin']),
        allow_none=True,
    )
    r""" Remote endpoint type.

Valid choices:

* cache
* none
* origin"""

    remote_svm = marshmallow_fields.Str(
        data_key="remote_svm",
        allow_none=True,
    )
    r""" Remote volume SVM."""

    remote_svm_uuid = marshmallow_fields.Str(
        data_key="remote_svm_uuid",
        allow_none=True,
    )
    r""" Remote SVM UUID."""

    remote_vol_const_msid = Size(
        data_key="remote_vol_const_msid",
        allow_none=True,
    )
    r""" Remote volume's Master Set ID."""

    remote_volume = marshmallow_fields.Str(
        data_key="remote_volume",
        allow_none=True,
    )
    r""" Remote Volume name."""

    svm = marshmallow_fields.Str(
        data_key="svm",
        allow_none=True,
    )
    r""" Volume SVM."""

    svm_uuid = marshmallow_fields.Str(
        data_key="svm_uuid",
        allow_none=True,
    )
    r""" Local SVM UUID."""

    volume = marshmallow_fields.Str(
        data_key="volume",
        allow_none=True,
    )
    r""" Local Volume name."""

    @property
    def resource(self):
        return ConnectionStatus

    gettable_fields = [
        "links",
        "conn_state",
        "last_update_time",
        "local_fg_msid",
        "node",
        "remote_cluster",
        "remote_endpoint",
        "remote_svm",
        "remote_svm_uuid",
        "remote_vol_const_msid",
        "remote_volume",
        "svm",
        "svm_uuid",
        "volume",
    ]
    """links,conn_state,last_update_time,local_fg_msid,node,remote_cluster,remote_endpoint,remote_svm,remote_svm_uuid,remote_vol_const_msid,remote_volume,svm,svm_uuid,volume,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class ConnectionStatus(Resource):
    r""" FlexCache Connection Status Endpoint """

    _schema = ConnectionStatusSchema
    _path = "/api/storage/flexcache/connection-status"
    _keys = ["node", "svm", "local_fg_msid", "remote_svm_uuid", "remote_vol_const_msid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves attributes of the connection status between cache and origin volumes.
### Related ONTAP commands
* `volume flexcache connection-status show`
### Learn more
* [`DOC /storage/flexcache/connection-status`](#docs-storage-storage_flexcache_connection-status)
Retrieves origin of FlexCache in the cluster.
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
        """Returns a count of all ConnectionStatus resources that match the provided query"""
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
        """Returns a list of RawResources that represent ConnectionStatus resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves attributes of the connection status between cache and origin volumes.
### Related ONTAP commands
* `volume flexcache connection-status show`
### Learn more
* [`DOC /storage/flexcache/connection-status`](#docs-storage-storage_flexcache_connection-status)
Retrieves origin of FlexCache in the cluster.
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves connection status between a cache and origin volume.
### Related ONTAP commands
* `volume flexcache connection-status show`
### Learn more
* [`DOC /storage/flexcache/connection-status`](#docs-storage-storage_flexcache_connection-status)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





