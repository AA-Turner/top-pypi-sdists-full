r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

# Overview
You can use this API to create a cluster, update cluster-wide configurations, and retrieve the current configuration details.
## Creating a cluster
You can create a new cluster by issuing a POST request to /cluster. Parameters are provided in the body of the POST request to configure cluster-wide settings and add nodes during the cluster setup.
### Fields used for creating a cluster
The fields used for the cluster APIs fall into the following categories:

* Required cluster-wide configuration
* Optional cluster-wide configuration
### Required cluster-wide configuration
The following fields are always required for any POST /cluster request:

* name
* password
### Optional cluster-wide configuration
The following fields are used to set up additional cluster-wide configurations:

* location
* contact
* dns_domains
* name_servers
* ntp_servers
* timezone
* license
* configuration_backup
* management_interface
* nodes
* active_directory
### Nodes field
The nodes field specifies the nodes to join to the cluster. To use this API, all nodes must run the same version of ONTAP. If you do not specify a node, the cluster is configured with one node added. The REST request is issued to the node that is added to the cluster. If you specify one node, do not use the "node.cluster_interface.ip.address" field. If you specify multiple nodes, specify the node to which the REST request is issued in addition to the remote nodes. Use the "node.cluster_interface.ip.address" field to identify each node. All other node fields are optional in all cases. If you provide a field for one node, you need to provide the same field for all nodes.
### Node networking fields
The cluster management interface and each node management interface use the cluster management interface subnet mask and gateway. For advanced configurations in which the cluster and node management interfaces are on different subnets, use the /network/ip/interface APIs to configure network interfaces after setup is complete.
The management interfaces are used to communicate with the name servers and NTP servers. The address family of the name servers and NTP servers must match the management interfaces address family.
### Single node cluster field
When the "single_node_cluster" field is set to "true", the cluster is created in single node cluster mode. You can provide a node field for this node for node-specific configuration but do not use the "node.cluster_interface.ip.address" field. Storage failover is configured to non-HA mode, and ports used for cluster ports are moved to the default IPspace. This might cause the node to reboot during setup. While a node reboots, the RESTful interface might not be available. See "Connection failures during cluster create" for more information.
### Create recommended aggregates parameter
When the "create_recommended_aggregates" parameter is set to "true", aggregates based on an optimal layout recommended by the system are created on each of the nodes in the cluster. The default setting is "false".
<br/>
---
## Performance monitoring
Performance of the cluster can be monitored by the `metric.*` and `statistics.*` fields. These fields show the performance of the cluster in terms of IOPS, latency and throughput. The `metric.*` fields denote an average, whereas the `statistics.*` fields denote a real-time monotonically increasing value aggregated across all nodes.
<br/>
---
## Analytics auto-enable properties
New SVMs will use the values set for the "auto_enable_analytics" and "auto_enable_activity_tracking" fields as the default for new volumes. The default setting is false.
### Setting auto_enable_analytics
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Cluster

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Cluster()
    resource.auto_enable_analytics = True
    resource.patch()

```

### Setting auto_enable_activity_tracking
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Cluster

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Cluster()
    resource.auto_enable_activity_tracking = True
    resource.patch()

```

<br/>
---
## Monitoring cluster create status
### Errors before the job starts
Configuration in the POST /cluster request is validated before the cluster create job starts. If an invalid configuration is found, an HTTP error code in the 4xx range is returned. No cluster create job is started.
### Polling on the job
After a successful POST /cluster request is issued, an HTTP error code of 202 is returned along with a job UUID and link in the body of the response. The cluster create job continues asynchronously and is monitored with the job UUID using the /cluster/jobs API. The "message" field in the response of the GET /cluster/jobs/{uuid} request shows the current step in the job, and the "state" field shows the overall state of the job.
### Errors during the job
If a failure occurs during the cluster create job, the job body provides details of the error along with error code fields. See the error table under "Responses" in the POST /cluster documentation for common error codes and descriptions.
### Rerunning POST /cluster
The POST /cluster request can be rerun if errors occur. When rerunning the request, use the same body and query parameters. You can change the value of any field in the original body or query, but you cannot change the provided fields. For example, an initial request might have a body section as follows:
<br />
```
body =
{
  "name": "clusCreateRerun",
  "password": "openSesame",
  "nodes": [
    {
      "cluster_interface": {
        "ip": {
          "address": "1.1.1.1"
        }
      }
    },
    {
      "cluster_interface": {
        "ip": {
          "address": "2.2.2.2"
        }
      }
    }
  ]
}
```
A rerun request updates the body details to:
<br />
```
body =
{
  "name": "clusCreateRerun",
  "password": "openSesame",
  "nodes": [
    {
      "cluster_interface": {
        "ip": {
          "address": "3.3.3.3"
        }
      }
    },
    {
      "cluster_interface": {
        "ip": {
          "address": "4.4.4.4"
        }
      }
    }
  ]
}
```
A rerun request with the following body details is invalid:
<br />
```
body =
{
  "name": "clusCreateRerun",
  "password": "openSesame",
  "nodes": [
    {
      "cluster_interface": {
        "ip": {
          "address": "3.3.3.3"
        }
      }
    }
  ]
}
```
Note that the password might already be configured. If a password is already configured and then a new password is provided, the new request overwrites the existing password. If a password is already configured either by another interface or by a previous POST request to /cluster, authenticate any future REST requests with that password. If a POST request to /cluster with the default return_timeout of 0 returns an error, then the password was not changed.
### Connection failures during cluster create
A request to poll the job status might fail during a cluster create job in the following two cases. In these cases, programmatic use of the RESTful interface might be resilient to these connection failures.
1. When the "single_node_cluster" flag is set to "true", the node might reboot. During this time, the RESTful interface might refuse connections and return errors on a GET request, or connection timeouts might occur. Programmatic use of the RESTful interface during reboots must consider these effects while polling a cluster create job.
2. The "mgmt_auto" LIF is removed during the cluster create job. A POST /cluster request might be issued on the "mgmt_auto" LIF. However, requests to poll the job status might fail during cluster create when the "mgmt_auto" LIF is removed. The "mgmt_auto" LIF is only removed if a cluster management interface is provided as an argument to POST /cluster, and only after the cluster management interface is created. Programmatic use of the POST /cluster API on the "mgmt_auto" LIF should be configured to dynamically switch to polling the job on the cluster management LIF.
<br/>
---
## Active Directory account for the cluster
An Active Directory account for the cluster can be retrieved, created, modified, and deleted by using the `active_directory.*` fields. An account can be created either during cluster creation using a POST request or after cluster creation using a PATCH request.
An Active Directory account can be deleted by passing `null` as the Active Directory name during a PATCH request. The `username` and `password` fields are required to create, modify, and delete an Active Directory account.
Creating a new Active Directory account for the cluster:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Cluster

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Cluster()
    resource.active_directory = {
        "username": "administrator",
        "password": "password",
        "name": "adaccount",
        "fqdn": "test.com",
        "force_account_overwrite": True,
    }
    resource.patch()

```

<br/>
Deleting the Active Directory account of the cluster:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Cluster

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Cluster()
    resource.active_directory = {
        "username": "administrator",
        "password": "password",
        "name": None,
    }
    resource.patch()

```

<br/>
---
## Modifying cluster configurations
The following fields can be used to modify a cluster-wide configuration:

* name
* location
* contact
* dns_domains
* name_servers
* timezone
* auto-enable-analytics
* auto-enable-activity-tracking
* active_directory
<br/>
---
# Examples
### Minimally configuring a 2-node setup
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Cluster

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Cluster()
    resource.name = "clusCreateExample1"
    resource.password = "openSesame"
    resource.nodes = [
        {"cluster_interface": {"ip": {"address": "1.1.1.1"}}},
        {"cluster_interface": {"ip": {"address": "2.2.2.2"}}},
    ]
    resource.post(hydrate=True)
    print(resource)

```

---
### Setting up a single node with additional node configuration and auto aggregate creation
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Cluster

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Cluster()
    resource.name = "clusCreateExample2"
    resource.password = "openSesame"
    resource.nodes = [{"name": "singleNode", "location": "Sunnyvale"}]
    resource.post(
        hydrate=True, single_node_cluster=True, create_recommended_aggregates=True
    )
    print(resource)

```

---
### Modifying a cluster-wide configuration
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Cluster

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Cluster()
    resource.contact = "it@company.com"
    resource.patch()

```

---
## Creating a cluster using the cluster "create" operation
This example shows how to create a cluster using the cluster APIs. Specifically, this example shows the creation of a two-node cluster and uses information from the nodes themselves combined with user supplied information to configure the cluster.
### Preparing for setup
Before the REST APIs can be issued to create the cluster, the cluster must be wired up and powered on. The network connections between the nodes for the cluster interconnect and the connections to the management network must be completed.  After the nodes are powered on, the nodes automatically configure interfaces on the platform's default cluster ports to allow the nodes to discover each other during setup and expansion workflows. You must configure a management interface on one node or use the mgmt_auto LIF, which is assigned an IP address using DHCP, to start using the REST APIs.  By making a console connection to a node, the cluster setup wizard guides you through the configuration of the initial node management interface to which the REST calls can be sent.  Once this step is completed, exit the wizard by typing "exit". You can then issue REST API requests.
1.  Wire and power on the nodes.
2.  Make a console connection to one node to access the cluster setup wizard.
3.  Enter node management interface information to enable REST API requests to be sent to the node.
```
Welcome to the cluster setup wizard.
You can enter the following commands at any time:
  "help" or "?" - if you want to have a question clarified,
  "back" - if you want to change previously answered questions, and
  "exit" or "quit" - if you want to quit the cluster setup wizard.
  Any changes you made before quitting will be saved.
  You can return to cluster setup at any time by typing "cluster setup".
  To accept a default or omit a question, do not enter a value.
  This system will send event messages and periodic reports to NetApp Technical
  Support. To disable this feature, enter
  autosupport modify -support disable
  within 24 hours.
  Enabling AutoSupport can significantly speed problem determination and
  resolution should a problem occur on your system.
  For further information on AutoSupport, see:
    http://support.netapp.com/autosupport/
    Type yes to confirm and continue {yes}: yes
    Enter the node management interface port [e0c]:
      Enter the node management interface IP address: 10.224.82.249
      Enter the node management interface netmask: 255.255.192.0
      Enter the node management interface default gateway: 10.224.64.1
      A node management interface on port e0c with IP address 10.224.82.249 has been created.
      Use your web browser to complete cluster setup by accessing
      https://10.224.82.249
      Otherwise, press Enter to complete cluster setup using the command line
      interface: exit
      Exiting the cluster setup wizard. Any changes you made have been saved.
      The cluster administrator's account (username "admin") password is set to the system default.
      Warning: You have exited the cluster setup wizard before completing all
      of the tasks. The cluster is not configured. You can complete cluster setup by typing
      "cluster setup" in the command line interface.
```
---
### Discovering the nodes
If you issue a GET /api/cluster/nodes request when the nodes are not in a cluster, the API returns a list of nodes that were discovered on the cluster interconnect.  Information returned includes the node's serial number, model, software version, UUID, and cluster interface address.  The number of nodes returned should be the same as the number of nodes expected to be in the cluster.  If too many nodes are discovered, remove the nodes that should not be part of the cluster.  If not enough nodes are discovered, verify all the nodes are powered on, that the connections to the cluster interconnect are complete, and retry the command.
<br />
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Node

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Node.get_collection(fields="state,uptime")))

```
<div class="try_it_out">
<input id="example7_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example7_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example7_result" class="try_it_out_content">
```
[
    Node(
        {
            "name": "cluster1",
            "uptime": 134555,
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/6dce4710-c860-11e9-b5bc-005056bb6135"
                }
            },
            "uuid": "6dce4710-c860-11e9-b5bc-005056bb6135",
            "state": "up",
        }
    )
]

```
</div>
</div>

---
### Creating the cluster
When the node information is available, including each node's cluster interface address, you can assemble the information for creating the cluster.  Provide the cluster name and the password for the admin account.  The rest of the information is optional and can be configured later using other APIs.  Provide the cluster interface address for each node to be included in the cluster so that you can connect to it while adding it to the cluster. In addition to the cluster interface address, you can provide the optional node name, location, and management interface information. If you do not provide node names, nodes are named based on the cluster name. The nodes' management interface subnet mask and gateway values are omitted and must be the same as the cluster management interface's subnet mask and gateway.
<br />
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Cluster

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Cluster()
    resource.name = "cluster1"
    resource.location = "datacenter1"
    resource.contact = "me"
    resource.dns_domains = ["example.com"]
    resource.name_servers = ["10.224.223.130", "10.224.223.131", "10.224.223.132"]
    resource.ntp_servers = ["time.nist.gov"]
    resource.active_directory = {
        "username": "administrator",
        "password": "password",
        "name": "adaccount",
        "fqdn": "test.com",
        "force_account_overwrite": True,
    }
    resource.management_interface = {
        "ip": {
            "address": "10.224.82.25",
            "netmask": "255.255.192.0",
            "gateway": "10.224.64.1",
        }
    }
    resource.password = "mypassword"
    resource.license = {"keys": ["AMEPOSOIKLKGEEEEDGNDEKSJDE"]}
    resource.nodes = [
        {
            "cluster_interface": {"ip": {"address": "169.254.245.113"}},
            "name": "node1",
            "management_interface": {"ip": {"address": "10.224.82.29"}},
        },
        {
            "cluster_interface": {"ip": {"address": "169.254.217.95"}},
            "name": "node2",
            "management_interface": {"ip": {"address": "10.224.82.31"}},
        },
    ]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example8_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example8_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example8_result" class="try_it_out_content">
```
Cluster(
    {
        "license": {"keys": ["AMEPOSOIKLKGEEEEDGNDEKSJDE"]},
        "name_servers": ["10.224.223.130", "10.224.223.131", "10.224.223.132"],
        "name": "cluster1",
        "management_interface": {
            "ip": {
                "gateway": "10.224.64.1",
                "netmask": "255.255.192.0",
                "address": "10.224.82.25",
            }
        },
        "ntp_servers": ["time.nist.gov"],
        "password": "mypassword",
        "location": "datacenter1",
        "active_directory": {
            "fqdn": "test.com",
            "name": "adaccount",
            "password": "password",
            "username": "administrator",
            "force_account_overwrite": True,
        },
        "dns_domains": ["example.com"],
        "contact": "me",
        "nodes": [
            {
                "cluster_interface": {"ip": {"address": "169.254.245.113"}},
                "name": "node1",
                "management_interface": {"ip": {"address": "10.224.82.29"}},
            },
            {
                "cluster_interface": {"ip": {"address": "169.254.217.95"}},
                "name": "node2",
                "management_interface": {"ip": {"address": "10.224.82.31"}},
            },
        ],
    }
)

```
</div>
</div>

---
### Monitoring the progress of cluster creation
To monitor the progress of the cluster create operation, poll the returned job link until the state value is no longer "running" or "queued".
<br />
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Job

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Job(uuid="b5bc07e2-1e9-11e9-a751-005056bbd95f")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example9_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example9_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example9_result" class="try_it_out_content">
```
Job(
    {
        "description": "POST /api/cluster",
        "code": 0,
        "message": "success",
        "state": "success",
        "uuid": "b5bc07e2-19e9-11e9-a751-005056bbd95f",
        "_links": {
            "self": {"href": "/api/cluster/jobs/b5bc07e2-19e9-11e9-a751-005056bbd95f"}
        },
    }
)

```
</div>
</div>

---
### Verifying the cluster information
After the cluster is created, you can verify the information applied using a number of APIs. You can retrieve most of the information provided using the /api/cluster and /api/cluster/nodes APIs. In addition, you can view the network interface and route information using the /api/network APIs. The following example shows how to retrieve the cluster information:
<br />
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Cluster

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Cluster()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example10_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example10_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example10_result" class="try_it_out_content">
```
Cluster(
    {
        "name_servers": ["192.0.2.1", "192.0.2.2"],
        "name": "C1_sti44-vsim-ucs515w_1621957038",
        "_links": {"self": {"href": "/api/cluster"}},
        "ntp_servers": ["192.0.2.3"],
        "metric": {
            "status": "ok",
            "iops": {"total": 0, "write": 0, "other": 0, "read": 0},
            "latency": {"total": 0, "write": 0, "other": 0, "read": 0},
            "timestamp": "2021-05-26T20:36:15+00:00",
            "throughput": {"total": 0, "write": 0, "other": 0, "read": 0},
            "duration": "PT15S",
        },
        "uuid": "5f7f57c7-bd67-11eb-95f4-005056a7b9b1",
        "location": "sti",
        "management_interfaces": [
            {
                "name": "clus_mgmt",
                "_links": {
                    "self": {
                        "href": "/api/network/ip/interfaces/beef2db7-bd67-11eb-95f4-005056a7b9b1"
                    }
                },
                "uuid": "beef2db7-bd67-11eb-95f4-005056a7b9b1",
                "ip": {"address": "192.0.2.4"},
            },
            {
                "name": "sti44-vsim-ucs515w_cluster_mgmt_inet6",
                "_links": {
                    "self": {
                        "href": "/api/network/ip/interfaces/cb63e02c-bd72-11eb-95f4-005056a7b9b1"
                    }
                },
                "uuid": "cb63e02c-bd72-11eb-95f4-005056a7b9b1",
                "ip": {"address": "2001:db8:ef56:gh78::ij90"},
            },
            {
                "name": "sti44-vsim-ucs515x_cluster_mgmt_inet6",
                "_links": {
                    "self": {
                        "href": "/api/network/ip/interfaces/ea13dec1-bd72-11eb-bd00-005056a7f50e"
                    }
                },
                "uuid": "ea13dec1-bd72-11eb-bd00-005056a7f50e",
                "ip": {"address": "2001:db8:ef56:gh78::ij91"},
            },
        ],
        "peering_policy": {
            "authentication_required": True,
            "encryption_required": False,
            "minimum_passphrase_length": 8,
        },
        "san_optimized": False,
        "statistics": {
            "status": "ok",
            "iops_raw": {"total": 0, "write": 0, "other": 0, "read": 0},
            "latency_raw": {"total": 0, "write": 0, "other": 0, "read": 0},
            "throughput_raw": {"total": 0, "write": 0, "other": 0, "read": 0},
            "timestamp": "2021-05-26T20:36:25+00:00",
        },
        "active_directory": {
            "fqdn": "TEST.COM",
            "name": "ADACCOUNT",
            "organizational_unit": "CN=Computers",
        },
        "dns_domains": ["example.com"],
        "version": {
            "generation": 9,
            "full": "NetApp Release 9.10.1: Mon May 24 08:07:35 UTC 2021",
            "minor": 1,
            "major": 10,
        },
        "contact": "example_name",
        "timezone": {"name": "America/New_York"},
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


__all__ = ["Cluster", "ClusterSchema"]
__pdoc__ = {
    "ClusterSchema.resource": False,
    "ClusterSchema.opts": False,
}


class ClusterSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Cluster object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the cluster."""

    tags = marshmallow_fields.List(marshmallow_fields.Str, data_key="_tags", allow_none=True)
    r""" Tags are an optional way to track the uses of a resource. Tag values must be formatted as key:value strings.

Example: ["team:csi","environment:test"]"""

    active_directory = marshmallow_fields.Nested("netapp_ontap.models.cluster_active_directory.ClusterActiveDirectorySchema", data_key="active_directory", unknown=EXCLUDE, allow_none=True)
    r""" The active_directory field of the cluster."""

    auto_enable_activity_tracking = marshmallow_fields.Boolean(
        data_key="auto_enable_activity_tracking",
        allow_none=True,
    )
    r""" Indicates how new SVMs will default "auto_enable_activity_tracking" for new volumes."""

    auto_enable_analytics = marshmallow_fields.Boolean(
        data_key="auto_enable_analytics",
        allow_none=True,
    )
    r""" Indicates how new SVMs will default "auto_enable_analytics" for new volumes."""

    certificate = marshmallow_fields.Nested("netapp_ontap.resources.security_certificate.SecurityCertificateSchema", data_key="certificate", unknown=EXCLUDE, allow_none=True)
    r""" The certificate field of the cluster."""

    configuration_backup = marshmallow_fields.Nested("netapp_ontap.resources.configuration_backup.ConfigurationBackupSchema", data_key="configuration_backup", unknown=EXCLUDE, allow_none=True)
    r""" The configuration_backup field of the cluster."""

    contact = marshmallow_fields.Str(
        data_key="contact",
        allow_none=True,
    )
    r""" The contact field of the cluster.

Example: support@company.com"""

    disaggregated = marshmallow_fields.Boolean(
        data_key="disaggregated",
        allow_none=True,
    )
    r""" Specifies whether the cluster is designed for disaggregated storage."""

    dns_domains = marshmallow_fields.List(marshmallow_fields.Str, data_key="dns_domains", allow_none=True)
    r""" A list of DNS domains.
Domain names have the following requirements:

* The name must contain only the following characters: A through Z, a through z, 0 through 9, ".", "-" or "_".
* The first character of each label, delimited by ".", must be one of the following characters: A through Z or a through z or 0 through 9.
* The last character of each label, delimited by ".", must be one of the following characters: A through Z, a through z, or 0 through 9.
* The top level domain must contain only the following characters: A through Z, a through z.
* The system reserves the following names:"all", "local", and "localhost".


Example: ["example.com","example2.example3.com"]"""

    license = marshmallow_fields.Nested("netapp_ontap.models.license_keys.LicenseKeysSchema", data_key="license", unknown=EXCLUDE, allow_none=True)
    r""" License keys or NLF contents."""

    location = marshmallow_fields.Str(
        data_key="location",
        allow_none=True,
    )
    r""" The location field of the cluster.

Example: building 1"""

    management_interface = marshmallow_fields.Nested("netapp_ontap.models.cluster_management_interface.ClusterManagementInterfaceSchema", data_key="management_interface", unknown=EXCLUDE, allow_none=True)
    r""" The management interface of the cluster. The subnet mask and gateway for this interface are used for the node management interfaces provided in the node configuration."""

    management_interfaces = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.ip_interface.IpInterfaceSchema", unknown=EXCLUDE, allow_none=True), data_key="management_interfaces", allow_none=True)
    r""" The management_interfaces field of the cluster."""

    metric = marshmallow_fields.Nested("netapp_ontap.resources.performance_metric.PerformanceMetricSchema", data_key="metric", unknown=EXCLUDE, allow_none=True)
    r""" Performance numbers, such as IOPS latency and throughput."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The name field of the cluster.

Example: cluster1"""

    name_servers = marshmallow_fields.List(marshmallow_fields.Str, data_key="name_servers", allow_none=True)
    r""" The list of IP addresses of the DNS servers. Addresses can be either
IPv4 or IPv6 addresses.


Example: ["10.224.65.20","2001:db08:a0b:12f0::1"]"""

    nodes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, allow_none=True), data_key="nodes", allow_none=True)
    r""" Complete node information"""

    ntp_servers = marshmallow_fields.List(marshmallow_fields.Str, data_key="ntp_servers", allow_none=True)
    r""" Host name, IPv4 address, or IPv6 address for the external NTP time servers.

Example: ["time.nist.gov","10.98.19.20","2610:20:6F15:15::27"]"""

    password = marshmallow_fields.Str(
        data_key="password",
        allow_none=True,
    )
    r""" Initial admin password used to create the cluster.

Example: mypassword"""

    peering_policy = marshmallow_fields.Nested("netapp_ontap.models.cluster_peering_policy.ClusterPeeringPolicySchema", data_key="peering_policy", unknown=EXCLUDE, allow_none=True)
    r""" The peering_policy field of the cluster."""

    san_optimized = marshmallow_fields.Boolean(
        data_key="san_optimized",
        allow_none=True,
    )
    r""" Specifies if this cluster is an All SAN Array."""

    statistics = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_raw.PerformanceMetricRawSchema", data_key="statistics", unknown=EXCLUDE, allow_none=True)
    r""" The statistics field of the cluster."""

    timezone = marshmallow_fields.Nested("netapp_ontap.models.timezone_cluster.TimezoneClusterSchema", data_key="timezone", unknown=EXCLUDE, allow_none=True)
    r""" Provides the cluster-wide time zone information that localizes time found on messages displayed on each node's:

* console messages;
* logging to internal ONTAP log files; and
* localized REST API full ISO-8601 date, time, and time zone format information.
Machine-to-machine interfaces, such as file access protocols (NFS, CIFS), block access protocols (SAN), and other protocols
such as Manage ONTAP (ONTAPI), use second or subsecond time values that are based on world time or UTC."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The uuid field of the cluster.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    version = marshmallow_fields.Nested("netapp_ontap.models.version.VersionSchema", data_key="version", unknown=EXCLUDE, allow_none=True)
    r""" This returns the cluster version information.  When the cluster has more than one node, the cluster version is equivalent to the lowest of generation, major, and minor versions on all nodes."""

    @property
    def resource(self):
        return Cluster

    gettable_fields = [
        "links",
        "tags",
        "active_directory",
        "auto_enable_activity_tracking",
        "auto_enable_analytics",
        "certificate.links",
        "certificate.name",
        "certificate.uuid",
        "contact",
        "disaggregated",
        "dns_domains",
        "location",
        "management_interfaces.links",
        "management_interfaces.ip",
        "management_interfaces.name",
        "management_interfaces.uuid",
        "metric",
        "name",
        "name_servers",
        "ntp_servers",
        "peering_policy",
        "san_optimized",
        "statistics.iops_raw",
        "statistics.latency_raw",
        "statistics.status",
        "statistics.throughput_raw",
        "statistics.timestamp",
        "timezone",
        "uuid",
        "version",
    ]
    """links,tags,active_directory,auto_enable_activity_tracking,auto_enable_analytics,certificate.links,certificate.name,certificate.uuid,contact,disaggregated,dns_domains,location,management_interfaces.links,management_interfaces.ip,management_interfaces.name,management_interfaces.uuid,metric,name,name_servers,ntp_servers,peering_policy,san_optimized,statistics.iops_raw,statistics.latency_raw,statistics.status,statistics.throughput_raw,statistics.timestamp,timezone,uuid,version,"""

    patchable_fields = [
        "tags",
        "active_directory",
        "auto_enable_activity_tracking",
        "auto_enable_analytics",
        "certificate.name",
        "certificate.uuid",
        "contact",
        "dns_domains",
        "location",
        "name",
        "name_servers",
        "timezone",
    ]
    """tags,active_directory,auto_enable_activity_tracking,auto_enable_analytics,certificate.name,certificate.uuid,contact,dns_domains,location,name,name_servers,timezone,"""

    postable_fields = [
        "tags",
        "active_directory",
        "auto_enable_activity_tracking",
        "auto_enable_analytics",
        "configuration_backup",
        "contact",
        "dns_domains",
        "license",
        "location",
        "management_interface",
        "name",
        "name_servers",
        "nodes",
        "ntp_servers",
        "password",
        "timezone",
    ]
    """tags,active_directory,auto_enable_activity_tracking,auto_enable_analytics,configuration_backup,contact,dns_domains,license,location,management_interface,name,name_servers,nodes,ntp_servers,password,timezone,"""

class Cluster(Resource):
    r""" Complete cluster information """

    _schema = ClusterSchema
    _path = "/api/cluster"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the cluster configuration.
### Learn more
* [`DOC /cluster`](#docs-cluster-cluster)"""
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
        r"""Creates a cluster.
### Required properties
* `name`
* `password`
### Recommended optional properties
* `location`
* `contact`
* `dns_domains`
* `name_servers`
* `ntp_servers`
* `license`
* `configuration_backup`
* `management_interface`
* `nodes`
* `timezone`
### Learn more
* [`DOC /cluster`](#docs-cluster-cluster)
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
        r"""Updates the cluster configuration after the cluster is created.
### Related ONTAP commands
* `cluster identity modify`
* `system node modify`
* `vserver services dns modify`
* `vserver services name-service dns modify`
* `timezone`
* `security ssl modify`
* `vserver active-directory create`
* `vserver active-directory modify`
* `vserver active-directory delete`

### Learn more
* [`DOC /cluster`](#docs-cluster-cluster)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



