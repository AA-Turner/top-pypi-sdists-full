r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

# Overview
You can use this API to create, perform operations, and retrieve relevant information pertaining to MetroCluster. The GET operation fetches MetroCluster status and configuration parameters for the local and partner cluster. The PATCH operation executes a switchover, heal or switchback operation. The POST request can be used to setup a MetroCluster.
## Creating a MetroCluster
A new MetroCluster can be set up by issuing a POST to /cluster/metrocluster. Parameters are provided in the body of the POST request.
### Fields used for setting up a MetroCluster configuration
The fields used for MetroCluster APIs are either required or optional and are described as follows:
### Required configuration fields
These fields are always required for any POST /cluster/metrocluster request.

* `partner_cluster.name` - Specifies the partner cluster name to which cluster peering has been established.
* `dr_pairs` - Specifies local and DR partner node pairs.  Each pair uniquely identifies a DR group.
### Optional configuration fields
This field is used to set up additional components in a MetroCluster configuration.

* `mediator.*` - Specifies mediator parameters. If Mediator Assisted Unplanned Switchover (MAUSO) functionality is required, then a mediator should be configured.
* `mccip_ports` - Specifies relevant layer 3 network configuration information for each port. These include port name, node name, IP address, gateway, and netmask. If mccip_ports is not provided, then the API automatically generates IP addresses for the ports and creates a layer 2 network configuration.
### Polling the setup job
After a successful POST /cluster/metrocluster is issued, an HTTP status code of 202 (Accepted) is returned along with a job UUID and a link in the body of the response. The setup job continues asynchronously and can be monitored by using the job UUID and the /cluster/jobs API. The "message" field in the response of the GET /cluster/jobs/{uuid} request shows the current step in the job, and the "state" field shows the overall state of the job.
<br/>
---
## Examples
## Setting up a 4-node MetroCluster
```
This example shows the POST body when setting up a 4-node MetroCluster along with a mediator. It is required that cluster peering be established between two clusters, in this example, site "mcc_siteA" and "mcc_siteB" before issuing the POST request. Nodes "node-a" and "node-b" are HA partners and part of the local cluster "mcc_siteA", wheres nodes "node-c" and "node-d" are HA partners in the partner cluster  "mcc_siteB". Specifying a single DR pairing of "node-a" and "node-c" is sufficient to identify a DR group -- "node-a" and "node-c" will be designated primary DR partners ("node-b" and "node-d" too). "node-d" will then be designated auxiliary partner of "node-a". Once the MetroCluster configuration has been completed, and since mediator parameters have been provided, the mediator will be setup and MAUSO enabled.
# API
/api/cluster/metrocluster
```
### POST body included from file
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Metrocluster

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Metrocluster()
    resource.partner_cluster = {"name": "mcc_siteB"}
    resource.dr_pairs = [{"node": {"name": "node-a"}, "partner": {"name": "node-c"}}]
    resource.mediator = {
        "ip_address": "1.2.3.4",
        "user": "mcc_mediator",
        "password": "openMediator",
    }
    resource.post(hydrate=True)
    print(resource)

```

### Inline POST body
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Metrocluster

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Metrocluster()
    resource.partner_cluster = {"name": "mcc_siteB"}
    resource.dr_pairs = [{"node": {"name": "node-a"}, "partner": {"name": "node-c"}}]
    resource.mediator = {
        "ip_address": "1.2.3.4",
        "user": "mcc_mediator",
        "password": "openMediator",
    }
    resource.post(hydrate=True)
    print(resource)

```

### POST Response
```
HTTP/1.1 202 Accepted
Date: Thu, 09 Jan 2020 20:38:05 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Location: /api/cluster/metrocluster
Content-Length: 189
Content-Type: application/hal+json
{
  "job": {
    "uuid": "f23abbdb-331f-11ea-acd3-005056a708b2",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/f23abbdb-331f-11ea-acd3-005056a708b2"
      }
    }
  }
}
```
### Monitoring the job progress
Use the link provided in the response to the POST request to fetch information for the setup job.
<br/>
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Job

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Job(uuid="f23abbdb-331f-11ea-acd3-005056a708b2")
    resource.get()
    print(resource)

```

<br/>
#### Job status response
The following is an example of the job status response returned by the running MetroCluster setup job:
<br/>
```
HTTP/1.1 200 OK
Date: Thu, 09 Jan 2020 20:40:20 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Length: 373
Content-Type: application/hal+json
{
  "uuid": "f23abbdb-331f-11ea-acd3-005056a708b2",
  "description": "POST /api/cluster/metrocluster",
  "state": "running",
  "message": "Checking remote storage pool",
  "code": 2432844,
  "start_time": "2020-01-09T15:38:08-05:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/f23abbdb-331f-11ea-acd3-005056a708b2"
    }
}
```
### Completion message
This is the final update message from the setup job indicating completion.
<br/>
```
{
  "uuid": "f23abbdb-331f-11ea-acd3-005056a708b2",
  "description": "POST /api/cluster/metrocluster",
  "state": "running",
  "message": "MetroCluster setup is complete",
  "code": 2432849,
  "start_time": "2020-01-09T15:38:08-05:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/f23abbdb-331f-11ea-acd3-005056a708b2"
    }
  }
}
```
### Final status of a successful MetroCluster setup workflow
When the setup job completes, the 'end_time' field is populated, and the 'state' and 'message' fields report the final status.
<br/>
```
HTTP/1.1 200 OK
Date: Thu, 09 Jan 2020 20:43:54 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Length: 360
Content-Type: application/hal+json
{
  "uuid": "f23abbdb-331f-11ea-acd3-005056a708b2",
  "description": "POST /api/cluster/metrocluster",
  "state": "success",
  "message": "success",
  "code": 0,
  "start_time": "2020-01-09T15:38:08-05:00",
  "end_time": "2020-01-09T15:43:50-05:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/f23abbdb-331f-11ea-acd3-005056a708b2"
    }
  }
}
```
### Retrieving the MetroCluster configuration after completion of the POST request
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Metrocluster

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Metrocluster()
    resource.get()
    print(resource)

```

<br/>
#### Response
```
HTTP/1.1 200 OK
Date: Thu, 09 Jan 2020 20:49:40 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Length: 849
Content-Type: application/hal+json
{
  "local": {
    "configuration_state": "configured",
    "periodic_check_enabled": true,
    "mode": "normal",
    "partner_cluster_reachable": true,
    "cluster": {
      "name": "mcc_siteA",
      "uuid": "4294c4f2-30e2-11ea-8cac-005056a708b2",
      "_links": {
        "self": {
          "href": "/api/cluster"
        }
      }
    }
  },
  "remote": {
    "configuration_state": "configured",
    "periodic_check_enabled": true,
    "mode": "normal",
    "cluster": {
      "name": "mcc_siteB",
      "uuid": "4207c6a5-30e2-11ea-be25-005056a7dc84",
      "_links": {
        "self": {
          "href": "/api/cluster/peers/4207c6a5-30e2-11ea-be25-005056a7dc84/cluster"
        }
      }
    }
  },
  "configuration_type": "ip_fabric",
  "_links": {
    "self": {
      "href": "/api/cluster/metrocluster"
    }
  }
}
```
### Retrieving information about the nodes in a MetroCluster configuration
#### Request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import MetroclusterNode

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(MetroclusterNode.get_collection()))

```

<br/>
#### Response
```
HTTP/1.1 200 OK
Date: Fri, 10 Jan 2020 02:26:20 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Type: application/hal+json
Transfer-Encoding: chunked
{
  "records": [
    {
      "dr_group_id": 1,
      "cluster": {
        "name": "mcc_siteA",
        "uuid": "4294c4f2-30e2-11ea-8cac-005056a708b2",
        "_links": {
          "self": {
            "href": "/api/cluster"
          }
        }
      },
      "node": {
        "name": "node-a",
        "uuid": "1e6b0137-30dd-11ea-82ba-005056a7c78a",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/1e6b0137-30dd-11ea-82ba-005056a7c78a"
          }
        }
      },
      "_links": {
        "self": {
          "href": "/api/cluster/metrocluster/nodes/1e6b0137-30dd-11ea-82ba-005056a7c78a"
        }
      }
    },
    {
      "dr_group_id": 1,
      "cluster": {
        "name": "mcc_siteA",
        "uuid": "4294c4f2-30e2-11ea-8cac-005056a708b2",
        "_links": {
          "self": {
            "href": "/api/cluster"
          }
        }
      },
      "node": {
        "name": "node-b",
        "uuid": "1e57ba22-30dd-11ea-8b19-005056a708b2",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/1e57ba22-30dd-11ea-8b19-005056a708b2"
          }
        }
      },
      "_links": {
        "self": {
          "href": "/api/cluster/metrocluster/nodes/1e57ba22-30dd-11ea-8b19-005056a708b2"
        }
      }
    },
    {
      "dr_group_id": 1,
      "cluster": {
        "name": "mcc_siteB",
        "uuid": "4207c6a5-30e2-11ea-be25-005056a7dc84",
        "_links": {
          "self": {
            "href": "/api/cluster/peers/4207c6a5-30e2-11ea-be25-005056a7dc84/cluster"
          }
        }
      },
      "node": {
        "name": "node-c",
        "uuid": "1e563efc-30dd-11ea-a9d3-005056a71573",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/1e563efc-30dd-11ea-a9d3-005056a71573"
          }
        }
      },
      "_links": {
        "self": {
          "href": "/api/cluster/metrocluster/nodes/1e563efc-30dd-11ea-a9d3-005056a71573"
        }
      }
    },
    {
      "dr_group_id": 1,
      "cluster": {
        "name": "mcc_siteB",
        "uuid": "4207c6a5-30e2-11ea-be25-005056a7dc84",
        "_links": {
          "self": {
            "href": "/api/cluster/peers/4207c6a5-30e2-11ea-be25-005056a7dc84/cluster"
          }
        }
      },
      "node": {
        "name": "node-d",
        "uuid": "1e400aa4-30dd-11ea-adec-005056a7dc84",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/1e400aa4-30dd-11ea-adec-005056a7dc84"
          }
        }
      },
      "encryption_enabled": false,
      "_links": {
        "self": {
          "href": "/api/cluster/metrocluster/nodes/1e400aa4-30dd-11ea-adec-005056a7dc84"
        }
      }
    }
  ],
  "num_records": 4,
  "_links": {
    "self": {
      "href": "/api/cluster/metrocluster/nodes"
    }
  }
}
```
---
### Retrieving MetroCluster status and configuration information
```
GET https://<mgmt-ip>/api/cluster/metrocluster
{
    "local": {
        "configuration_state": "configured",
        "periodic_check_enabled": true,
        "mode": "normal",
        "cluster": {
            "name": "cluster1",
            "uuid": "bbc00ca3-8d81-11e9-b5a9-005056826931",
            "_links": {
                "self": {
                    "href": "/api/cluster"
                }
            }
        }
    },
    "remote": {
        "configuration_state": "configured",
        "periodic_check_enabled": true,
        "mode": "normal",
        "cluster": {
            "name": "cluster3",
            "uuid": "ce2cf803-8d81-11e9-87db-00505682cecf",
            "_links": {
                "self": {
                    "href": "/api/cluster/peers/ce2cf803-8d81-11e9-87db-00505682cecf/cluster"
                }
            }
        }
    },
    "_links": {
        "self": {
            "href": "/api/cluster/metrocluster"
        }
    }
}
```
---
### Initiating a switchover, heal or switchback command using PATCH
PATCH is used to initiate a variety of operations by specifying one of the following values in the "action" parameter:

* `switchover` - Initiates  an Unplanned Switchover (USO).
* `negotiated_switchover` - Indicates that an Negotiated switchover (NSO) is to be performed.
* `negotiated_switchover_simulate` - Provides validation in preparation for NSO but does not perform the operation.
* `switchback` - Indicates that a switchback is to be performed.
* `switchback_simulate` - Provides validation for switchback but does not commit the operation.
* `heal_aggregates` - Indicates that the aggregates phase of the heal operation is to be performed.
* `heal_root_aggregates` - Indicates that the root aggregates phase of the heal operation is to be performed.
#### PATCH Switchover example
```
PATCH https://<mgmt-ip>/api/cluster/metrocluster?action=switchover
{
    "job": {
        "uuid": "70e54274-57ee-11e9-aa33-005056820b99",
        "_links": {
            "self": {
                "href": "/api/cluster/jobs/70e54274-57ee-11e9-aa33-005056820b99"
            }
        }
    }
}
```
This returns a job UUID. A subsequent GET for this job should return the following:
<br/>
```
GET https://<mgmt-ip>/api/cluster/jobs/70e54274-57ee-11e9-aa33-005056820b99
{
    "uuid": "70e54274-57ee-11e9-aa33-005056820b99",
    "description": "MetroCluster Switchover Job",
    "state": "success",
    "message": "Complete: Switchover is successful.",
    "code": 0,
    "start_time": "2019-04-05T15:02:02-07:00",
    "end_time": "2019-04-05T15:02:30-07:00",
    "_links": {
        "self": {
            "href": "/api/cluster/jobs/70e54274-57ee-11e9-aa33-005056820b99"
        }
    }
}
```
<br/>
#### PATCH Switchback example:
```
PATCH https://<mgmt-ip>/api/cluster/metrocluster?action=switchback
{
    "job": {
        "uuid": "a62714cc-57ec-11e9-aa33-005056820b99",
        "_links": {
            "self": {
                "href": "/api/cluster/jobs/a62714cc-57ec-11e9-aa33-005056820b99"
            }
        }
    }
}
```
This returns a job UUID with a link to the job. A subsequent GET for this job UUID can be used to retrieve the completion status of the operation:
<br/>
```
GET https://<mgmt-ip>/api/cluster/jobs/a62714cc-57ec-11e9-aa33-005056820b99
{
    "uuid": "a62714cc-57ec-11e9-aa33-005056820b99",
    "description": "MetroCluster Switchback Job",
    "state": "success",
    "message": "Complete: Switchback is successful.",
    "code": 0,
    "start_time": "2019-04-05T14:49:12-07:00",
    "end_time": "2019-04-05T14:50:12-07:00",
    "_links": {
        "self": {
            "href": "/api/cluster/jobs/a62714cc-57ec-11e9-aa33-005056820b99"
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


__all__ = ["Metrocluster", "MetroclusterSchema"]
__pdoc__ = {
    "MetroclusterSchema.resource": False,
    "MetroclusterSchema.opts": False,
}


class MetroclusterSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Metrocluster object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the metrocluster."""

    configuration_type = marshmallow_fields.Str(
        data_key="configuration_type",
        validate=enum_validation(['invalid', 'stretch', 'fabric', 'two_node_fabric', 'ip_fabric', 'ip_two_node_fabric', 'mixed_fabric']),
        allow_none=True,
    )
    r""" Displays the MetroCluster configuration type.

Valid choices:

* invalid
* stretch
* fabric
* two_node_fabric
* ip_fabric
* ip_two_node_fabric
* mixed_fabric"""

    dr_pairs = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.dr_pair.DrPairSchema", unknown=EXCLUDE, allow_none=True), data_key="dr_pairs", allow_none=True)
    r""" DR Pairs to create as part of a MetroCluster configure."""

    encryption_enabled = marshmallow_fields.Boolean(
        data_key="encryption_enabled",
        allow_none=True,
    )
    r""" Indicates if the encryption for NVLog and storage traffic is enabled."""

    local = marshmallow_fields.Nested("netapp_ontap.models.metrocluster_local.MetroclusterLocalSchema", data_key="local", unknown=EXCLUDE, allow_none=True)
    r""" The local field of the metrocluster."""

    mccip_ports = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.mccip_port.MccipPortSchema", unknown=EXCLUDE, allow_none=True), data_key="mccip_ports", allow_none=True)
    r""" List of Port specifications."""

    mediator = marshmallow_fields.Nested("netapp_ontap.resources.mediator.MediatorSchema", data_key="mediator", unknown=EXCLUDE, allow_none=True)
    r""" Mediator information"""

    partner_cluster = marshmallow_fields.Nested("netapp_ontap.resources.cluster.ClusterSchema", data_key="partner_cluster", unknown=EXCLUDE, allow_none=True)
    r""" The partner_cluster field of the metrocluster."""

    remote = marshmallow_fields.Nested("netapp_ontap.models.metrocluster_remote.MetroclusterRemoteSchema", data_key="remote", unknown=EXCLUDE, allow_none=True)
    r""" The remote field of the metrocluster."""

    @property
    def resource(self):
        return Metrocluster

    gettable_fields = [
        "links",
        "configuration_type",
        "encryption_enabled",
        "local",
        "remote",
    ]
    """links,configuration_type,encryption_enabled,local,remote,"""

    patchable_fields = [
        "encryption_enabled",
    ]
    """encryption_enabled,"""

    postable_fields = [
        "dr_pairs",
        "encryption_enabled",
        "mccip_ports",
        "mediator",
        "partner_cluster.name",
        "partner_cluster.uuid",
    ]
    """dr_pairs,encryption_enabled,mccip_ports,mediator,partner_cluster.name,partner_cluster.uuid,"""

class Metrocluster(Resource):
    r""" Holds MetroCluster status and configuration parameters for the local and remote clusters. REST: /api/cluster/metrocluster """

    _schema = MetroclusterSchema
    _path = "/api/cluster/metrocluster"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves MetroCluster status and configuration details.
### Related ONTAP commands
* `metrocluster show`
* `metrocluster node show`

### Learn more
* [`DOC /cluster/metrocluster`](#docs-cluster-cluster_metrocluster)"""
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
        r"""Sets up a MetroCluster.
### Required properties
* `partner_cluster.name`
* `dr_pairs`
### Recommended optional properties
* `mediator.*`
* `mccip_ports`
### Learn more
* [`DOC /cluster/metrocluster`](#docs-cluster-cluster_metrocluster)
### Related ONTAP commands
* `metrocluster configuration-settings dr-group create`
* `metrocluster configuration-settings interface create`
* `metrocluster configuration-settings connection connect`
* `metrocluster configuration-settings mediator add`
* `storage aggregate create`
* `storage aggregate mirror`
* `metrocluster configure`
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
        r"""Initiates a switchover, heal or switchback operation.
### Related ONTAP commands
* `metrocluster switchover`
* `metrocluster switchback`
* `metrocluster heal`
* `metrocluster modify`

### Learn more
* [`DOC /cluster/metrocluster`](#docs-cluster-cluster_metrocluster)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



