r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Application containers provision one or more storage objects. Currently, only NAS volumes are supported. Application containers allow you to specify the policies and rules for enabling and managing client access to storage. FlexCache volumes can also be provisioned.
## Examples
### Creating a FlexVol with NAS (NFS and CIFS access) along with S3 NAS bucket with S3 access policies
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Container

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Container()
    resource.svm = {"name": "vs0"}
    resource.volumes = [
        {
            "name": "vol1",
            "space": {"size": "100mb"},
            "scale_out": "false",
            "nas": {
                "path": "/vol1",
                "export_policy": {
                    "name": "vol1",
                    "rules": [
                        {
                            "clients": [{"match": "0.0.0.0/0"}],
                            "rw_rule": ["any"],
                            "ro_rule": ["any"],
                        }
                    ],
                },
                "cifs": {
                    "shares": [
                        {
                            "name": "vol1",
                            "acls": [
                                {
                                    "type": "windows",
                                    "permission": "full_control",
                                    "user_or_group": "everyone",
                                }
                            ],
                        }
                    ]
                },
            },
            "s3_bucket": {
                "name": "vol1",
                "nas_path": "/vol1",
                "policy": {
                    "statements": [
                        {
                            "actions": ["ListBucket"],
                            "effect": "allow",
                            "principals": ["user1", "group/grp1"],
                            "resources": ["vol1", "vol1/*"],
                        }
                    ]
                },
            },
        }
    ]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
Container(
    {
        "volumes": [
            {
                "s3_bucket": {
                    "policy": {
                        "statements": [
                            {
                                "effect": "allow",
                                "actions": ["ListBucket"],
                                "resources": ["vol1", "vol1/*"],
                                "principals": ["user1", "group/grp1"],
                            }
                        ]
                    },
                    "name": "vol1",
                    "nas_path": "/vol1",
                },
                "nas": {
                    "path": "/vol1",
                    "export_policy": {
                        "name": "vol1",
                        "rules": [
                            {
                                "ro_rule": ["any"],
                                "clients": [{"match": "0.0.0.0/0"}],
                                "rw_rule": ["any"],
                            }
                        ],
                    },
                    "cifs": {
                        "shares": [
                            {
                                "acls": [
                                    {
                                        "permission": "full_control",
                                        "user_or_group": "everyone",
                                        "type": "windows",
                                    }
                                ],
                                "name": "vol1",
                            }
                        ]
                    },
                },
                "space": {"size": 104857600},
                "scale_out": False,
                "name": "vol1",
            }
        ],
        "svm": {"name": "vs0"},
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


__all__ = ["Container", "ContainerSchema"]
__pdoc__ = {
    "ContainerSchema.resource": False,
    "ContainerSchema.opts": False,
}


class ContainerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Container object"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the container."""

    volumes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.container_volume.ContainerVolumeSchema", unknown=EXCLUDE, allow_none=True), data_key="volumes", allow_none=True)
    r""" A list of NAS volumes to provision.<br/>"""

    @property
    def resource(self):
        return Container

    gettable_fields = [
        "volumes",
    ]
    """volumes,"""

    patchable_fields = [
        "volumes",
    ]
    """volumes,"""

    postable_fields = [
        "svm.name",
        "svm.uuid",
        "volumes",
    ]
    """svm.name,svm.uuid,volumes,"""

class Container(Resource):
    """Allows interaction with Container objects on the host"""

    _schema = ContainerSchema
    _path = "/api/application/containers"



    @classmethod
    def post_collection(
        cls,
        records: Iterable["Container"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Container"], NetAppResponse]:
        r"""<personalities supports=asar2,unified>
* POST is not supported
</personalities>
<personalities supports=aiml>
Creates one or more of the following:
* New NAS FlexVol or FlexGroup volumes
* S3 buckets
* Access policies for NFS, CIFS and S3
* FlexCache volumes
## Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the container.
* `volumes`
## Naming Conventions
### Volume
  * volumes[].name, if specified
  * suffixed by "_#" where "#" is a system generated unique number, if provisioning_options.count is provided
</personalities>

### Learn more
* [`DOC /application/containers`](#docs-application-application_containers)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)




    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""<personalities supports=asar2,unified>
* POST is not supported
</personalities>
<personalities supports=aiml>
Creates one or more of the following:
* New NAS FlexVol or FlexGroup volumes
* S3 buckets
* Access policies for NFS, CIFS and S3
* FlexCache volumes
## Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the container.
* `volumes`
## Naming Conventions
### Volume
  * volumes[].name, if specified
  * suffixed by "_#" where "#" is a system generated unique number, if provisioning_options.count is provided
</personalities>

### Learn more
* [`DOC /application/containers`](#docs-application-application_containers)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)




