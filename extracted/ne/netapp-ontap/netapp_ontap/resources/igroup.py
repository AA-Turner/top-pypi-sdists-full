r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
An initiator group (igroup) is a collection of Fibre Channel (FC) world wide port names (WWPNs), and/or iSCSI Qualified Names (IQNs), and/or iSCSI EUIs (Extended Unique Identifiers) that identify host endpoints.<br/>
Initiator groups are used to control which hosts can access specific LUNs. To grant access to a LUN from one or more hosts, create an initiator group containing the host initiator names, then create a LUN map that associates the initiator group with the LUN.<br/>
An initiator group may contain either initiators or other initiator groups, but not both simultaneously. When a parent initiator group is mapped, it inherits all of the initiators of any initiator groups nested below it. If any nested initiator group is modified to contain different initiators, the parent initiator groups inherit the change. A parent can have many nested initiator groups and an initiator group can be nested under multiple parents. Initiators can only be added or removed from the initiator group that directly contains them. The maximum supported depth of nesting is three layers.<br/>
Best practice when using nested initiator groups is to match host hierarchies. A single initiator group should correspond to a single host. If a LUN needs to be mapped to multiple hosts, the initiator groups representing those hosts should be aggregated into a parent initiator group and the LUN should be mapped to that initiator group. For multi-ported hosts, initiators have a comment property where the port corresponding to the initiator can be documented.<br/>
The initiator group REST API allows you to create, update, delete, and discover initiator groups, and to add and remove initiators that can access the target and associated LUNs.<br/>
An initiator can appear in multiple initiator groups. An initiator group can be mapped to multiple LUNs. A specific initiator can be mapped to a specific LUN only once. With the introduction of nestable initiator groups, best practice is to use the hierarchy such that an initiator is only a direct member of a single initiator group, and that initiator group can then be referenced by other initiator groups. This avoid needing to update multiple initiator groups when initiators change.<br/>
All initiators or nested initiator groups in an initiator group must be from the same operating system. The initiator group's operating system is specified when the initiator group is created.<br/>
When an initiator group is created, the `protocol` property is used to restrict member initiators to Fibre Channel (_fcp_), iSCSI (_iscsi_), or both (_mixed_). Initiator groups within a nested hierarchy may not have conflicting protocols.<br/>
Zero or more initiators or nested initiator groups can be supplied when the initiator group is created. After creation, initiators can be added or removed from the initiator group using the `/protocols/san/igroups/{igroup.uuid}/initiators` endpoint. Initiator groups containing other initiator groups report the aggregated list of initiators from all nested initiator groups, but modifications of the initiator list must be performed on the initiator group that directly contains the initiators. See [`POST /protocols/san/igroups/{igroup.uuid}/initiators`](#/SAN/igroup_initiator_create) and [`DELETE /protocols/san/igroups/{igroup.uuid}/initiators/{name}`](#/SAN/igroup_initiator_delete) for more details.<br/>
An FC WWPN consists of 16 hexadecimal digits grouped as 8 pairs separated by colons. The format for an iSCSI IQN is _iqn.yyyy-mm.reverse_domain_name:any_. The iSCSI EUI format consists of the _eui._ prefix followed by 16 hexadecimal characters.
## Examples
### Creating an initiator group with no initiators
The example initiator group used here is for Linux iSCSI initiators only. Note that the `return_records` query parameter is used to obtain the newly created initiator group in the response.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Igroup()
    resource.svm = {"name": "svm1"}
    resource.name = "igroup1"
    resource.os_type = "linux"
    resource.protocol = "iscsi"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
Igroup(
    {
        "os_type": "linux",
        "protocol": "iscsi",
        "name": "igroup1",
        "uuid": "8f249e7d-ab9f-11e8-b8a3-005056bb7072",
        "_links": {
            "self": {
                "href": "/api/protocols/san/igroups/8f249e7d-ab9f-11e8-b8a3-005056bb7072"
            }
        },
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"}
            },
            "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
        },
    }
)

```
</div>
</div>

---
### Creating an initiator group with initiators
The example initiator group used here is for Windows. FC Protocol and iSCSI initiators are allowed. Note that the `return_records` query parameter is used to obtain the newly created initiator group in the response.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Igroup()
    resource.svm = {"name": "svm1"}
    resource.name = "igroup2"
    resource.os_type = "windows"
    resource.protocol = "mixed"
    resource.initiators = [
        {"name": "20:01:00:50:56:bb:70:72"},
        {"name": "iqn.1991-05.com.ms:host1"},
    ]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
Igroup(
    {
        "os_type": "windows",
        "protocol": "mixed",
        "name": "igroup2",
        "uuid": "abf9c39d-ab9f-11e8-b8a3-005056bb7072",
        "_links": {
            "self": {
                "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072"
            }
        },
        "initiators": [
            {
                "name": "20:01:00:50:56:bb:70:72",
                "_links": {
                    "self": {
                        "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072/initiators/20:01:00:50:56:bb:70:72"
                    }
                },
            },
            {
                "name": "iqn.1991-05.com.ms:host1",
                "_links": {
                    "self": {
                        "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072/initiators/iqn.1991-05.com.ms:host1"
                    }
                },
            },
        ],
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"}
            },
            "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
        },
    }
)

```
</div>
</div>

---
### Creating an initiator group with nested initiator groups
The example initiator group used here is for Windows. FC Protocol and iSCSI initiators are allowed. Note that the `return_records` query parameter is used to obtain the newly created initiator group in the response. The new initiator group is create so as to contain the initiator group created in the previous example. The initiators list reports all initiators nested below this initiator group, and note that the href link for the initiators refers to the initiator group that directly owns the initiator, not this initiator group.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Igroup()
    resource.svm = {"name": "svm1"}
    resource.name = "igroup3"
    resource.os_type = "windows"
    resource.protocol = "mixed"
    resource.igroups = [{"name": "igroup2"}]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
Igroup(
    {
        "os_type": "windows",
        "protocol": "mixed",
        "name": "igroup3",
        "uuid": "abf9c39d-ab9f-11e8-b8a3-005056bb7073",
        "igroups": [
            {
                "name": "igroup2",
                "uuid": "abf9c39d-ab9f-11e8-b8a3-005056bb7072",
                "_links": {
                    "self": {
                        "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072"
                    }
                },
            }
        ],
        "_links": {
            "self": {
                "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7073"
            }
        },
        "initiators": [
            {
                "igroup": {
                    "name": "igroup2",
                    "uuid": "abf9c39d-ab9f-11e8-b8a3-005056bb7072",
                    "_links": {
                        "self": {
                            "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072"
                        }
                    },
                },
                "name": "20:01:00:50:56:bb:70:72",
                "_links": {
                    "self": {
                        "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072/initiators/20:01:00:50:56:bb:70:72"
                    }
                },
            },
            {
                "igroup": {
                    "name": "igroup2",
                    "uuid": "abf9c39d-ab9f-11e8-b8a3-005056bb7072",
                    "_links": {
                        "self": {
                            "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072"
                        }
                    },
                },
                "name": "iqn.1991-05.com.ms:host1",
                "_links": {
                    "self": {
                        "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072/initiators/iqn.1991-05.com.ms:host1"
                    }
                },
            },
        ],
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"}
            },
            "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
        },
    }
)

```
</div>
</div>

---
### Retrieving all initiator groups
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Igroup.get_collection()))

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
[
    Igroup(
        {
            "name": "igroup1",
            "uuid": "8f249e7d-ab9f-11e8-b8a3-005056bb7072",
            "_links": {
                "self": {
                    "href": "/api/protocols/san/igroups/8f249e7d-ab9f-11e8-b8a3-005056bb7072"
                }
            },
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"
                    }
                },
                "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
            },
        }
    ),
    Igroup(
        {
            "name": "igroup2",
            "uuid": "abf9c39d-ab9f-11e8-b8a3-005056bb7072",
            "_links": {
                "self": {
                    "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072"
                }
            },
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"
                    }
                },
                "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
            },
        }
    ),
    Igroup(
        {
            "name": "igroup3",
            "uuid": "abf9c39d-ab9f-11e8-b8a3-005056bb7073",
            "_links": {
                "self": {
                    "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7073"
                }
            },
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"
                    }
                },
                "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving all properties of all initiator groups
The `fields` query parameter is used to request all initiator group
properties. Note that the nested and parent initiator groups are considered
expensive properties and will only be returned if explicitly requested.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Igroup.get_collection(fields="*,igroups,parent_igroups")))

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
[
    Igroup(
        {
            "os_type": "linux",
            "protocol": "iscsi",
            "name": "igroup1",
            "uuid": "8f249e7d-ab9f-11e8-b8a3-005056bb7072",
            "_links": {
                "self": {
                    "href": "/api/protocols/san/igroups/8f249e7d-ab9f-11e8-b8a3-005056bb7072"
                }
            },
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"
                    }
                },
                "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
            },
        }
    ),
    Igroup(
        {
            "os_type": "windows",
            "protocol": "mixed",
            "name": "igroup2",
            "uuid": "abf9c39d-ab9f-11e8-b8a3-005056bb7072",
            "_links": {
                "self": {
                    "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072"
                }
            },
            "initiators": [
                {
                    "name": "20:01:00:50:56:bb:70:72",
                    "_links": {
                        "self": {
                            "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072/initiators/20:01:00:50:56:bb:70:72"
                        }
                    },
                },
                {
                    "name": "iqn.1991-05.com.ms:host1",
                    "_links": {
                        "self": {
                            "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072/initiators/iqn.1991-05.com.ms:host1"
                        }
                    },
                },
            ],
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"
                    }
                },
                "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
            },
            "parent_igroups": [
                {
                    "name": "igroup3",
                    "uuid": "abf9c39d-ab9f-11e8-b8a3-005056bb7073",
                    "_links": {
                        "self": {
                            "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7073"
                        }
                    },
                }
            ],
        }
    ),
    Igroup(
        {
            "os_type": "windows",
            "protocol": "mixed",
            "name": "igroup3",
            "uuid": "abf9c39d-ab9f-11e8-b8a3-005056bb7073",
            "igroups": [
                {
                    "name": "igroup2",
                    "uuid": "abf9c39d-ab9f-11e8-b8a3-005056bb7072",
                    "_links": {
                        "self": {
                            "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072"
                        }
                    },
                }
            ],
            "_links": {
                "self": {
                    "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7073"
                }
            },
            "initiators": [
                {
                    "igroup": {
                        "name": "igroup2",
                        "uuid": "abf9c39d-ab9f-11e8-b8a3-005056bb7072",
                        "_links": {
                            "self": {
                                "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072"
                            }
                        },
                    },
                    "name": "20:01:00:50:56:bb:70:72",
                    "_links": {
                        "self": {
                            "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072/initiators/20:01:00:50:56:bb:70:72"
                        }
                    },
                },
                {
                    "igroup": {
                        "name": "igroup2",
                        "uuid": "abf9c39d-ab9f-11e8-b8a3-005056bb7072",
                        "_links": {
                            "self": {
                                "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072"
                            }
                        },
                    },
                    "name": "iqn.1991-05.com.ms:host1",
                    "_links": {
                        "self": {
                            "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072/initiators/iqn.1991-05.com.ms:host1"
                        }
                    },
                },
            ],
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"
                    }
                },
                "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving all initiator groups for Linux
The `os_type` query parameter is used to perform the query.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Igroup.get_collection(os_type="linux")))

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
[
    Igroup(
        {
            "os_type": "linux",
            "name": "igroup1",
            "uuid": "8f249e7d-ab9f-11e8-b8a3-005056bb7072",
            "_links": {
                "self": {
                    "href": "/api/protocols/san/igroups/8f249e7d-ab9f-11e8-b8a3-005056bb7072"
                }
            },
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"
                    }
                },
                "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
            },
        }
    )
]

```
</div>
</div>

---
### Retrieving a specific initiator group
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Igroup(uuid="8f249e7d-ab9f-11e8-b8a3-005056bb7072")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
Igroup(
    {
        "os_type": "linux",
        "protocol": "iscsi",
        "name": "igroup1",
        "uuid": "8f249e7d-ab9f-11e8-b8a3-005056bb7072",
        "_links": {
            "self": {
                "href": "/api/protocols/san/igroups/8f249e7d-ab9f-11e8-b8a3-005056bb7072"
            }
        },
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"}
            },
            "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
        },
    }
)

```
</div>
</div>

---
### Retrieving LUNs mapped to a specific initiator group
The `fields` parameter is used to specify the desired properties.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Igroup(uuid="8f249e7d-ab9f-11e8-b8a3-005056bb7072")
    resource.get(fields="lun_maps")
    print(resource)

```
<div class="try_it_out">
<input id="example7_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example7_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example7_result" class="try_it_out_content">
```
Igroup(
    {
        "lun_maps": [
            {
                "lun": {
                    "name": "/vol/vol1/lun1",
                    "_links": {
                        "self": {
                            "href": "/api/storage/luns/4b33ba57-c4e0-4dbb-bc47-214800d18a71"
                        }
                    },
                    "node": {
                        "name": "node1",
                        "_links": {
                            "self": {
                                "href": "/api/cluster/nodes/f17182af-223f-4d51-8197-2cb2146d5c4c"
                            }
                        },
                        "uuid": "f17182af-223f-4d51-8197-2cb2146d5c4c",
                    },
                    "uuid": "4b33ba57-c4e0-4dbb-bc47-214800d18a71",
                },
                "logical_unit_number": 0,
            }
        ],
        "name": "igroup1",
        "uuid": "8f249e7d-ab9f-11e8-b8a3-005056bb7072",
        "_links": {
            "self": {
                "href": "/api/protocols/san/igroups/8f249e7d-ab9f-11e8-b8a3-005056bb7072"
            }
        },
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"}
            },
            "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
        },
    }
)

```
</div>
</div>

---
### Renaming an initiator group
Note that renaming an initiator group must be done in a PATCH request separate from any other modifications.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Igroup(uuid="8f249e7d-ab9f-11e8-b8a3-005056bb7072")
    resource.name = "igroup1_newName"
    resource.patch()

```

---
### Changing the operating system type of an initiator group
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Igroup(uuid="8f249e7d-ab9f-11e8-b8a3-005056bb7072")
    resource.os_type = "aix"
    resource.patch()

```

---
### Adding an initiator to an initiator group
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IgroupInitiator

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IgroupInitiator("8f249e7d-ab9f-11e8-b8a3-005056bb7072")
    resource.name = "iqn.1991-05.com.ms:host2"
    resource.post(hydrate=True)
    print(resource)

```

---
### Adding multiple initiators to an initiator group
Note the use of the `records` property to add multiple initiators to the initiator group in a single API call.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IgroupInitiator

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IgroupInitiator("8f249e7d-ab9f-11e8-b8a3-005056bb7072")
    resource.records = [
        {"name": "iqn.1991-05.com.ms:host3"},
        {"name": "iqn.1991-05.com.ms:host4"},
    ]
    resource.post(hydrate=True)
    print(resource)

```

---
### Removing an initiator from an initiator group
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IgroupInitiator

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IgroupInitiator(
        "8f249e7d-ab9f-11e8-b8a3-005056bb7072", name="iqn.1991-05.com.ms:host3"
    )
    resource.delete()

```

---
### Removing an initiator from a mapped initiator group
Normally, removing an initiator from an initiator group that is mapped to a LUN is not allowed. The removal can be forced using the `allow_delete_while_mapped` query parameter.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IgroupInitiator

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IgroupInitiator(
        "8f249e7d-ab9f-11e8-b8a3-005056bb7072", name="iqn.1991-05.com.ms:host4"
    )
    resource.delete(allow_delete_while_mapped=True)

```

---
### Adding a nested initiator group to an initiator group
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IgroupNested

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IgroupNested("8f249e7d-ab9f-11e8-b8a3-005056bb7072")
    resource.name = "host2_igroup"
    resource.post(hydrate=True)
    print(resource)

```

---
### Adding multiple nested initiator groups to an initiator group
Note the use of the `records` property to add multiple nested initiator groups to the initiator group in a single API call.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IgroupNested

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IgroupNested("8f249e7d-ab9f-11e8-b8a3-005056bb7072")
    resource.records = [
        {"name": "host3_igroup"},
        {"uuid": "c439efc8-0a70-11eb-adc1-0242ac120002"},
    ]
    resource.post(hydrate=True)
    print(resource)

```

---
### Removing a nested initiator group from an initiator group
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IgroupNested

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IgroupNested(
        "8f249e7d-ab9f-11e8-b8a3-005056bb7072",
        uuid="c439efc8-0a70-11eb-adc1-0242ac120002",
    )
    resource.delete()

```

---
### Removing a nested initiator group from a mapped initiator group
Normally, removing a nested initiator group from an initiator group that is mapped to a LUN is not allowed. The removal can be forced using the `allow_delete_while_mapped` query parameter.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IgroupNested

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IgroupNested(
        "8f249e7d-ab9f-11e8-b8a3-005056bb7072",
        uuid="c439efc8-0a70-11eb-adc1-0242ac120002",
    )
    resource.delete(allow_delete_while_mapped=True)

```

---
### Deleting an initiator group
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Igroup(uuid="abf9c39d-ab9f-11e8-b8a3-005056bb7072")
    resource.delete()

```

---
### Deleting a mapped initiator group
Normally, deleting an initiator group that is mapped to a LUN is not allowed. The deletion can be forced using the `allow_delete_while_mapped` query parameter.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Igroup(uuid="abf9c39d-ab9f-11e8-b8a3-005056bb7072")
    resource.delete(allow_delete_while_mapped=True)

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


__all__ = ["Igroup", "IgroupSchema"]
__pdoc__ = {
    "IgroupSchema.resource": False,
    "IgroupSchema.opts": False,
}


class IgroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Igroup object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the igroup."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        validate=len_validation(minimum=0, maximum=254),
        allow_none=True,
    )
    r""" A comment available for use by the administrator. Valid in POST and PATCH."""

    connectivity_tracking = marshmallow_fields.Nested("netapp_ontap.models.igroup_connectivity_tracking.IgroupConnectivityTrackingSchema", data_key="connectivity_tracking", unknown=EXCLUDE, allow_none=True)
    r""" An overview of the connections to ONTAP by the initiators in this group."""

    delete_on_unmap = marshmallow_fields.Boolean(
        data_key="delete_on_unmap",
        allow_none=True,
    )
    r""" An option that causes the initiator group to be deleted when the last LUN map associated with it is deleted. Optional in POST and PATCH. This property defaults to _false_ when the initiator group is created."""

    igroups = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.igroup_child.IgroupChildSchema", unknown=EXCLUDE, allow_none=True), data_key="igroups", allow_none=True)
    r""" The existing initiator groups that are members of the group. Optional in POST.<br/>
This property is mutually exclusive with the _initiators_ property during POST.<br/>
This array contains only the direct children of the initiator group. If the member initiator groups have further nested initiator groups, those are reported in the `igroups` property of the child initiator group.<br/>
Zero or more nested initiator groups can be supplied when the initiator group is created. The initiator group will act as if it contains the aggregation of all initiators in any nested initiator groups.<br/>
After creation, nested initiator groups can be added or removed from the initiator group using the `/protocols/san/igroups/{igroup.uuid}/igroups` endpoint. See [`POST /protocols/san/igroups/{igroup.uuid}/igroups`](#/SAN/igroup_nested_create) and [`DELETE /protocols/san/igroups/{igroup.uuid}/igroups/{uuid}`](#/SAN/igroup_nested_delete) for more details."""

    initiators = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.igroup_initiator_list_item.IgroupInitiatorListItemSchema", unknown=EXCLUDE, allow_none=True), data_key="initiators", allow_none=True)
    r""" The initiators that are members of the group or any group nested below this group. Optional in POST.<br/>
This property is mutually exclusive with the _igroups_ property during POST.<br/>
During GET, this array contains initiators that are members of this group or any nested initiator groups below this group. When initiators of nested groups are returned, they include links to the initiator group that directly contains the initiator.<br/>
Zero or more initiators can be supplied when the initiator group is created. After creation, initiators can be added or removed from the initiator group using the `/protocols/san/igroups/{igroup.uuid}/initiators` endpoint. See [`POST /protocols/san/igroups/{igroup.uuid}/initiators`](#/SAN/igroup_initiator_create) and [`DELETE /protocols/san/igroups/{igroup.uuid}/initiators/{name}`](#/SAN/igroup_initiator_delete) for more details."""

    lun_maps = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.igroup_lun_maps.IgroupLunMapsSchema", unknown=EXCLUDE, allow_none=True), data_key="lun_maps", allow_none=True)
    r""" All LUN maps with which the initiator is associated.<br/>
If the requested igroup is part of a remote, non-local, MetroCluster SVM, the LUN maps are not retrieved.<br/>
There is an added computational cost to retrieving property values for `lun_maps`. They are not populated for either a collection GET or an instance GET unless explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more."""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=96),
        allow_none=True,
    )
    r""" The name of the initiator group. Required in POST; optional in PATCH.


Example: igroup1"""

    os_type = marshmallow_fields.Str(
        data_key="os_type",
        validate=enum_validation(['aix', 'hpux', 'hyper_v', 'linux', 'netware', 'openvms', 'solaris', 'vmware', 'windows', 'xen']),
        allow_none=True,
    )
    r""" The host operating system of the initiator group. All initiators in the group should be hosts of the same operating system. Required in POST; optional in PATCH.


Valid choices:

* aix
* hpux
* hyper_v
* linux
* netware
* openvms
* solaris
* vmware
* windows
* xen"""

    parent_igroups = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.igroup_parent.IgroupParentSchema", unknown=EXCLUDE, allow_none=True), data_key="parent_igroups", allow_none=True)
    r""" The initiator groups that contain this initiator group as a member."""

    portset = marshmallow_fields.Nested("netapp_ontap.resources.portset.PortsetSchema", data_key="portset", unknown=EXCLUDE, allow_none=True)
    r""" The portset field of the igroup."""

    protocol = marshmallow_fields.Str(
        data_key="protocol",
        validate=enum_validation(['fcp', 'iscsi', 'mixed']),
        allow_none=True,
    )
    r""" The protocols supported by the initiator group. This restricts the type of initiators that can be added to the initiator group. Optional in POST; if not supplied, this defaults to _mixed_.<br/>
The protocol of an initiator group cannot be changed after creation of the group.


Valid choices:

* fcp
* iscsi
* mixed"""

    replication = marshmallow_fields.Nested("netapp_ontap.models.igroup_replication.IgroupReplicationSchema", data_key="replication", unknown=EXCLUDE, allow_none=True)
    r""" Properties related to initiator group replication."""

    supports_igroups = marshmallow_fields.Boolean(
        data_key="supports_igroups",
        allow_none=True,
    )
    r""" An initiator group may contain either initiators or other initiator groups, but not both simultaneously. This property is _true_ when initiator groups can be added to this initiator group. The `initiators.name` property cannot be used to determine this via a query because it reports initiators inherited from nested igroups."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the igroup."""

    target = marshmallow_fields.Nested("netapp_ontap.models.igroup_target.IgroupTargetSchema", data_key="target", unknown=EXCLUDE, allow_none=True)
    r""" Properties of the SCSI target to which the initiator group provides access."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The unique identifier of the initiator group.


Example: 4ea7a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return Igroup

    gettable_fields = [
        "links",
        "comment",
        "connectivity_tracking",
        "delete_on_unmap",
        "igroups",
        "initiators",
        "lun_maps",
        "name",
        "os_type",
        "parent_igroups",
        "portset.links",
        "portset.name",
        "portset.uuid",
        "protocol",
        "replication",
        "supports_igroups",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "target",
        "uuid",
    ]
    """links,comment,connectivity_tracking,delete_on_unmap,igroups,initiators,lun_maps,name,os_type,parent_igroups,portset.links,portset.name,portset.uuid,protocol,replication,supports_igroups,svm.links,svm.name,svm.uuid,target,uuid,"""

    patchable_fields = [
        "comment",
        "delete_on_unmap",
        "name",
        "os_type",
        "portset.name",
        "portset.uuid",
        "replication",
    ]
    """comment,delete_on_unmap,name,os_type,portset.name,portset.uuid,replication,"""

    postable_fields = [
        "comment",
        "delete_on_unmap",
        "igroups",
        "initiators",
        "name",
        "os_type",
        "portset.name",
        "portset.uuid",
        "protocol",
        "replication",
        "svm.name",
        "svm.uuid",
    ]
    """comment,delete_on_unmap,igroups,initiators,name,os_type,portset.name,portset.uuid,protocol,replication,svm.name,svm.uuid,"""

class Igroup(Resource):
    r""" An initiator group (igroup) is a collection of Fibre Channel (FC) world wide port names (WWPNs), and/or iSCSI Qualified Names (IQNs), and/or iSCSI EUIs (Extended Unique Identifiers) that identify host endpoints.<br/>
Initiator groups are used to control which hosts can access specific LUNs. To grant access to a LUN from one or more hosts, create an initiator group containing the host initiator names, then create a LUN map that associates the initiator group with the LUN.<br/>
An initiator group may contain either initiators or other initiator groups, but not both simultaneously. When a parent initiator group is mapped, it inherits all of the initiators of any initiator groups nested below it. If any nested initiator group is modified to contain different initiators, the parent initiator groups inherit the change. A parent can have many nested initiator groups and an initiator group can be nested under multiple parents. Initiators can only be added or removed from the initiator group that directly contains them. The maximum supported depth of nesting is three layers.<br/>
Best practice when using nested initiator groups is to match host hierarchies. A single initiator group should correspond to a single host. If a LUN needs to be mapped to multiple hosts, the initiator groups representing those hosts should be aggregated into a parent initiator group and the LUN should be mapped to that initiator group. For multi-ported hosts, initiators have a comment property where the port corresponding to the initiator can be documented.<br/>
An initiator can appear in multiple initiator groups. An initiator group can be mapped to multiple LUNs. A specific initiator can be mapped to a specific LUN only once. With the introduction of nestable initiator groups, best practice is to use the hierarchy such that an initiator is only a direct member of a single initiator group, and that initiator group can then be referenced by other initiator groups.<br/>
All initiators or nested initiator groups in an initiator group must be from the same operating system. The initiator group's operating system is specified when the initiator group is created.<br/>
When an initiator group is created, the `protocol` property is used to restrict member initiators to Fibre Channel (_fcp_), iSCSI (_iscsi_), or both (_mixed_). Initiator groups within a nested hierarchy may not have conflicting protocols.<br/>
Zero or more initiators or nested initiator groups can be supplied when the initiator group is created. After creation, initiators can be added or removed from the initiator group using the `/protocols/san/igroups/{igroup.uuid}/initiators` endpoint. Initiator groups containing other initiator groups report the aggregated list of initiators from all nested initiator groups, but modifications of the initiator list must be performed on the initiator group that directly contains the initiators. See [`POST /protocols/san/igroups/{igroup.uuid}/initiators`](#/SAN/igroup_initiator_create) and [`DELETE /protocols/san/igroups/{igroup.uuid}/initiators/{name}`](#/SAN/igroup_initiator_delete) for more details.<br/> """

    _schema = IgroupSchema
    _path = "/api/protocols/san/igroups"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves initiator groups.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `connectivity_tracking.*`
* `igroups.*`
* `lun_maps.*`
* `parent_igroups.*`
* `target.*`
### Related ONTAP commands
* `lun igroup show`
* `lun mapping show`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
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
        """Returns a count of all Igroup resources that match the provided query"""
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
        """Returns a list of RawResources that represent Igroup resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Igroup"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates an initiator group.
### Related ONTAP commands
* `lun igroup modify`
* `lun igroup rename`
* `lun igroup bind`
* `lun igroup unbind`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["Igroup"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Igroup"], NetAppResponse]:
        r"""Creates an initiator group.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the initiator group.
* `name` - Name of the initiator group.
* `os_type` - Operating system of the initiator group's initiators.
### Recommended optional properties
* `initiators.name` - Name(s) of initiator group's initiators. This property can be used to create the initiator group and populate it with initiators in a single request.
### Default property values
If not specified in POST, the following default property values are assigned.
* `protocol` - _mixed_ - Data protocol of the initiator group's initiators.
### Related ONTAP commands
* `lun igroup create`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
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
        records: Iterable["Igroup"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an initiator group.
### Related ONTAP commands
* `lun igroup delete`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves initiator groups.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `connectivity_tracking.*`
* `igroups.*`
* `lun_maps.*`
* `parent_igroups.*`
* `target.*`
### Related ONTAP commands
* `lun igroup show`
* `lun mapping show`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an initiator group.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `connectivity_tracking.*`
* `igroups.*`
* `lun_maps.*`
* `parent_igroups.*`
### Related ONTAP commands
* `lun igroup show`
* `lun mapping show`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
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
        r"""Creates an initiator group.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the initiator group.
* `name` - Name of the initiator group.
* `os_type` - Operating system of the initiator group's initiators.
### Recommended optional properties
* `initiators.name` - Name(s) of initiator group's initiators. This property can be used to create the initiator group and populate it with initiators in a single request.
### Default property values
If not specified in POST, the following default property values are assigned.
* `protocol` - _mixed_ - Data protocol of the initiator group's initiators.
### Related ONTAP commands
* `lun igroup create`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
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
        r"""Updates an initiator group.
### Related ONTAP commands
* `lun igroup modify`
* `lun igroup rename`
* `lun igroup bind`
* `lun igroup unbind`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
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
        r"""Deletes an initiator group.
### Related ONTAP commands
* `lun igroup delete`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


