r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
A consistency group is a group of volumes that supports capabilities such as creating a snapshot of all of its member volumes at the same point-in-time with a write-fence, thus ensuring a consistent image of the volumes at that time.
<br>Applications with datasets scoped to a single volume can have its contents saved to a snapshot, replicated, or cloned in a crash-consistent manner implicitly with corresponding native ONTAP volume-granular operations. Applications with datasets spanning a group of multiple volumes must have such operations performed on the group. Typically, by first fencing writes to all the volumes in the group, flushing any writes pending in queues, executing the intended operation, that is, take snapshot of every volume in the group and when that is complete, unfence and resume writes. A consistency group is the conventional mechanism for providing such group semantics.
## Consistency group  APIs
The following APIs are used to perform operations related to consistency groups:

* GET       /api/application/consistency-groups
* POST      /api/application/consistency-groups
* GET       /api/application/consistency-groups/{uuid}
* PATCH     /api/application/consistency-groups/{uuid}
* DELETE    /api/application/consistency-groups/{uuid}
## Examples
### Retrieving all consistency groups of an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(ConsistencyGroup.get_collection(**{"svm.name": "vs1"})))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    ConsistencyGroup(
        {
            "name": "vol1",
            "_links": {
                "self": {
                    "href": "/api/application/consistency-groups/6f48d798-0a7f-11ec-a449-005056bbcf9f"
                }
            },
            "uuid": "6f48d798-0a7f-11ec-a449-005056bbcf9f",
        }
    ),
    ConsistencyGroup(
        {
            "name": "parent_cg",
            "_links": {
                "self": {
                    "href": "/api/application/consistency-groups/c1b22c85-0a82-11ec-a449-005056bbcf9f"
                }
            },
            "uuid": "c1b22c85-0a82-11ec-a449-005056bbcf9f",
        }
    ),
    ConsistencyGroup(
        {
            "name": "child_1",
            "_links": {
                "self": {
                    "href": "/api/application/consistency-groups/c1b270b1-0a82-11ec-a449-005056bbcf9f"
                }
            },
            "uuid": "c1b270b1-0a82-11ec-a449-005056bbcf9f",
        }
    ),
    ConsistencyGroup(
        {
            "name": "child_2",
            "_links": {
                "self": {
                    "href": "/api/application/consistency-groups/c1b270c3-0a82-11ec-a449-005056bbcf9f"
                }
            },
            "uuid": "c1b270c3-0a82-11ec-a449-005056bbcf9f",
        }
    ),
]

```
</div>
</div>

### Retrieving details of all consistency groups of an SVM
Retrieving details of the consistency groups for a specified SVM. These details are considered to be performant and will return within 1 second when 40 records or less are requested.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            ConsistencyGroup.get_collection(
                fields="*", max_records=40, **{"svm.name": "vs1"}
            )
        )
    )

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    ConsistencyGroup(
        {
            "replicated": False,
            "name": "vol1",
            "_links": {
                "self": {
                    "href": "/api/application/consistency-groups/6f48d798-0a7f-11ec-a449-005056bbcf9f"
                }
            },
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/4853f97a-0a63-11ec-a449-005056bbcf9f"
                    }
                },
                "uuid": "4853f97a-0a63-11ec-a449-005056bbcf9f",
            },
            "uuid": "6f48d798-0a7f-11ec-a449-005056bbcf9f",
            "space": {"available": 107704320, "used": 299008, "size": 108003328},
        }
    ),
    ConsistencyGroup(
        {
            "replicated": False,
            "name": "parent_cg",
            "_links": {
                "self": {
                    "href": "/api/application/consistency-groups/c1b22c85-0a82-11ec-a449-005056bbcf9f"
                }
            },
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/4853f97a-0a63-11ec-a449-005056bbcf9f"
                    }
                },
                "uuid": "4853f97a-0a63-11ec-a449-005056bbcf9f",
            },
            "consistency_groups": [
                {
                    "space": {"available": 39346176, "used": 499712, "size": 41943040},
                    "name": "child_1",
                    "uuid": "c1b270b1-0a82-11ec-a449-005056bbcf9f",
                    "_links": {
                        "self": {
                            "href": "/api/application/consistency-groups/c1b270b1-0a82-11ec-a449-005056bbcf9f"
                        }
                    },
                },
                {
                    "space": {"available": 39350272, "used": 495616, "size": 41943040},
                    "name": "child_2",
                    "uuid": "c1b270c3-0a82-11ec-a449-005056bbcf9f",
                    "_links": {
                        "self": {
                            "href": "/api/application/consistency-groups/c1b270c3-0a82-11ec-a449-005056bbcf9f"
                        }
                    },
                },
            ],
            "uuid": "c1b22c85-0a82-11ec-a449-005056bbcf9f",
            "snapshot_policy": {
                "name": "default-1weekly",
                "uuid": "a30bd0fe-067d-11ec-a449-005056bbcf9f",
                "_links": {
                    "self": {
                        "href": "/api/storage/snapshot-policies/a30bd0fe-067d-11ec-a449-005056bbcf9f"
                    }
                },
            },
            "space": {"available": 78696448, "used": 995328, "size": 83886080},
        }
    ),
    ConsistencyGroup(
        {
            "name": "child_1",
            "_links": {
                "self": {
                    "href": "/api/application/consistency-groups/c1b270b1-0a82-11ec-a449-005056bbcf9f"
                }
            },
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/4853f97a-0a63-11ec-a449-005056bbcf9f"
                    }
                },
                "uuid": "4853f97a-0a63-11ec-a449-005056bbcf9f",
            },
            "uuid": "c1b270b1-0a82-11ec-a449-005056bbcf9f",
            "parent_consistency_group": {
                "name": "parent_cg",
                "_links": {
                    "self": {
                        "href": "/api/application/consistency-groups/c1b22c85-0a82-11ec-a449-005056bbcf9f"
                    }
                },
                "uuid": "c1b22c85-0a82-11ec-a449-005056bbcf9f",
            },
            "snapshot_policy": {
                "name": "default",
                "uuid": "a30b60a4-067d-11ec-a449-005056bbcf9f",
                "_links": {
                    "self": {
                        "href": "/api/storage/snapshot-policies/a30b60a4-067d-11ec-a449-005056bbcf9f"
                    }
                },
            },
            "space": {"available": 39346176, "used": 499712, "size": 41943040},
        }
    ),
    ConsistencyGroup(
        {
            "name": "child_2",
            "_links": {
                "self": {
                    "href": "/api/application/consistency-groups/c1b270c3-0a82-11ec-a449-005056bbcf9f"
                }
            },
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/4853f97a-0a63-11ec-a449-005056bbcf9f"
                    }
                },
                "uuid": "4853f97a-0a63-11ec-a449-005056bbcf9f",
            },
            "uuid": "c1b270c3-0a82-11ec-a449-005056bbcf9f",
            "parent_consistency_group": {
                "name": "parent_cg",
                "_links": {
                    "self": {
                        "href": "/api/application/consistency-groups/c1b22c85-0a82-11ec-a449-005056bbcf9f"
                    }
                },
                "uuid": "c1b22c85-0a82-11ec-a449-005056bbcf9f",
            },
            "snapshot_policy": {
                "name": "default",
                "uuid": "a30b60a4-067d-11ec-a449-005056bbcf9f",
                "_links": {
                    "self": {
                        "href": "/api/storage/snapshot-policies/a30b60a4-067d-11ec-a449-005056bbcf9f"
                    }
                },
            },
            "space": {"available": 39350272, "used": 495616, "size": 41943040},
        }
    ),
]

```
</div>
</div>

### Retrieving details of non-nested consistency groups
Retrieves details of the consistency groups without nested consistency groups, or only the parent consistency group for a number of consistency groups of a specified SVM.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            ConsistencyGroup.get_collection(
                **{"svm.name": "vs1", "parent_consistency_group.uuid": "null"}
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
    ConsistencyGroup(
        {
            "name": "vol1",
            "_links": {
                "self": {
                    "href": "/api/application/consistency-groups/6f48d798-0a7f-11ec-a449-005056bbcf9f"
                }
            },
            "svm": {"name": "vs1"},
            "uuid": "6f48d798-0a7f-11ec-a449-005056bbcf9f",
        }
    ),
    ConsistencyGroup(
        {
            "name": "parent_cg",
            "_links": {
                "self": {
                    "href": "/api/application/consistency-groups/c1b22c85-0a82-11ec-a449-005056bbcf9f"
                }
            },
            "svm": {"name": "vs1"},
            "uuid": "c1b22c85-0a82-11ec-a449-005056bbcf9f",
        }
    ),
]

```
</div>
</div>

### Creating a single consistency group with a new SAN volume
Provisions an application with one consistency group, each with one new SAN volumes, with one LUN, an igroup and no explicit snapshot policy, FabricPool tiering policy, storage service, and QoS policy specification. The igroup to map a LUN to is specified at LUN-granularity.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroup()
    resource.svm = {"name": "vs1"}
    resource.luns = [
        {
            "name": "/vol/vol1/lun1",
            "space": {"size": "100mb"},
            "os_type": "linux",
            "lun_maps": [
                {
                    "igroup": {
                        "name": "igroup1",
                        "initiators": [{"name": "example_name"}],
                    }
                }
            ],
        }
    ]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
ConsistencyGroup(
    {
        "name": "vol1",
        "luns": [
            {
                "os_type": "linux",
                "lun_maps": [
                    {
                        "igroup": {
                            "name": "igroup1",
                            "initiators": [{"name": "example_name"}],
                        }
                    }
                ],
                "space": {"size": 104857600},
                "name": "/vol/vol1/lun1",
            }
        ],
        "svm": {
            "name": "vs1",
            "_links": {
                "self": {"href": "/api/svm/svms/4853f97a-0a63-11ec-a449-005056bbcf9f"}
            },
            "uuid": "4853f97a-0a63-11ec-a449-005056bbcf9f",
        },
        "uuid": "6f48d798-0a7f-11ec-a449-005056bbcf9f",
    }
)

```
</div>
</div>

### Creating an Application with two consistency groups with existing SAN volumes
Provisions an application with two consistency groups, each with two existing SAN volumes, a snapshot policy at application-granularity, and a distinct consistency group granular snapshot policy.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroup()
    resource.svm = {"name": "vs1"}
    resource.name = "parent_cg"
    resource.snapshot_policy = {"name": "default-1weekly"}
    resource.consistency_groups = [
        {
            "name": "child_1",
            "snapshot_policy": {"name": "default"},
            "volumes": [
                {"name": "existing_vol1", "provisioning_options": {"action": "add"}},
                {"name": "existing_vol2", "provisioning_options": {"action": "add"}},
            ],
        },
        {
            "name": "child_2",
            "snapshot_policy": {"name": "default"},
            "volumes": [
                {"name": "existing_vol3", "provisioning_options": {"action": "add"}},
                {"name": "existing_vol4", "provisioning_options": {"action": "add"}},
            ],
        },
    ]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
ConsistencyGroup(
    {
        "name": "parent_cg",
        "svm": {
            "name": "vs1",
            "_links": {
                "self": {"href": "/api/svm/svms/4853f97a-0a63-11ec-a449-005056bbcf9f"}
            },
            "uuid": "4853f97a-0a63-11ec-a449-005056bbcf9f",
        },
        "consistency_groups": [
            {
                "volumes": [{"name": "existing_vol1"}, {"name": "existing_vol2"}],
                "name": "child_1",
                "uuid": "c1b270b1-0a82-11ec-a449-005056bbcf9f",
                "snapshot_policy": {"name": "default"},
            },
            {
                "volumes": [{"name": "existing_vol3"}, {"name": "existing_vol4"}],
                "name": "child_2",
                "uuid": "c1b270c3-0a82-11ec-a449-005056bbcf9f",
                "snapshot_policy": {"name": "default"},
            },
        ],
        "uuid": "c1b22c85-0a82-11ec-a449-005056bbcf9f",
        "snapshot_policy": {"name": "default-1weekly"},
    }
)

```
</div>
</div>

### Retrieving specific details of an existing consistency group
Retrieves the details of an existing consistency group.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroup(uuid="6f48d798-0a7f-11ec-a449-005056bbcf9f")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
ConsistencyGroup(
    {
        "replicated": False,
        "name": "vol1",
        "_links": {
            "self": {
                "href": "/api/application/consistency-groups/6f48d798-0a7f-11ec-a449-005056bbcf9f"
            }
        },
        "svm": {
            "name": "vs1",
            "_links": {
                "self": {"href": "/api/svm/svms/4853f97a-0a63-11ec-a449-005056bbcf9f"}
            },
            "uuid": "4853f97a-0a63-11ec-a449-005056bbcf9f",
        },
        "uuid": "6f48d798-0a7f-11ec-a449-005056bbcf9f",
        "space": {"available": 107724800, "used": 278528, "size": 108003328},
    }
)

```
</div>
</div>

### Retrieving all details of an existing consistency group
Retrieves all details of an existing consistency group. These details are not considered to be performant and are not guaranteed to return within one second.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroup(uuid="6f48d798-0a7f-11ec-a449-005056bbcf9f")
    resource.get(fields="**")
    print(resource)

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
ConsistencyGroup(
    {
        "replicated": False,
        "name": "vol1",
        "_links": {
            "self": {
                "href": "/api/application/consistency-groups/6f48d798-0a7f-11ec-a449-005056bbcf9f?fields=**"
            }
        },
        "luns": [
            {
                "create_time": "2021-08-31T13:18:24-04:00",
                "serial_number": "wIqM6]RfQK3t",
                "os_type": "linux",
                "lun_maps": [
                    {
                        "igroup": {
                            "os_type": "linux",
                            "protocol": "mixed",
                            "name": "igroup1",
                            "uuid": "6f4a4b86-0a7f-11ec-a449-005056bbcf9f",
                            "initiators": [{"name": "example_name"}],
                        },
                        "logical_unit_number": 0,
                    }
                ],
                "space": {
                    "guarantee": {"requested": False, "reserved": False},
                    "used": 0,
                    "size": 104857600,
                },
                "name": "/vol/vol1/lun1",
                "uuid": "6f51748a-0a7f-11ec-a449-005056bbcf9f",
            }
        ],
        "svm": {
            "name": "vs1",
            "_links": {
                "self": {"href": "/api/svm/svms/4853f97a-0a63-11ec-a449-005056bbcf9f"}
            },
            "uuid": "4853f97a-0a63-11ec-a449-005056bbcf9f",
        },
        "qos": {
            "policy": {
                "name": "extreme-fixed",
                "_links": {
                    "self": {
                        "href": "/api/storage/qos/policies/b7189398-e572-48ab-8f69-82cd46580812"
                    }
                },
                "uuid": "b7189398-e572-48ab-8f69-82cd46580812",
            }
        },
        "uuid": "6f48d798-0a7f-11ec-a449-005056bbcf9f",
        "tiering": {"policy": "none"},
        "volumes": [
            {
                "space": {"available": 107569152, "used": 434176, "size": 108003328},
                "name": "vol1",
                "comment": "",
                "qos": {
                    "policy": {
                        "name": "extreme-fixed",
                        "_links": {
                            "self": {
                                "href": "/api/storage/qos/policies/b7189398-e572-48ab-8f69-82cd46580812"
                            }
                        },
                        "uuid": "b7189398-e572-48ab-8f69-82cd46580812",
                    }
                },
                "uuid": "6f516c6c-0a7f-11ec-a449-005056bbcf9f",
                "tiering": {"policy": "none"},
                "snapshot_policy": {
                    "name": "default",
                    "uuid": "a30b60a4-067d-11ec-a449-005056bbcf9f",
                },
            }
        ],
        "space": {"available": 107569152, "used": 434176, "size": 108003328},
    }
)

```
</div>
</div>

### Adding LUNs to an existing volume in an existing consistency group
Adds two NVMe namespaces to an existing volume in an existing consistency group, creates a new subsystem, and binds the new namespaces to it.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroup(uuid="6f48d798-0a7f-11ec-a449-005056bbcf9f")
    resource.luns = [
        {
            "name": "/vol/vol1/new_luns",
            "provisioning_options": {"count": 2, "action": "create"},
            "space": {"size": "100mb"},
            "os_type": "linux",
            "lun_maps": [
                {
                    "igroup": {
                        "name": "igroup2",
                        "initiators": [{"name": "01:02:03:04:05:06:07:01"}],
                    }
                }
            ],
        }
    ]
    resource.patch()

```

### Restoring a consistency group to the contents of an existing snapshot
Restores an existing consistency group to the contents of an existing snapshot of the consistency group.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroup(uuid="6f51748a-0a7f-11ec-a449-005056bbcf9f")
    resource.restore_to = {"snapshot": {"uuid": "92c6c770-17a1-11eb-b141-005056acd498"}}
    resource.patch()

```

### Deleting a consistency group
Deletes a consistency group, where all storage originally associated with that consistency group remains in place.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroup(uuid="6f48d798-0a7f-11ec-a449-005056bbcf9f")
    resource.delete()

```

### Cloning an existing consistency group
The following example clones an existing consistency group with the current contents:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroup()
    resource.name = "clone01_of_cg01"
    resource.svm = {"name": "vs_0"}
    resource.clone = {
        "volume": {"prefix": "my_clone_pfx", "suffix": "my_clone_sfx"},
        "split_initiated": True,
        "parent_consistency_group": {
            "name": "cg01",
            "uuid": "ca5e76fb-98c0-11ec-855a-005056a7693b",
        },
        "guarantee": {"type": "none"},
    }
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example10_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example10_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example10_result" class="try_it_out_content">
```
ConsistencyGroup(
    {
        "name": "clone01_of_cg01",
        "svm": {"name": "vs_0"},
        "clone": {
            "volume": {"prefix": "my_clone_pfx", "suffix": "my_clone_sfx"},
            "guarantee": {"type": "none"},
            "parent_consistency_group": {
                "name": "cg01",
                "uuid": "ca5e76fb-98c0-11ec-855a-005056a7693b",
            },
            "split_initiated": True,
        },
    }
)

```
</div>
</div>

### Cloning a consistency group from an existing snapshot
The following example clones an existing consistency group with contents from an existing snapshot:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroup()
    resource.name = "clone01_of_cg01"
    resource.svm = {"name": "vs_0"}
    resource.clone = {
        "volume": {"prefix": "my_clone_pfx", "suffix": "my_clone_sfx"},
        "split_initiated": True,
        "parent_snapshot": {"name": "snap01_of_cg01"},
        "parent_consistency_group": {
            "name": "cg01",
            "uuid": "ca5e76fb-98c0-11ec-855a-005056a7693b",
        },
        "guarantee": {"type": "none"},
    }
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example11_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example11_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example11_result" class="try_it_out_content">
```
ConsistencyGroup(
    {
        "name": "clone01_of_cg01",
        "svm": {"name": "vs_0"},
        "clone": {
            "volume": {"prefix": "my_clone_pfx", "suffix": "my_clone_sfx"},
            "guarantee": {"type": "none"},
            "parent_consistency_group": {
                "name": "cg01",
                "uuid": "ca5e76fb-98c0-11ec-855a-005056a7693b",
            },
            "parent_snapshot": {"name": "snap01_of_cg01"},
            "split_initiated": True,
        },
    }
)

```
</div>
</div>

### Adding namespaces to an existing volume in an existing consistency group
To add two NVMe Namespaces to an existing volume in an existing consistency group, create a new subsystem and bind the new namespaces to it.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroup(uuid="6f51748a-0a7f-11ec-a449-005056bbcf9f")
    resource.namespaces = [
        {
            "name": "/vol/vol1/new_namespace",
            "space": {"size": "10M"},
            "os_type": "windows",
            "provisioning_options": {"count": 2},
            "subsystem_map": {
                "subsystem": {
                    "name": "mySubsystem",
                    "hosts": [
                        {
                            "nqn": "nqn.1992-08.com.netapp:sn.d04594ef915b4c73b642169e72e4c0b1:subsystem.host1"
                        },
                        {
                            "nqn": "nqn.1992-08.com.netapp:sn.d04594ef915b4c73b642169e72e4c0b1:subsystem.host2"
                        },
                    ],
                }
            },
        }
    ]
    resource.patch()

```

### Add a new volume in an existing consistency group
The following example adds two new volumes to an existing consistency group.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroup(uuid="6f51748a-0a7f-11ec-a449-005056bbcf9f")
    resource.volumes = [
        {
            "name": "new_vol_",
            "provisioning_options": {"count": "2"},
            "space": {"size": "1gb"},
        }
    ]
    resource.patch()

```

### Adding an existing volume to an existing consistency group
The following example adds an existing volume to an existing consistency group.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroup(uuid="6f51748a-0a7f-11ec-a449-005056bbcf9f")
    resource.volumes = [
        {"name": "existing_vol", "provisioning_options": {"action": "add"}}
    ]
    resource.patch()

```

### Promoting a single consistency group to a nested consistency group
The following example promotes a single consistency group to a
nested consistency group with a new child consistency group.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroup(uuid="6f51748a-0a7f-11ec-a449-005056bbcf9f")
    resource.provisioning_options = {"action": "promote"}
    resource.consistency_groups = [
        {"name": "cg_child", "provisioning_options": {"action": "create"}}
    ]
    resource.patch()

```

### Demoting a nested consistency group to a single consistency group
The following example demotes (flattens) a nested consistency group to a
single consistency group.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroup(uuid="6f51748a-0a7f-11ec-a449-005056bbcf9f")
    resource.provisioning_options = {"action": "demote"}
    resource.patch()

```

### Adding a new child consistency group to nested consistency group
The following example adds a new child consistency group to an
existing nested consistency group, creating a new volume.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroup(uuid="6f51748a-0a7f-11ec-a449-005056bbcf9f")
    resource.consistency_groups = [
        {
            "name": "cg_child5",
            "provisioning_options": {"action": "create"},
            "volumes": [{"name": "child5_vol_1", "space": {"size": "100mb"}}],
        }
    ]
    resource.patch()

```

### Removing a child consistency group from nested consistency group
The following example removes a child consistency group from a
nested consistency, changing it to a single consistency group
with a new consistency group name.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroup(uuid="6f51748a-0a7f-11ec-a449-005056bbcf9f")
    resource.consistency_groups = [
        {
            "name": "cg_child5",
            "provisioning_options": {"action": "remove", "name": "new_single_cg"},
        }
    ]
    resource.patch()

```

### Create a new parent consistency group with an existing consistency group
The following example creates a new nested consistency group
with an existing consistency group as child consistency group.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroup()
    resource.svm = {"name": "vs1"}
    resource.name = "cg_parent2"
    resource.consistency_groups = [
        {"name": "cg_large", "provisioning_options": {"action": "add"}},
        {"name": "cg_standalone2", "provisioning_options": {"action": "add"}},
    ]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example19_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example19_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example19_result" class="try_it_out_content">
```
ConsistencyGroup(
    {
        "name": "cg_parent2",
        "svm": {"name": "vs1"},
        "consistency_groups": [
            {"name": "cg_large", "provisioning_options": {"action": "add"}},
            {"name": "cg_standalone2", "provisioning_options": {"action": "add"}},
        ],
    }
)

```
</div>
</div>

### Reassign a volume to another child consistency group.
The following example reassigns a volume from a child consistency group
to another child consistency group with the same parent consistency group.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroup(uuid="6f51748a-0a7f-11ec-a449-005056bbcf9f")
    resource.consistency_groups = [
        {
            "name": "cg_child1",
            "volumes": [
                {"name": "child2_vol_1", "provisioning_options": {"action": "reassign"}}
            ],
        },
        {"name": "cg_child2"},
    ]
    resource.patch()

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


__all__ = ["ConsistencyGroup", "ConsistencyGroupSchema"]
__pdoc__ = {
    "ConsistencyGroupSchema.resource": False,
    "ConsistencyGroupSchema.opts": False,
}


class ConsistencyGroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroup object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the consistency_group."""

    tags = marshmallow_fields.List(marshmallow_fields.Str, data_key="_tags", allow_none=True)
    r""" Tags are an optional way to track the uses of a resource. Tag values must be formatted as key:value strings.

Example: ["team:csi","environment:test"]"""

    application = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_application.ConsistencyGroupApplicationSchema", data_key="application", unknown=EXCLUDE, allow_none=True)
    r""" The application field of the consistency_group."""

    clone = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_clone.ConsistencyGroupCloneSchema", data_key="clone", unknown=EXCLUDE, allow_none=True)
    r""" The clone field of the consistency_group."""

    consistency_groups = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_child.ConsistencyGroupChildSchema", unknown=EXCLUDE, allow_none=True), data_key="consistency_groups", allow_none=True)
    r""" A consistency group is a mutually exclusive aggregation of volumes or other consistency groups. A consistency group can only be associated with one direct parent consistency group."""

    luns = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_lun.ConsistencyGroupLunSchema", unknown=EXCLUDE, allow_none=True), data_key="luns", allow_none=True)
    r""" The LUNs array can be used to create or modify LUNs in a consistency group on a new or existing volume that is a member of the consistency group. LUNs are considered members of a consistency group if they are located on a volume that is a member of the consistency group."""

    map_to = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_map_to.ConsistencyGroupMapToSchema", data_key="map_to", unknown=EXCLUDE, allow_none=True)
    r""" Specifies the igroup or subsystem to map the LUNs or namespaces within the consistency group. This parameter can only be used if all the storage objects within the consistency groups are either LUNs or namespaces."""

    metric = marshmallow_fields.Nested("netapp_ontap.resources.consistency_group_metrics.ConsistencyGroupMetricsSchema", data_key="metric", unknown=EXCLUDE, allow_none=True)
    r""" Performance and capacity numbers, such as, IOPS, latency, throughput, used space, and available space."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the consistency group. The consistency group name must be unique within an SVM.<br/>"""

    namespaces = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_consistency_groups_namespaces.ConsistencyGroupConsistencyGroupsNamespacesSchema", unknown=EXCLUDE, allow_none=True), data_key="namespaces", allow_none=True)
    r""" An NVMe namespace is a collection of addressable logical blocks presented to hosts connected to the SVM using the NVMe over Fabrics protocol.
In ONTAP, an NVMe namespace is located within a volume. Optionally, it can be located within a qtree in a volume.<br/>
An NVMe namespace is created to a specified size using thin or thick provisioning as determined by the volume on which it is created. NVMe namespaces support being cloned. An NVMe namespace cannot be renamed, resized, or moved to a different volume. NVMe namespaces do not support the assignment of a QoS policy for performance management, but a QoS policy can be assigned to the volume containing the namespace. See the NVMe namespace object model to learn more about each of the properties supported by the NVMe namespace REST API.<br/>
An NVMe namespace must be mapped to an NVMe subsystem to grant access to the subsystem's hosts. Hosts can then access the NVMe namespace and perform I/O using the NVMe over Fabrics protocol."""

    parent_consistency_group = marshmallow_fields.Nested("netapp_ontap.resources.consistency_group.ConsistencyGroupSchema", data_key="parent_consistency_group", unknown=EXCLUDE, allow_none=True)
    r""" The parent_consistency_group field of the consistency_group."""

    provisioning_options = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_provisioning_options.ConsistencyGroupProvisioningOptionsSchema", data_key="provisioning_options", unknown=EXCLUDE, allow_none=True)
    r""" Options that are applied to the operation."""

    qos = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_qos.ConsistencyGroupQosSchema", data_key="qos", unknown=EXCLUDE, allow_none=True)
    r""" The qos field of the consistency_group."""

    replicated = marshmallow_fields.Boolean(
        data_key="replicated",
        allow_none=True,
    )
    r""" Indicates whether or not replication has been enabled on this consistency group."""

    replication_relationships = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_replication_relationships.ConsistencyGroupReplicationRelationshipsSchema", unknown=EXCLUDE, allow_none=True), data_key="replication_relationships", allow_none=True)
    r""" Indicates the SnapMirror relationship of this consistency group."""

    replication_source = marshmallow_fields.Boolean(
        data_key="replication_source",
        allow_none=True,
    )
    r""" Since support for this field is to be removed in the next release, use replication_relationships.is_source instead."""

    restore_to = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_consistency_groups_restore_to.ConsistencyGroupConsistencyGroupsRestoreToSchema", data_key="restore_to", unknown=EXCLUDE, allow_none=True)
    r""" Use to restore a consistency group to a previous snapshot"""

    snaplock = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_snaplock.ConsistencyGroupSnaplockSchema", data_key="snaplock", unknown=EXCLUDE, allow_none=True)
    r""" The snaplock field of the consistency_group."""

    snapshot_policy = marshmallow_fields.Nested("netapp_ontap.resources.snapshot_policy.SnapshotPolicySchema", data_key="snapshot_policy", unknown=EXCLUDE, allow_none=True)
    r""" The snapshot policy of the consistency group.<br/>
This is the dedicated consistency group snapshot policy, not an aggregation of the volume granular snapshot policy."""

    space = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_space.ConsistencyGroupSpaceSchema", data_key="space", unknown=EXCLUDE, allow_none=True)
    r""" The space field of the consistency_group."""

    statistics = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_statistics.ConsistencyGroupStatisticsSchema", data_key="statistics", unknown=EXCLUDE, allow_none=True)
    r""" These are raw performance and space numbers, such as, IOPS, latency, throughput, used space, and available space. These numbers are aggregated across all nodes in the cluster and increase with the uptime of the cluster."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the consistency_group."""

    tiering = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_tiering.ConsistencyGroupTieringSchema", data_key="tiering", unknown=EXCLUDE, allow_none=True)
    r""" The tiering field of the consistency_group."""

    unmap_from = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_unmap_from.ConsistencyGroupUnmapFromSchema", data_key="unmap_from", unknown=EXCLUDE, allow_none=True)
    r""" Specify the igroup or subsystem within the consistency group from which the LUNs or namespaces will be unmapped. This parameter can only be used if all the storage objects within the consistency groups are either LUNs or namespaces."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The unique identifier of the consistency group. The UUID is generated by ONTAP when the consistency group is created.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    vdisk_type = marshmallow_fields.Str(
        data_key="vdisk_type",
        validate=enum_validation(['luns', 'namespaces', 'mixed']),
        allow_none=True,
    )
    r""" Type of objects in the consistency group.

Valid choices:

* luns
* namespaces
* mixed"""

    volumes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_consistency_groups_volumes.ConsistencyGroupConsistencyGroupsVolumesSchema", unknown=EXCLUDE, allow_none=True), data_key="volumes", allow_none=True)
    r""" A consistency group is a mutually exclusive aggregation of volumes or other consistency groups. A volume can only be associated with one direct parent consistency group.<br/>

The total number of volumes across all child consistency groups contained in a consistency group is constrained by the same limit."""

    @property
    def resource(self):
        return ConsistencyGroup

    gettable_fields = [
        "links",
        "tags",
        "application",
        "clone",
        "consistency_groups",
        "luns",
        "metric",
        "name",
        "namespaces",
        "parent_consistency_group.links",
        "parent_consistency_group.name",
        "parent_consistency_group.uuid",
        "qos",
        "replicated",
        "replication_relationships",
        "replication_source",
        "snaplock",
        "snapshot_policy.links",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "space",
        "statistics",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "tiering",
        "uuid",
        "vdisk_type",
        "volumes",
    ]
    """links,tags,application,clone,consistency_groups,luns,metric,name,namespaces,parent_consistency_group.links,parent_consistency_group.name,parent_consistency_group.uuid,qos,replicated,replication_relationships,replication_source,snaplock,snapshot_policy.links,snapshot_policy.name,snapshot_policy.uuid,space,statistics,svm.links,svm.name,svm.uuid,tiering,uuid,vdisk_type,volumes,"""

    patchable_fields = [
        "tags",
        "application",
        "clone",
        "consistency_groups",
        "luns",
        "map_to",
        "namespaces",
        "provisioning_options",
        "qos",
        "restore_to",
        "snaplock",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "unmap_from",
        "vdisk_type",
        "volumes",
    ]
    """tags,application,clone,consistency_groups,luns,map_to,namespaces,provisioning_options,qos,restore_to,snaplock,snapshot_policy.name,snapshot_policy.uuid,unmap_from,vdisk_type,volumes,"""

    postable_fields = [
        "tags",
        "application",
        "clone",
        "consistency_groups",
        "luns",
        "name",
        "namespaces",
        "provisioning_options",
        "qos",
        "snaplock",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "svm.name",
        "svm.uuid",
        "tiering",
        "vdisk_type",
        "volumes",
    ]
    """tags,application,clone,consistency_groups,luns,name,namespaces,provisioning_options,qos,snaplock,snapshot_policy.name,snapshot_policy.uuid,svm.name,svm.uuid,tiering,vdisk_type,volumes,"""

class ConsistencyGroup(Resource):
    """Allows interaction with ConsistencyGroup objects on the host"""

    _schema = ConsistencyGroupSchema
    _path = "/api/application/consistency-groups"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieve details of a collection or a specific consistency group.
## Notes
When volume granular properties, such as, the storage SLC, Fabric Pool tiering are not the same for all the existing volumes of a consistency group, the corresponding property is not reported at consistency group granularity. It is only reported if all the volumes of the consistency group have the same value for that property.
<br>If this consistency group instance has 1 or more replication relationships, the "replicated" parameter is true.  If there are no associated replication relationships, it is false. This parameter is only included in the output for Single-CG and Parent-CG, not for Child-CG.
If this consistency group instance has 1 or more replication relationships, the "replication_relationships" parameter is included in the output for Single-CG and Parent-CG instances.  If there are no associated replication relationships, this parameter is not included in the output.
Note that this parameter is an array and as such it has as many elements as the number of replication relationships associated with this consistency group. Each element of the array describes properties of one replication relationship associated with this consistency group. The "uuid" parameter identifies a specific replication relationship and the "href" parameter is a link to the corresponding SnapMirror relationship. The "is_source" parameter is true if this consistency group is the source in that relationship, otherwise it is false.
## Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`DOC Requesting specific fields`](#docs-docs-Requesting-specific-fields) to learn more.
* `volumes`
* `luns`
* `namespaces`

### Learn more
* [`DOC /application/consistency-groups`](#docs-application-application_consistency-groups)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all ConsistencyGroup resources that match the provided query"""
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
        """Returns a list of RawResources that represent ConsistencyGroup resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["ConsistencyGroup"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a consistency group.
<br>Note that this operation will never delete storage elements. You can specify only elements that should be added to the consistency group regardless of existing storage objects.

## Related ONTAP commands
* `vserver consistency-group modify`

### Learn more
* [`DOC /application/consistency-groups`](#docs-application-application_consistency-groups)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["ConsistencyGroup"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["ConsistencyGroup"], NetAppResponse]:
        r"""Creates a consistency group with one or more consistency groups having:
* new SAN volumes,
* existing SAN, NVMe or NAS FlexVol volumes in a new or existing consistency group
## Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the group.
* `volumes`, `luns` or `namespaces`
## Naming Conventions
### Consistency groups
  * name or consistency_groups[].name, if specified
  * derived from volumes[0].name, if only one volume is specified, same as volume name
### Volume
  * volumes[].name, if specified
  * derived from volume prefix in luns[].name
  * derived from cg[].name, suffixed by "_#" where "#" is a system generated unique number
  * suffixed by "_#" where "#" is a system generated unique number, if provisioning_options.count is provided
### LUN
  * luns[].name, if specified
  * derived from volumes[].name, suffixed by "_#" where "#" is a system generated unique number
  * suffixed by "_#" where "#" is a system generated unique number, if provisioning_options.count is provided
### NVMe Namespace
  * namespaces[].name, if specified
  * derived from volumes[].name, suffixed by "_#" where "#" is a system generated unique number
  * suffixed by "_#" where "#" is a system generated unique number, if provisioning_options.count is provided
## Related ONTAP commands
There are no ONTAP commands for managing consistency group.

### Learn more
* [`DOC /application/consistency-groups`](#docs-application-application_consistency-groups)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["ConsistencyGroup"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a consistency group.
<br>Note this will not delete any associated volumes or LUNs. To delete those elements, use the appropriate object endpoint.
## Related ONTAP commands
There are no ONTAP commands for managing consistency groups.

### Learn more
* [`DOC /application/consistency-groups`](#docs-application-application_consistency-groups)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieve details of a collection or a specific consistency group.
## Notes
When volume granular properties, such as, the storage SLC, Fabric Pool tiering are not the same for all the existing volumes of a consistency group, the corresponding property is not reported at consistency group granularity. It is only reported if all the volumes of the consistency group have the same value for that property.
<br>If this consistency group instance has 1 or more replication relationships, the "replicated" parameter is true.  If there are no associated replication relationships, it is false. This parameter is only included in the output for Single-CG and Parent-CG, not for Child-CG.
If this consistency group instance has 1 or more replication relationships, the "replication_relationships" parameter is included in the output for Single-CG and Parent-CG instances.  If there are no associated replication relationships, this parameter is not included in the output.
Note that this parameter is an array and as such it has as many elements as the number of replication relationships associated with this consistency group. Each element of the array describes properties of one replication relationship associated with this consistency group. The "uuid" parameter identifies a specific replication relationship and the "href" parameter is a link to the corresponding SnapMirror relationship. The "is_source" parameter is true if this consistency group is the source in that relationship, otherwise it is false.
## Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`DOC Requesting specific fields`](#docs-docs-Requesting-specific-fields) to learn more.
* `volumes`
* `luns`
* `namespaces`

### Learn more
* [`DOC /application/consistency-groups`](#docs-application-application_consistency-groups)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a single consistency group.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`DOC Requesting specific fields`](#docs-docs-Requesting-specific-fields) to learn more.
* `volumes`
* `luns`
* `namespaces`
## Related ONTAP commands
There are no ONTAP commands for managing consistency groups.

### Learn more
* [`DOC /application/consistency-groups`](#docs-application-application_consistency-groups)"""
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
        r"""Creates a consistency group with one or more consistency groups having:
* new SAN volumes,
* existing SAN, NVMe or NAS FlexVol volumes in a new or existing consistency group
## Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the group.
* `volumes`, `luns` or `namespaces`
## Naming Conventions
### Consistency groups
  * name or consistency_groups[].name, if specified
  * derived from volumes[0].name, if only one volume is specified, same as volume name
### Volume
  * volumes[].name, if specified
  * derived from volume prefix in luns[].name
  * derived from cg[].name, suffixed by "_#" where "#" is a system generated unique number
  * suffixed by "_#" where "#" is a system generated unique number, if provisioning_options.count is provided
### LUN
  * luns[].name, if specified
  * derived from volumes[].name, suffixed by "_#" where "#" is a system generated unique number
  * suffixed by "_#" where "#" is a system generated unique number, if provisioning_options.count is provided
### NVMe Namespace
  * namespaces[].name, if specified
  * derived from volumes[].name, suffixed by "_#" where "#" is a system generated unique number
  * suffixed by "_#" where "#" is a system generated unique number, if provisioning_options.count is provided
## Related ONTAP commands
There are no ONTAP commands for managing consistency group.

### Learn more
* [`DOC /application/consistency-groups`](#docs-application-application_consistency-groups)"""
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
        r"""Updates a consistency group.
<br>Note that this operation will never delete storage elements. You can specify only elements that should be added to the consistency group regardless of existing storage objects.

## Related ONTAP commands
* `vserver consistency-group modify`

### Learn more
* [`DOC /application/consistency-groups`](#docs-application-application_consistency-groups)"""
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
        r"""Deletes a consistency group.
<br>Note this will not delete any associated volumes or LUNs. To delete those elements, use the appropriate object endpoint.
## Related ONTAP commands
There are no ONTAP commands for managing consistency groups.

### Learn more
* [`DOC /application/consistency-groups`](#docs-application-application_consistency-groups)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


