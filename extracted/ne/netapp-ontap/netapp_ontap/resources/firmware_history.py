r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Use this API to retrieve a history of firmware update requests. This API supports GET calls.
---
## Examples
### Retrieving history of firmware updates
The following example retrieves a history of firmware updates performed on the cluster.
Note that if the <i>fields=*</i> parameter is not specified, only the job ID and start time are returned.
Filters can be added on the fields to limit the results.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FirmwareHistory

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(FirmwareHistory.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    FirmwareHistory(
        {
            "job": {"uuid": "adf700c2-b50e-11ea-a54f-005056bbec43"},
            "start_time": "1970-01-01T00:02:03+00:00",
            "node": {"name": "node1", "uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ee"},
            "update_status": [
                {
                    "worker": {
                        "error": {
                            "message": "A firmware file already exists.",
                            "code": 2228327,
                        },
                        "state": "failed",
                        "node": {
                            "name": "node1",
                            "uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ee",
                        },
                    }
                },
                {
                    "worker": {
                        "error": {"message": "Success", "code": 0},
                        "state": "complete",
                        "node": {
                            "name": "node2",
                            "uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ef",
                        },
                    }
                },
            ],
            "_links": {
                "self": {
                    "href": "/api/cluster/firmware/history/1970-01-01T00%3A02%3A03-00%3A00/adf700c2-b50e-11ea-a54f-005056bbec43"
                }
            },
            "fw_update_state": "starting_workers",
            "fw_file_name": "all_disk_fw.zip",
            "end_time": "1970-01-01T00:07:36+00:00",
        }
    ),
    FirmwareHistory(
        {
            "job": {"uuid": "f84adabe-b50e-11ea-a54f-005056bbec43"},
            "start_time": "1970-01-01T00:02:03+00:00",
            "node": {"name": "node1", "uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ee"},
            "update_status": [
                {
                    "worker": {
                        "error": {
                            "message": "A firmware file already exists.",
                            "code": 2228327,
                        },
                        "state": "failed",
                        "node": {
                            "name": "node1",
                            "uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ee",
                        },
                    }
                },
                {
                    "worker": {
                        "error": {"message": "Success", "code": 0},
                        "state": "complete",
                        "node": {
                            "name": "node2",
                            "uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ef",
                        },
                    }
                },
            ],
            "_links": {
                "self": {
                    "href": "/api/cluster/firmware/history/1970-01-01T00%3A02%3A03-00%3A00/f84adabe-b50e-11ea-a54f-005056bbec43"
                }
            },
            "fw_update_state": "completed",
            "fw_file_name": "all_shelf_fw.zip",
            "end_time": "1970-01-01T00:07:36+00:00",
        }
    ),
]

```
</div>
</div>

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


__all__ = ["FirmwareHistory", "FirmwareHistorySchema"]
__pdoc__ = {
    "FirmwareHistorySchema.resource": False,
    "FirmwareHistorySchema.opts": False,
}


class FirmwareHistorySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FirmwareHistory object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the firmware_history."""

    end_time = ImpreciseDateTime(
        data_key="end_time",
        allow_none=True,
    )
    r""" End time of this update request.

Example: 2019-02-02T19:00:00.000+0000"""

    fw_file_name = marshmallow_fields.Str(
        data_key="fw_file_name",
        allow_none=True,
    )
    r""" Name of the firmware file.

Example: all_disk_fw.zip"""

    fw_update_state = marshmallow_fields.Str(
        data_key="fw_update_state",
        validate=enum_validation(['downloading', 'moving_firmware', 'starting_workers', 'waiting_on_workers', 'completed', 'failed']),
        allow_none=True,
    )
    r""" The fw_update_state field of the firmware_history.

Valid choices:

* downloading
* moving_firmware
* starting_workers
* waiting_on_workers
* completed
* failed"""

    job = marshmallow_fields.Nested("netapp_ontap.models.job_link.JobLinkSchema", data_key="job", unknown=EXCLUDE, allow_none=True)
    r""" The job field of the firmware_history."""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the firmware_history."""

    start_time = ImpreciseDateTime(
        data_key="start_time",
        allow_none=True,
    )
    r""" Start time of this update request.

Example: 2019-02-02T19:00:00.000+0000"""

    update_status = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.firmware_history_update_state.FirmwareHistoryUpdateStateSchema", unknown=EXCLUDE, allow_none=True), data_key="update_status", allow_none=True)
    r""" The update_status field of the firmware_history."""

    @property
    def resource(self):
        return FirmwareHistory

    gettable_fields = [
        "links",
        "end_time",
        "fw_file_name",
        "fw_update_state",
        "job",
        "node.links",
        "node.name",
        "node.uuid",
        "start_time",
        "update_status",
    ]
    """links,end_time,fw_file_name,fw_update_state,job,node.links,node.name,node.uuid,start_time,update_status,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class FirmwareHistory(Resource):
    """Allows interaction with FirmwareHistory objects on the host"""

    _schema = FirmwareHistorySchema
    _path = "/api/cluster/firmware/history"

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the history details for firmware update requests.
### Learn more
* [`DOC /cluster/firmware/history`](#docs-cluster-cluster_firmware_history)
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
        """Returns a count of all FirmwareHistory resources that match the provided query"""
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
        """Returns a list of RawResources that represent FirmwareHistory resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the history details for firmware update requests.
### Learn more
* [`DOC /cluster/firmware/history`](#docs-cluster-cluster_firmware_history)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






