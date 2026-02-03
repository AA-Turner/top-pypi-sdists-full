r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this endpoint to retrieve the DCN software package information for a specific UUID from the ONTAP cluster, initiate DCN cluster software upgrade with a previously uploaded package and retrieve the DCN cluster software upgrade status.
<br/>
## Examples
### Retrieving cluster software package information
The following example shows how to retrieve information of a specific DCN software package and to monitor the status of DCN cluster software upgrade, using UUID of the package.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import DcnClusterSoftwarePackage

with HostConnection(
    "<mgmt-ip>", username="username", password="password", verify=False
):
    resource = DcnClusterSoftwarePackage(uuid="f0ce5ac2-3347-4fa9-9335-ff8f2212bdad")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
DcnClusterSoftwarePackage(
    {
        "version": {
            "minor": 1,
            "major": 18,
            "generation": 9,
            "full": "9.18.1U0 Wed Jan 15 18:20:57 UTC 2026",
            "patch": "U0",
        },
        "staged": False,
        "state": "available",
        "size": 38777467320,
        "compatible": True,
        "create_time": "2025-10-14T16:50:21-04:00",
        "uuid": "f0ce5ac2-3347-4fa9-9335-ff8f2212bdad",
    }
)

```
</div>
</div>

---
The following example shows how to initiate an upgrade of the DCN cluster.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import DcnClusterSoftwarePackage

with HostConnection(
    "<mgmt-ip>", username="username", password="password", verify=False
):
    resource = DcnClusterSoftwarePackage(uuid="f0ce5ac2-3347-4fa9-9335-ff8f2212bdad")
    resource.staged = True
    resource.patch()

```

# The API:
/api/dcn/cluster/software/packages/{uuid}
# The request
curl -ku username:password -X GET "https://<mgmt-ip>/api/dcn/cluster/software/packages/f0ce5ac2-3347-4fa9-9335-ff8f2212bdad"
# The response:
200 - OK
{
  "_links": {
    "self": {
      "href": "/api/dcn/cluster/software/packages/f0ce5ac2-3347-4fa9-9335-ff8f2212bdad"
    }
  },
  "compatible": true,
  "create_time": "2025-10-14T16:50:21-04:00",
  "install_status": {
    "active": true,
    "duration": "PT90M1S",
    "message": "Node: sti-s44nl-058 (ec0d65ea-318d-11f0-bd9a-9082c3027ea1), State: running | Node: sti-s44nl-059 (960d6c6c-3183-11f0-815c-9082c3027e8d), State: success | Node: sti-s44nl-060 (35956352-318e-11f0-9084-9082c3027eae), State: success",
    "start_time": "2025-10-14T17:50:23-04:00"
  },
  "size": 38777467320,
  "staged": true,
  "state": "installing",
  "uuid": "f0ce5ac2-3347-4fa9-9335-ff8f2212bdad",
  "version": {
    "full": "9.18.1U0 Wed Jan 15 18:20:57 UTC 2026",
    "generation": 9,
    "major": 18,
    "minor": 1,
    "patch": "U0"
  }
}"""

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


__all__ = ["DcnClusterSoftwarePackage", "DcnClusterSoftwarePackageSchema"]
__pdoc__ = {
    "DcnClusterSoftwarePackageSchema.resource": False,
    "DcnClusterSoftwarePackageSchema.opts": False,
}

class DcnClusterSoftwarePackageSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnClusterSoftwarePackage object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.application_nvme_access_subsystem_map_subsystem_hosts_links", "ApplicationNvmeAccessSubsystemMapSubsystemHostsLinksSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the dcn_cluster_software_package."""

    compatible = marshmallow_fields.Boolean(
        data_key="compatible",
        allow_none=True,
    )
    r""" DCN software compatibility with ONTAP.

Example: true"""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" Indicates when this package was placed on the system.

Example: 2025-05-20T19:00:00.000+0000"""

    install_status = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_cluster_software_install_status", "DcnClusterSoftwareInstallStatusSchema"),
                data_key="install_status",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The install_status field of the dcn_cluster_software_package."""

    size = Size(
        data_key="size",
        allow_none=True,
    )
    r""" Size of the package in bytes.

Example: 5368709120"""

    staged = marshmallow_fields.Boolean(
        data_key="staged",
        allow_none=True,
    )
    r""" True if this software package is currently pending for upgrade. Set to true to start the upgrade.

Example: true"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['available', 'validating', 'valid', 'invalid', 'unavailable', 'installing', 'installed', 'install_failed', 'processing', 'downloading']),
        allow_none=True,
    )
    r""" Current status of the package.

Valid choices:

* available
* validating
* valid
* invalid
* unavailable
* installing
* installed
* install_failed
* processing
* downloading"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" UUID of this entry.

Example: f0ce5ac2-3347-4fa9-9335-ff8f2212bdad"""

    version = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_version", "DcnVersionSchema"),
                data_key="version",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" This contains DCN version information."""

    @property
    def resource(self):
        return DcnClusterSoftwarePackage

    gettable_fields = [
        "links",
        "compatible",
        "create_time",
        "install_status",
        "size",
        "staged",
        "state",
        "uuid",
        "version",
    ]
    """links,compatible,create_time,install_status,size,staged,state,uuid,version,"""

    patchable_fields = [
        "staged",
    ]
    """staged,"""

    postable_fields = [
    ]
    """"""

class DcnClusterSoftwarePackage(Resource):
    """Allows interaction with DcnClusterSoftwarePackage objects on the host"""

    _schema = DcnClusterSoftwarePackageSchema
    _path = "/api/dcn/cluster/software/packages"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the DCN software packages on the ONTAP cluster.

### Learn more
* [`DOC /dcn/cluster/software/packages`](#docs-dcn-dcn_cluster_software_packages)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all DcnClusterSoftwarePackage resources that match the provided query"""
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
        """Returns a list of RawResources that represent DcnClusterSoftwarePackage resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["DcnClusterSoftwarePackage"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Triggers an update of the DCN cluster with the previously uploaded DCN software.
Important note:
  * Setting 'staged' to true triggers the DCN cluster upgrade.

### Learn more
* [`DOC /dcn/cluster/software/packages/{uuid}`](#docs-dcn-dcn_cluster_software_packages_{uuid})"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the DCN software packages on the ONTAP cluster.

### Learn more
* [`DOC /dcn/cluster/software/packages`](#docs-dcn-dcn_cluster_software_packages)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the DCN software package information for a specified package UUID.

### Learn more
* [`DOC /dcn/cluster/software/packages/{uuid}`](#docs-dcn-dcn_cluster_software_packages_{uuid})"""
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
        r"""Triggers an update of the DCN cluster with the previously uploaded DCN software.
Important note:
  * Setting 'staged' to true triggers the DCN cluster upgrade.

### Learn more
* [`DOC /dcn/cluster/software/packages/{uuid}`](#docs-dcn-dcn_cluster_software_packages_{uuid})"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



