r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to add, modify or remove a mediator in a MetroCluster IP configuration or a SnapMirror active sync configuration. You can also use this API to get the status and details of the existing mediator. The GET operation returns the status of the mediator along with the mediator details. The DELETE operation removes the mediator. The POST operation adds the mediator. The PATCH operation modifies the local and remote proxy options.
SnapMirror active sync supports two types of mediators:
1.  **ONTAP Mediator:**  This is the traditional mediator used in SnapMirror active sync, and is hosted on-premises. It requires deployment at a third, neutral site.
2.  **ONTAP cloud mediator:**  This mediator is hosted in BlueXP SaaS and is primarily designed for SnapMirror active sync. It eliminates the need for a third site and provides enhanced scalability and availability.
## Adding a mediator
A mediator can be added by issuing a POST request on /cluster/mediators. Parameters are provided in the body of the POST request. There are no optional parameters for adding a mediator to a MetroCluster IP configuration.
### Required configuration fields (MetroCluster)
These fields are always required for any POST /cluster/mediators request.

* `ip_address`         - Specifies the IP address of the mediator.
* `user`               - Specifies a user name credential.
* `password`           - Specifies a password credential.
### Required configuration fields (SnapMirror active sync: ONTAP Mediator, ONTAP cloud mediator)
These fields are required for any POST /cluster/mediators request.

* `type`                            - (defaults to "on-prem" if omitted) Specifies the type of mediator. For the ONTAP Mediator, the value of type has to be "on-prem". For the ONTAP cloud mediator, the value of type has to be "cloud".
* `peer_cluster.name`               - Specifies the name of the peer cluster.
* `ip_address`                      - (only applicable to the ONTAP Mediator) Specifies the IP address of the mediator.
* `user`                            - (only applicable to the ONTAP Mediator) Specifies the user name credential.
* `password`                        - (only applicable to the ONTAP Mediator) Specifies a password credential.
* `ca_certificate`                  - (optional if the certificate is already installed, only applicable to the ONTAP Mediator) Specifies the CA certificate for the ONTAP Mediator.
* `bluexp_org_id`                   - (only applicable to the ONTAP cloud mediator) Specifies the BlueXP organization ID.
* `service_account_client_id`       - (only applicable to the ONTAP cloud mediator) Specifies the client ID of the service account.
* `service_account_client_secret`   - (only applicable to the ONTAP cloud mediator) Specifies the client secret of the service account.
* `bluexp_account_token`            - (only applicable to the ONTAP cloud mediator) Specifies the BlueXP service account token. This field is mutually exclusive with the `service_account_client_id` and `service_account_client_secret` pair, meaning either the token or the client-id and client-secret pair is allowed.
* `use_http_proxy_local`            - (optional, defaults to false if omitted, only applicable for ONTAP cloud mediator) Specifies if a HTTP proxy should be used on the ONTAP cluster.
* `use_http_proxy_remote`           - (optional, defaults to false if omitted, only applicable for ONTAP cloud mediator) Specifies if a HTTP proxy should be used on the peer ONTAP cluster.
* `strict_cert_validation`          - (optional, defaults to false if omitted, only applicable for ONTAP cloud mediator) Specifies if strict validation of certificates is performed while making REST API calls to the ONTAP Cloud Mediator.
### Polling the setup job
After a successful POST /cluster/mediators is issued, an HTTP status code of 202 (Accepted) is returned along with a job UUID and a link in the body of the response. The setup job continues asynchronously and can be monitored by using the job UUID and the /cluster/jobs API. The "message" field in the response of the GET /cluster/jobs/{uuid} request shows the current step in the job, and the "state" field shows the overall state of the job.
## Deleting a mediator
A mediator can be deleted by issuing a DELETE to /cluster/mediators/{uuid}. Parameters are provided in the body of the DELETE request. There are no optional parameters for deleting a mediator in a MetroCluster IP configuration.
### Required configuration fields (MetroCluster)
These fields are always required for any DELETE /cluster/mediators/{uuid} request.

* `user`               - Specifies a user name credential.
* `password`           - Specifies a password credential.
### Required configuration fields (SnapMirror active sync: ONTAP Mediator, ONTAP cloud mediator)
No fields are required in the body of the DELETE /cluster/mediators/{uuid} request for a mediator in SnapMirror active sync configuration.
### Polling the delete job
After a successful DELETE /cluster/mediators/{uuid} is issued, an HTTP status code of 202 (Accepted) is returned along with a job UUID and a link in the body of the response. The delete job continues asynchronously and can be monitored by using the job UUID and the /cluster/jobs API. The "message" field in the response of the GET /cluster/jobs/{uuid} request shows the current step in the job, and the "state" field shows the overall state of the job.
## Modify a mediator
An ONTAP cloud mediator can be modified by issuing a PATCH to /cluster/mediators/{uuid}. Parameters are provided in the body of the PATCH request. Currently there are only 2 parameters which can be modified.
### Fields which can be modified
These fields can be modified by any PATCH /cluster/mediators/{uuid} request.

* `use-http-proxy-local`    - Specifies if the local cluster should use http-proxy server while making REST API calls to mediator.
* `use-http-proxy-remote`   - Specifies if the remote cluster should use http-proxy while making REST API calls to mediator.
### Polling the modify job
After a successful PATCH /cluster/mediators/{uuid} is issued, an HTTP status code of 202 (Accepted) is returned along with a link in the body of the response. The modify response can be monitored by using the /cluster/jobs API. The "message" field in the response of the GET /cluster/jobs/{uuid} request shows the current step in the job, and the "state" field shows the overall state of the job.
<br/>
---
## Examples
### Setting up a mediator for a four-node MetroCluster and a SnapMirror active sync configuration
This example shows the POST body when setting up a mediator for a four-node MetroCluster IP configuration and a SnapMirror active sync configuration. For MetroCluster, the only prerequisite is that MetroCluster IP is configured.
```
# API
/api/cluster/mediators
```
### POST body included from file (MetroCluster)
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Mediator

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Mediator()
    resource.ip_address = "1.1.1.1"
    resource.user = "username"
    resource.password = "password"
    resource.post(hydrate=True)
    print(resource)

```

### POST body included from file (SnapMirror active sync: ONTAP Mediator)
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Mediator

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Mediator()
    resource.peer_cluster.name = "C2_sti230-vsim-sr092w_cluster"
    resource.ip_address = "172.18.48.61"
    resource.user = "username"
    resource.password = "password"
    resource.post(hydrate=True)
    print(resource)

```

### POST body included from file (SnapMirror active sync: ONTAP cloud mediator)
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Mediator

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Mediator()
    resource.peer_cluster.name = "C2_sti230-vsim-sr092w_cluster"
    resource.type = "cloud"
    resource.bluexp_org_id = "your-bluexp-org-id"
    resource.service_account_client_id = "your-account-client-id"
    resource.service_account_client_secret = "your-account-client-secret"
    resource.use_http_proxy_local = True
    resource.use_http_proxy_remote = True
    resource.strict_cert_validation = True
    resource.post(hydrate=True)
    print(resource)

```

### Inline POST body (MetroCluster)
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Mediator

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Mediator()
    resource.ip_address = "1.1.1.1"
    resource.user = "username"
    resource.password = "password"
    resource.post(hydrate=True)
    print(resource)

```

### Inline POST body (SnapMirror active sync: ONTAP Mediator)
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Mediator

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Mediator()
    resource.peer_cluster.name = "C2_sti230-vsim-sr092w_cluster"
    resource.ip_address = "172.18.48.61"
    resource.user = "username"
    resource.password = "password"
    resource.post(hydrate=True)
    print(resource)

```

### Inline POST body (SnapMirror active sync: ONTAP cloud mediator)
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Mediator

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Mediator()
    resource.peer_cluster.name = "C2_sti230-vsim-sr092w_cluster"
    resource.type = "cloud"
    resource.bluexp_org_id = "your-bluexp-org-id"
    resource.service_account_client_id = "your-account-client-id"
    resource.service_account_client_secret = "your-account-client-secret"
    resource.use_http_proxy_local = True
    resource.use_http_proxy_remote = True
    resource.strict_cert_validation = True
    resource.post(hydrate=True)
    print(resource)

```

### POST Response
```
HTTP/1.1 202 Accepted
Date: Tue, 22 Sep 2020 07:40:59 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Location: /api/cluster/metrocluster
Content-Length: 189
Content-Type: application/hal+json
{
  "job": {
    "uuid": "f567b48b-fca6-11ea-acaf-005056bb47c1",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/f567b48b-fca6-11ea-acaf-005056bb47c1"
      }
    }
  }
}
```
### Monitoring the job progress
Use the link provided in the response to the POST request to fetch information for the mediator setup job.
<br/>
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Job

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Job(uuid="f567b48b-fca6-11ea-acaf-005056bb47c1")
    resource.get()
    print(resource)

```

<br/>
#### Job status response
```
HTTP/1.1 202 Accepted
Date: Tue, 22 Sep 2020 07:41:29 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Location: /api/cluster/metrocluster
Content-Length: 189
Content-Type: application/hal+json
{
  "uuid": "f567b48b-fca6-11ea-acaf-005056bb47c1",
  "description": "POST /api/cluster/mediators/",
  "state": "running",
  "start_time": "2020-09-22T03:41:00-04:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/f567b48b-fca6-11ea-acaf-005056bb47c1"
    }
  }
}
```
#### Final status of a successful Mediator add
```
HTTP/1.1 202 Accepted
Date: Tue, 22 Sep 2020 07:43:38 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Location: /api/cluster/metrocluster
Content-Length: 358
Content-Type: application/hal+json
{
  "uuid": "f567b48b-fca6-11ea-acaf-005056bb47c1",
  "description": "POST /api/cluster/mediators/",
  "state": "success",
  "message": "success",
  "code": 0,
  "start_time": "2020-09-22T03:41:00-04:00",
  "end_time": "2020-09-22T03:42:10-04:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/f567b48b-fca6-11ea-acaf-005056bb47c1"
    }
  }
}
```
### Retrieving the existing mediator configurations
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Mediator

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Mediator.get_collection()))

```

<br/>
#### Response
```
HTTP/1.1 202 Accepted
Date: Tue, 22 Sep 2020 08:53:18 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Location: /api/cluster/metrocluster
Content-Length: 320
Content-Type: application/hal+json
{
  "records": [
    {
      "uuid": "f89e8906-fca6-11ea-acaf-005056bb47c1",
      "_links": {
        "self": {
          "href": "/api/cluster/mediators/f89e8906-fca6-11ea-acaf-005056bb47c1"
        }
      }
    }
  ],
  "num_records": 1,
  "_links": {
    "self": {
      "href": "/api/cluster/mediators"
    }
  }
}
```
### Retrieving a specific mediator using the UUID
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Mediator

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Mediator(uuid="f89e8906-fca6-11ea-acaf-005056bb47c1")
    resource.get()
    print(resource)

```

<br/>
#### Response (MetroCluster)
```
HTTP/1.1 202 Accepted
Date: Tue, 22 Sep 2020 08:59:40 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Location: /api/cluster/metrocluster
Content-Length: 347
Content-Type: application/hal+json
{
  "uuid": "f89e8906-fca6-11ea-acaf-005056bb47c1",
  "ip_address": "10.234.173.40",
  "port": 31784,
  "reachable": true,
  "peer_cluster": {
    "name": "mcc_siteB",
    "uuid": "38779fd1-fc6b-11ea-9421-005056bb21d8"
  },
  "peer_mediator_connectivity": "connected",
  "strict_cert_validation": "true",
  "_links": {
    "self": {
      "href": "/api/cluster/mediators/f89e8906-fca6-11ea-acaf-005056bb47c1"
    }
  }
}
```
#### Response (SnapMirror active sync: ONTAP Mediator)
```
{
  "uuid": "cc44f61f-ffd5-11ef-aaa6-005056ae32ff",
  "ip_address": "172.18.48.61",
  "port": 31784,
  "reachable": true,
  "peer_cluster": {
    "name": "C2_sti232-vsim-sr089o_cluster",
    "uuid": "ece8d7c6-fd8f-11ef-b8b3-005056aec21e"
  },
  "peer_mediator_connectivity": "connected",
  "local_mediator_connectivity": "connected",
  "type": "on_prem",
  "_links": {
    "self": {
      "href": "/api/cluster/mediators/cc44f61f-ffd5-11ef-aaa6-005056ae32ff"
    }
  }
}
```
#### Response (SnapMirror active sync: ONTAP cloud mediator)
```
{
  "uuid": "b9ba4e5b-ff14-11ef-82a4-005056ae1bc8",
  "ip_address": "0.0.0.0",
  "reachable": true,
  "peer_cluster": {
    "name": "C2_sti232-vsim-sr089o_cluster",
    "uuid": "ece8d7c6-fd8f-11ef-b8b3-005056aec21e"
  },
  "peer_mediator_connectivity": "connected",
  "local_mediator_connectivity": "connected",
  "use_http_proxy_local": true,
  "use_http_proxy_remote": true,
  "type": "cloud",
  "_links": {
    "self": {
      "href": "/api/cluster/mediators/b9ba4e5b-ff14-11ef-82a4-005056ae1bc8"
    }
  }
}
```
### Deleting a configured mediator using the UUID (MetroCluster)
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Mediator

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Mediator(uuid="{uuid}")
    resource.delete(body={"user": "username", "password": "password"})

```

#### Response
```
HTTP/1.1 202 Accepted
Date: Tue, 22 Sep 2020 09:13:52 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Location: /api/cluster/metrocluster
Content-Length: 189
Content-Type: application/hal+json
{
  "job": {
    "uuid": "eeb71ccd-fcb3-11ea-acaf-005056bb47c1",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/eeb71ccd-fcb3-11ea-acaf-005056bb47c1"
      }
    }
  }
}
```
### Deleting a configured mediator using the UUID (SnapMirror active sync: ONTAP Mediator, ONTAP cloud mediator)
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Mediator

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Mediator(uuid="{uuid}")
    resource.delete()

```

#### Response
```
{
  "job": {
    "uuid": "0661a77a-ff16-11ef-82a4-005056ae1bc8",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/0661a77a-ff16-11ef-82a4-005056ae1bc8"
      }
    }
  }
}
```
### Monitoring the job progress
Use the link provided in the response to the DELETE request to fetch information for the delete job.
<br/>
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Job

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Job(uuid="eeb71ccd-fcb3-11ea-acaf-005056bb47c1")
    resource.get()
    print(resource)

```

#### Job status response
```
HTTP/1.1 202 Accepted
Date: Tue, 22 Sep 2020 09:14:20 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Location: /api/cluster/metrocluster
Content-Length: 316
Content-Type: application/hal+json
{
  "uuid": "eeb71ccd-fcb3-11ea-acaf-005056bb47c1",
  "description": "DELETE /api/cluster/mediators/f89e8906-fca6-11ea-acaf-005056bb47c1",
  "state": "running",
  "start_time": "2020-09-22T05:13:52-04:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/eeb71ccd-fcb3-11ea-acaf-005056bb47c1"
    }
  }
}
```
#### Final status of the Mediator DELETE job
```
HTTP/1.1 202 Accepted
Date: Tue, 22 Sep 2020 09:21:46 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Location: /api/cluster/metrocluster
Content-Length: 396
Content-Type: application/hal+json
{
  "uuid": "eeb71ccd-fcb3-11ea-acaf-005056bb47c1",
  "description": "DELETE /api/cluster/mediators/f89e8906-fca6-11ea-acaf-005056bb47c1",
  "state": "success",
  "message": "success",
  "code": 0,
  "start_time": "2020-09-22T05:13:52-04:00",
  "end_time": "2020-09-22T05:14:24-04:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/eeb71ccd-fcb3-11ea-acaf-005056bb47c1"
    }
  }
}
```
### Modifying a configured Mediator using the uuid
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Mediator

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Mediator(uuid="{uuid}")
    resource.use_http_proxy_local = True
    resource.use_http_proxy_remote = True
    resource.strict_cert_validation = True
    resource.patch()

```

#### Response
```
HTTP/1.1 202 Accepted
Date: Thu, 06 Mar 2025 10:10:10 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Location: /api/cluster/metrocluster
Content-Length: 189
Content-Type: application/hal+json
{
  "job": {
    "uuid": "3016e8e9-fa73-11ef-9d41-005056ae10ae",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/3016e8e9-fa73-11ef-9d41-005056ae10ae"
      }
    }
  }
}
```
### Monitoring the job progress
Use the link provided in the response to the PATCH request to fetch information for the modify job.
<br/>
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Job

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Job(uuid="3016e8e9-fa73-11ef-9d41-005056ae10ae")
    resource.get()
    print(resource)

```

#### Job status response
```
HTTP/1.1 202 Accepted
Date: Thu, 06 Mar 2025 10:10:22 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Location: /api/cluster/metrocluster
Content-Length: 395
Content-Type: application/hal+json
{
  "uuid": "3016e8e9-fa73-11ef-9d41-005056ae10ae",
  "description": "PATCH /api/cluster/mediators/a9a812bf-f7f8-11ef-a923-005056ae10ae",
  "state": "success",
  "message": "success",
  "code": 0,
  "start_time": "2025-03-06T05:10:10-05:00",
  "end_time": "2025-03-06T05:10:10-05:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/3016e8e9-fa73-11ef-9d41-005056ae10ae"
    }
  }
}
```"""

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


__all__ = ["Mediator", "MediatorSchema"]
__pdoc__ = {
    "MediatorSchema.resource": False,
    "MediatorSchema.opts": False,
}


class MediatorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Mediator object"""

    bluexp_account_token = marshmallow_fields.Str(
        data_key="bluexp_account_token",
        allow_none=True,
    )
    r""" BlueXP account token. This field is only applicable to the ONTAP cloud mediator."""

    bluexp_org_id = marshmallow_fields.Str(
        data_key="bluexp_org_id",
        allow_none=True,
    )
    r""" BlueXP organization ID. This field is only applicable to the ONTAP cloud mediator."""

    ca_certificate = marshmallow_fields.Str(
        data_key="ca_certificate",
        allow_none=True,
    )
    r""" CA certificate for ONTAP Mediator. This is optional if the certificate is already installed."""

    dr_group = marshmallow_fields.Nested("netapp_ontap.resources.metrocluster_dr_group.MetroclusterDrGroupSchema", data_key="dr_group", unknown=EXCLUDE, allow_none=True)
    r""" The dr_group field of the mediator."""

    ip_address = marshmallow_fields.Str(
        data_key="ip_address",
        allow_none=True,
    )
    r""" The IP address of the mediator.

Example: 10.10.10.7"""

    local_mediator_connectivity = marshmallow_fields.Str(
        data_key="local_mediator_connectivity",
        allow_none=True,
    )
    r""" Indicates the mediator connectivity status of the local cluster. Possible values are connected, unreachable, unusable and down-high-latency. This field is only applicable to the mediators in SnapMirror active sync configuration.

Example: connected"""

    password = marshmallow_fields.Str(
        data_key="password",
        allow_none=True,
    )
    r""" The password used to connect to the REST server on the mediator.

Example: mypassword"""

    peer_cluster = marshmallow_fields.Nested("netapp_ontap.resources.cluster_peer.ClusterPeerSchema", data_key="peer_cluster", unknown=EXCLUDE, allow_none=True)
    r""" The peer_cluster field of the mediator."""

    peer_mediator_connectivity = marshmallow_fields.Str(
        data_key="peer_mediator_connectivity",
        allow_none=True,
    )
    r""" Indicates the mediator connectivity status of the peer cluster. Possible values are connected, unreachable, unknown and down-high-latency.

Example: connected"""

    port = Size(
        data_key="port",
        allow_none=True,
    )
    r""" The REST server's port number on the mediator.

Example: 31784"""

    reachable = marshmallow_fields.Boolean(
        data_key="reachable",
        allow_none=True,
    )
    r""" Indicates the connectivity status of the mediator.

Example: true"""

    service_account_client_id = marshmallow_fields.Str(
        data_key="service_account_client_id",
        allow_none=True,
    )
    r""" Client ID of the BlueXP service account. This field is only applicable to the ONTAP cloud mediator."""

    service_account_client_secret = marshmallow_fields.Str(
        data_key="service_account_client_secret",
        allow_none=True,
    )
    r""" Client secret token of the BlueXP service account. This field is only applicable to the ONTAP cloud mediator."""

    strict_cert_validation = marshmallow_fields.Boolean(
        data_key="strict_cert_validation",
        allow_none=True,
    )
    r""" Indicates if strict validation of certificates is performed while making REST API calls to the mediator. This field is only applicable to the ONTAP Cloud Mediator.

Example: true"""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['cloud', 'on_prem']),
        allow_none=True,
    )
    r""" Mediator type. This field is only applicable to the mediators in SnapMirror active sync configuration.

Valid choices:

* cloud
* on_prem"""

    use_http_proxy_local = marshmallow_fields.Boolean(
        data_key="use_http_proxy_local",
        allow_none=True,
    )
    r""" Indicates if the local cluster should use an http-proxy server while making REST API calls to the mediator. This field is only applicable to the ONTAP cloud mediator.

Example: true"""

    use_http_proxy_remote = marshmallow_fields.Boolean(
        data_key="use_http_proxy_remote",
        allow_none=True,
    )
    r""" Indicates if the remote cluster should use an http-proxy server while making REST API calls to the mediator. This field is only applicable to the ONTAP cloud mediator.

Example: true"""

    user = marshmallow_fields.Str(
        data_key="user",
        allow_none=True,
    )
    r""" The username used to connect to the REST server on the mediator.

Example: myusername"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The unique identifier for the mediator service."""

    @property
    def resource(self):
        return Mediator

    gettable_fields = [
        "ip_address",
        "local_mediator_connectivity",
        "peer_cluster.links",
        "peer_cluster.name",
        "peer_cluster.uuid",
        "peer_mediator_connectivity",
        "port",
        "reachable",
        "strict_cert_validation",
        "type",
        "use_http_proxy_local",
        "uuid",
    ]
    """ip_address,local_mediator_connectivity,peer_cluster.links,peer_cluster.name,peer_cluster.uuid,peer_mediator_connectivity,port,reachable,strict_cert_validation,type,use_http_proxy_local,uuid,"""

    patchable_fields = [
        "strict_cert_validation",
        "use_http_proxy_local",
        "use_http_proxy_remote",
    ]
    """strict_cert_validation,use_http_proxy_local,use_http_proxy_remote,"""

    postable_fields = [
        "bluexp_account_token",
        "bluexp_org_id",
        "ca_certificate",
        "ip_address",
        "password",
        "peer_cluster.name",
        "peer_cluster.uuid",
        "port",
        "service_account_client_id",
        "service_account_client_secret",
        "strict_cert_validation",
        "type",
        "use_http_proxy_local",
        "use_http_proxy_remote",
        "user",
    ]
    """bluexp_account_token,bluexp_org_id,ca_certificate,ip_address,password,peer_cluster.name,peer_cluster.uuid,port,service_account_client_id,service_account_client_secret,strict_cert_validation,type,use_http_proxy_local,use_http_proxy_remote,user,"""

class Mediator(Resource):
    r""" Mediator information """

    _schema = MediatorSchema
    _path = "/api/cluster/mediators"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r""""Retrieves a Mediator configured in the cluster."
### Related ONTAP commands
* `storage iscsi-initiator show`

### Learn more
* [`DOC /cluster/mediators`](#docs-cluster-cluster_mediators)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all Mediator resources that match the provided query"""
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
        """Returns a list of RawResources that represent Mediator resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Mediator"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Modifies the mediator configuration.
### Learn more
* [`DOC /cluster/mediators`](#docs-cluster-cluster_mediators)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["Mediator"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Mediator"], NetAppResponse]:
        r"""Creates and connect a mediator.
### Learn more
* [`DOC /cluster/mediators`](#docs-cluster-cluster_mediators)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["Mediator"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the mediator.
### Learn more
* [`DOC /cluster/mediators`](#docs-cluster-cluster_mediators)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r""""Retrieves a Mediator configured in the cluster."
### Related ONTAP commands
* `storage iscsi-initiator show`

### Learn more
* [`DOC /cluster/mediators`](#docs-cluster-cluster_mediators)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r""""Retrieves the Mediator state and configuration."
### Related ONTAP commands
* `storage iscsi-initiator show`

### Learn more
* [`DOC /cluster/mediators`](#docs-cluster-cluster_mediators)"""
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
        r"""Creates and connect a mediator.
### Learn more
* [`DOC /cluster/mediators`](#docs-cluster-cluster_mediators)"""
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
        r"""Modifies the mediator configuration.
### Learn more
* [`DOC /cluster/mediators`](#docs-cluster-cluster_mediators)"""
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
        r"""Deletes the mediator.
### Learn more
* [`DOC /cluster/mediators`](#docs-cluster-cluster_mediators)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


