r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Licensing allows you to tailor a system to meet an organization's specific needs. You can enable new features by purchasing a license from a NetApp sales associate. After installation of the license, the new feature is available immediately.
###
This interface manages licenses according to their supported feature. By default, the interface displays packages with installed licenses, but you can also return unlicensed packages.
###
Each feature has a compliance state that is indicated at the package level. Individual licenses also contain a compliance state indicated in the "licenses" array. The state of the package is determined by analyzing the underlying licenses according to the following criteria:

* Licensing terms
* Cluster state
### Licensing terms
The licensing terms define the conditions under which a package is considered "compliant". Individual licenses are evaluated based on the following:

* Scope
* Time period
* Usage
#### Scope
A package can be licensed under the following scopes:

* Site - Permits the feature to be used by any node in any cluster.
* Cluster - Permits the feature to be used by any node in a single specific cluster.
* Node - Permits the authorized node to use the feature. Within a cluster, if you don't supply every node with a valid license, the package state indicates "noncompliant". You must purchase a license for each node in a cluster for the package to be considered "compliant".
#### Time period
Some package licenses are only valid for a limited period of time. After a license has expired, the package state changes to "noncompliant". You need to purchase a new license for the package to return to a "compliant" state.
###
#### Usage
Some package licenses have additional terms that need to be maintained to keep a license in compliance. These conditions are defined by the individual license. For example, a license might define the maximum amount of storage that a node can allocate for the license to be "compliant".
###
### Cluster state
A cluster's state consists of the following:

* Node online status
* Node cluster membership
####
Some features require that a node be online to display a valid compliance state. If a node cannot be reached or is not known to the cluster, the individual license might indicate an "unknown" state.
####
_______
## Licensing keys
A license is issued in one of the following three formats:

  * 28-character key
  * NetApp License File Version 1 (NLFv1)
  * NetApp License File Version 2 (NLFv2)
#### Overview of NLFv1 and NLFv2 License Formats
NLFv1 and NLFv2 licenses are both JSON based files that allow features to be enabled.
####
The difference between the two formats is that a NLFv2 license allows multiple features to be enabled with a single file. A NLFv1 license is capable of enabling a single feature.
###
These licenses are identified, in the various methods, as follows:
###
| Format           | Identifying Keys                           |
| -----------------| -------------------------------------------|
| 28 Character Key | name / serial_number                       |
| NLFv1            | name / serial_number                       |
| NLFv2            | licenses.installed_license / serial_number |
###
The following is an example of a 28-character key:
####
```
AMEPOSOIKLKGEEEEDGNDEKSJDEEE
```
####
The following is an example of an NLFv1 key:
####
```JSON
{
  "statusResp": {
  "version": "1",
  "serialNumber": "123456789",
  "message": "Success",
  "licenses": {
    "capacity": "1",
    "type": "capacity",
    "licenseProtocol": "FABRICPOOL-TB",
    "package": "FabricPool",
    "licenseScope": "cluster"
  },
  "snStatus": "Active",
  "product": "fabricpool",
  "statusCode": "S007"
  },
  "Signature": "signatureABC"
}
```
####
The following is an example of an NLFv2 key:
####
```JSON
{
  "statusResp": {
  "version": "2",
  "serialNumber": "123456789",
  "message": "Success",
  "product": "Sample NLFv2 License",
  "licenses": {
    "capacity": "1",
    "type": "capacity",
    "HostID": "5554444",
    "package": [ "NFS", "CIFS" ],
    "licenseScope": "node"
  },
  "snStatus": "Active",
  "statusCode": "S007"
  },
  "Signature": "signatureABC"
}
```
###
You can use this API to submit any format to enable features.
###
_______
## Examples
### Retrieving a collection of licenses organized by package
This example retrieves a collection that contains one entry for each package (filtered to only the 'fabricpool' package).
####
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LicensePackage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(LicensePackage.get_collection(fields="*", name="fabricpool")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    LicensePackage(
        {
            "licenses": [
                {
                    "serial_number": "4149027342",
                    "capacity": {"used_size": 0, "maximum_size": 1099511627776},
                    "owner": "testcluster-1",
                }
            ],
            "description": "FabricPool License",
            "name": "fabricpool",
            "state": "compliant",
            "_links": {"self": {"href": "/api/cluster/licensing/licenses/fabricpool"}},
            "scope": "cluster",
        }
    )
]

```
</div>
</div>

### Retrieving a collection of licenses organized by package - for package cloud
The following example retrieves a collection that contains one entry for each package (filtered to only the
'cloud' package). The cloud package, in this example, is in the enforcement period as the license has expired.
The REST GET output displays an additional field 'shutdown_imminent' to indicate that the system will shutdown.
####
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LicensePackage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(LicensePackage.get_collection(fields="*", name="cloud")))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    LicensePackage(
        {
            "licenses": [
                {
                    "expiry_time": "2021-10-26T19:57:41+00:00",
                    "active": False,
                    "serial_number": "90120130000000000001",
                    "evaluation": True,
                    "owner": "test-vsim1",
                    "compliance": {"state": "noncompliant"},
                    "shutdown_imminent": True,
                }
            ],
            "entitlement": {"action": "acquire_license", "risk": "unlicensed"},
            "description": "Cloud ONTAP License",
            "name": "cloud",
            "state": "noncompliant",
            "_links": {"self": {"href": "/api/cluster/licensing/licenses/cloud"}},
            "scope": "node",
        }
    )
]

```
</div>
</div>

### Retrieving a collection of licenses installed with NLFv2
This example retrieves a collection of licenses that were installed by a NLFv2 formatted license.
####
**Note:** The license is referenced by the installed license "Core*Bundle" and the license serial number "4212426890"
####
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LicensePackage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            LicensePackage.get_collection(
                fields="*",
                serial_number=4212426890,
                **{"licenses.installed_license": "Core*Bundle"}
            )
        )
    )

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    LicensePackage(
        {
            "licenses": [
                {
                    "active": False,
                    "evaluation": False,
                    "owner": "test-vsim3",
                    "compliance": {"state": "unlicensed"},
                },
                {
                    "active": True,
                    "serial_number": "4212426890",
                    "evaluation": False,
                    "installed_license": "Core Bundle",
                    "capacity": {"maximum_size": 10995116277760},
                    "owner": "test-vsim4",
                    "host_id": "4212426890",
                    "compliance": {"state": "compliant"},
                },
            ],
            "entitlement": {"action": "acquire_license", "risk": "medium"},
            "description": "NFS License",
            "name": "nfs",
            "state": "noncompliant",
            "_links": {
                "self": {
                    "href": "/api/cluster/licensing/licenses/nfs/?licenses.installed_license=Core*Bundle"
                }
            },
            "scope": "node",
        }
    ),
    LicensePackage(
        {
            "licenses": [
                {
                    "active": False,
                    "evaluation": False,
                    "owner": "test-vsim3",
                    "compliance": {"state": "unlicensed"},
                },
                {
                    "active": True,
                    "serial_number": "4212426890",
                    "evaluation": False,
                    "installed_license": "Core Bundle",
                    "capacity": {"maximum_size": 10995116277760},
                    "owner": "test-vsim4",
                    "host_id": "4212426890",
                    "compliance": {"state": "compliant"},
                },
            ],
            "entitlement": {"action": "acquire_license", "risk": "medium"},
            "description": "CIFS License",
            "name": "cifs",
            "state": "noncompliant",
            "_links": {
                "self": {
                    "href": "/api/cluster/licensing/licenses/cifs/?licenses.installed_license=Core*Bundle"
                }
            },
            "scope": "node",
        }
    ),
    LicensePackage(
        {
            "licenses": [
                {
                    "active": False,
                    "evaluation": False,
                    "owner": "test-vsim3",
                    "compliance": {"state": "unlicensed"},
                },
                {
                    "active": True,
                    "serial_number": "4212426890",
                    "evaluation": False,
                    "installed_license": "Core Bundle",
                    "capacity": {"maximum_size": 10995116277760},
                    "owner": "test-vsim4",
                    "host_id": "4212426890",
                    "compliance": {"state": "compliant"},
                },
            ],
            "entitlement": {"action": "acquire_license", "risk": "medium"},
            "description": "iSCSI License",
            "name": "iscsi",
            "state": "noncompliant",
            "_links": {
                "self": {
                    "href": "/api/cluster/licensing/licenses/iscsi/?licenses.installed_license=Core*Bundle"
                }
            },
            "scope": "node",
        }
    ),
    LicensePackage(
        {
            "licenses": [
                {
                    "active": False,
                    "evaluation": False,
                    "owner": "test-vsim3",
                    "compliance": {"state": "unlicensed"},
                },
                {
                    "active": True,
                    "serial_number": "4212426890",
                    "evaluation": False,
                    "installed_license": "Core Bundle",
                    "capacity": {"maximum_size": 10995116277760},
                    "owner": "test-vsim4",
                    "host_id": "4212426890",
                    "compliance": {"state": "compliant"},
                },
            ],
            "entitlement": {"action": "acquire_license", "risk": "medium"},
            "description": "FCP License",
            "name": "fcp",
            "state": "noncompliant",
            "_links": {
                "self": {
                    "href": "/api/cluster/licensing/licenses/fcp/?licenses.installed_license=Core*Bundle"
                }
            },
            "scope": "node",
        }
    ),
    LicensePackage(
        {
            "licenses": [
                {
                    "active": False,
                    "evaluation": False,
                    "owner": "test-vsim3",
                    "compliance": {"state": "unlicensed"},
                },
                {
                    "active": True,
                    "serial_number": "4212426890",
                    "evaluation": False,
                    "installed_license": "Core Bundle",
                    "capacity": {"maximum_size": 10995116277760},
                    "owner": "test-vsim4",
                    "host_id": "4212426890",
                    "compliance": {"state": "compliant"},
                },
            ],
            "entitlement": {"action": "acquire_license", "risk": "medium"},
            "description": "SnapRestore License",
            "name": "snaprestore",
            "state": "noncompliant",
            "_links": {
                "self": {
                    "href": "/api/cluster/licensing/licenses/snaprestore/?licenses.installed_license=Core*Bundle"
                }
            },
            "scope": "node",
        }
    ),
    LicensePackage(
        {
            "licenses": [
                {
                    "active": False,
                    "evaluation": False,
                    "owner": "test-vsim3",
                    "compliance": {"state": "unlicensed"},
                },
                {
                    "active": True,
                    "serial_number": "4212426890",
                    "evaluation": False,
                    "installed_license": "Core Bundle",
                    "capacity": {"maximum_size": 10995116277760},
                    "owner": "test-vsim4",
                    "host_id": "4212426890",
                    "compliance": {"state": "compliant"},
                },
            ],
            "entitlement": {"action": "acquire_license", "risk": "medium"},
            "description": "FlexClone License",
            "name": "flexclone",
            "state": "noncompliant",
            "_links": {
                "self": {
                    "href": "/api/cluster/licensing/licenses/flexclone/?licenses.installed_license=Core*Bundle"
                }
            },
            "scope": "node",
        }
    ),
    LicensePackage(
        {
            "licenses": [
                {
                    "active": False,
                    "evaluation": False,
                    "owner": "test-vsim3",
                    "compliance": {"state": "unlicensed"},
                },
                {
                    "active": True,
                    "serial_number": "4212426890",
                    "evaluation": False,
                    "installed_license": "Core Bundle",
                    "capacity": {"maximum_size": 10995116277760},
                    "owner": "test-vsim4",
                    "host_id": "4212426890",
                    "compliance": {"state": "compliant"},
                },
            ],
            "description": "NVMe-oF License",
            "name": "nvme_of",
            "state": "noncompliant",
            "_links": {
                "self": {
                    "href": "/api/cluster/licensing/licenses/nvme_of/?licenses.installed_license=Core*Bundle"
                }
            },
            "scope": "node",
        }
    ),
    LicensePackage(
        {
            "licenses": [
                {
                    "active": False,
                    "evaluation": False,
                    "owner": "test-vsim3",
                    "compliance": {"state": "unlicensed"},
                },
                {
                    "active": True,
                    "serial_number": "4212426890",
                    "evaluation": False,
                    "installed_license": "Core Bundle",
                    "capacity": {"maximum_size": 10995116277760},
                    "owner": "test-vsim4",
                    "host_id": "4212426890",
                    "compliance": {"state": "compliant"},
                },
            ],
            "entitlement": {"action": "acquire_license", "risk": "medium"},
            "description": "S3 License",
            "name": "s3",
            "state": "noncompliant",
            "_links": {
                "self": {
                    "href": "/api/cluster/licensing/licenses/s3/?licenses.installed_license=Core*Bundle"
                }
            },
            "scope": "node",
        }
    ),
]

```
</div>
</div>

### Retrieving a collection of installed licenses
This example retrieves a collection containing all packages (except base) that have installed licenses.
####
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LicensePackage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(LicensePackage.get_collection(fields="*", name="!base")))

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
[
    LicensePackage(
        {
            "licenses": [
                {
                    "serial_number": "1-81-0000000000000004149027492",
                    "owner": "testcluster-1",
                }
            ],
            "entitlement": {"action": "none", "risk": "low"},
            "description": "NFS License",
            "name": "nfs",
            "state": "compliant",
            "_links": {"self": {"href": "/api/cluster/licensing/licenses/nfs"}},
            "scope": "node",
        }
    ),
    LicensePackage(
        {
            "licenses": [
                {
                    "serial_number": "1-81-0000000000000004149027492",
                    "owner": "testcluster-1",
                }
            ],
            "entitlement": {"action": "acquire_license", "risk": "medium"},
            "description": "CIFS License",
            "name": "cifs",
            "state": "compliant",
            "_links": {"self": {"href": "/api/cluster/licensing/licenses/cifs"}},
            "scope": "node",
        }
    ),
]

```
</div>
</div>

### Retrieving a collection of unlicensed packages
By default, unlicensed packages are filtered from the collection output. This example shows how to use a query to retrieve unlicensed packages.
####
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LicensePackage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(LicensePackage.get_collection(name="flexcache", state="unlicensed")))

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
[
    LicensePackage(
        {
            "name": "flexcache",
            "_links": {"self": {"href": "/api/cluster/licensing/licenses/flexcache"}},
        }
    )
]

```
</div>
</div>

### Installing a NLF license
This example installs a single NLFv1 license. A NLFv2 license installs using the same procedure.
###
**Note:** You must escape all the double quotes and backslash characters of the JSON license before it can be placed in the POST request.
####
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LicensePackage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LicensePackage()
    resource.post(hydrate=True)
    print(resource)

```

### Installing a 28-character key
This example installs a single 28-character key formatted license.
####
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LicensePackage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LicensePackage()
    resource.post(hydrate=True)
    print(resource)

```

### Installing multiple licenses with one API call
This example shows how multiple keys can be provided to install multiple features in a single API call.
####
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LicensePackage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LicensePackage()
    resource.post(hydrate=True)
    print(resource)

```


### Retrieving information for a specific license package
This example shows how to retrieve information about the specific feature package `fabricpool`.
####
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LicensePackage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LicensePackage(name="fabricpool")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example8_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example8_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example8_result" class="try_it_out_content">
```
LicensePackage(
    {
        "licenses": [
            {
                "serial_number": "123456789",
                "capacity": {"used_size": 0, "maximum_size": 109951162777600},
                "owner": "testcluster-1",
            }
        ],
        "description": "FabricPool License",
        "name": "fabricpool",
        "state": "compliant",
        "_links": {"self": {"href": "/api/cluster/licensing/licenses/fabricpool/"}},
        "scope": "cluster",
    }
)

```
</div>
</div>

### Deleting a specific license
This example show how to delete a CIFS site license.
####
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LicensePackage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LicensePackage(name="cifs")
    resource.delete(serial_number="1-80-000011")

```

### Deleting with a query
####
The following example shows how to delete all NFS licenses specified with the '*' query.
####
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LicensePackage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LicensePackage(name="nfs")
    resource.delete(serial_number="*")

```

### Deleting all licenses installed with NLFv2
####
The following example shows how to delete all licenses installed by a NLFv2 formatted license.
####
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LicensePackage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LicensePackage()
    resource.delete(
        serial_number="4149026-97-8", **{"licenses.installed_license": "Core*Bundle"}
    )

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


__all__ = ["LicensePackage", "LicensePackageSchema"]
__pdoc__ = {
    "LicensePackageSchema.resource": False,
    "LicensePackageSchema.opts": False,
}


class LicensePackageSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LicensePackage object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the license_package."""

    description = marshmallow_fields.Str(
        data_key="description",
        allow_none=True,
    )
    r""" License description

Example: NFS License"""

    entitlement = marshmallow_fields.Nested("netapp_ontap.models.entitlement.EntitlementSchema", data_key="entitlement", unknown=EXCLUDE, allow_none=True)
    r""" The entitlement field of the license_package."""

    keys = marshmallow_fields.List(marshmallow_fields.Str, data_key="keys", allow_none=True)
    r""" The keys field of the license_package."""

    licenses = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.license.LicenseSchema", unknown=EXCLUDE, allow_none=True), data_key="licenses", allow_none=True)
    r""" Installed licenses of the package."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the license.

Example: NFS"""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['not_available', 'site', 'cluster', 'node']),
        allow_none=True,
    )
    r""" Scope of the license.

Valid choices:

* not_available
* site
* cluster
* node"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['compliant', 'noncompliant', 'unlicensed', 'unknown']),
        allow_none=True,
    )
    r""" Summary state of package based on all installed licenses.

Valid choices:

* compliant
* noncompliant
* unlicensed
* unknown"""

    @property
    def resource(self):
        return LicensePackage

    gettable_fields = [
        "links",
        "description",
        "entitlement",
        "licenses",
        "name",
        "scope",
        "state",
    ]
    """links,description,entitlement,licenses,name,scope,state,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "keys",
    ]
    """keys,"""

class LicensePackage(Resource):
    """Allows interaction with LicensePackage objects on the host"""

    _schema = LicensePackageSchema
    _path = "/api/cluster/licensing/licenses"
    _keys = ["name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of license packages.
####
**Note:** By default, the GET method only returns licensed packages. You must provide the following query "state=unlicensed" to retrieve unlicensed packages.
**Note:** Starting with ONTAP 9.11.1, the GET method no longer returns the Base license record.
### Related ONTAP commands
* `system license show-status`
* `system license show`

### Learn more
* [`DOC /cluster/licensing/licenses`](#docs-cluster-cluster_licensing_licenses)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all LicensePackage resources that match the provided query"""
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
        """Returns a list of RawResources that represent LicensePackage resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["LicensePackage"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["LicensePackage"], NetAppResponse]:
        r"""Installs one or more feature licenses.
### Required properties
* `keys` - Array containing a list of NLF or 28-character license keys.
### Related ONTAP commands
* `system license add`

### Learn more
* [`DOC /cluster/licensing/licenses`](#docs-cluster-cluster_licensing_licenses)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["LicensePackage"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a license.
### Related ONTAP commands
* `system license delete`

### Learn more
* [`DOC /cluster/licensing/licenses`](#docs-cluster-cluster_licensing_licenses)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of license packages.
####
**Note:** By default, the GET method only returns licensed packages. You must provide the following query "state=unlicensed" to retrieve unlicensed packages.
**Note:** Starting with ONTAP 9.11.1, the GET method no longer returns the Base license record.
### Related ONTAP commands
* `system license show-status`
* `system license show`

### Learn more
* [`DOC /cluster/licensing/licenses`](#docs-cluster-cluster_licensing_licenses)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific license package.
####
**Note:** By default, the GET method only returns licensed packages. You must provide the following query "state=unlicensed" to retrieve unlicensed packages.
### Related ONTAP commands
* `system license show`
* `system license show-status`

### Learn more
* [`DOC /cluster/licensing/licenses`](#docs-cluster-cluster_licensing_licenses)"""
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
        r"""Installs one or more feature licenses.
### Required properties
* `keys` - Array containing a list of NLF or 28-character license keys.
### Related ONTAP commands
* `system license add`

### Learn more
* [`DOC /cluster/licensing/licenses`](#docs-cluster-cluster_licensing_licenses)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)


    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a license.
### Related ONTAP commands
* `system license delete`

### Learn more
* [`DOC /cluster/licensing/licenses`](#docs-cluster-cluster_licensing_licenses)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


