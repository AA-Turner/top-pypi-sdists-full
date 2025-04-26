r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Quota reports provide the current file and space consumption for a user, group, or qtree in a FlexVol or a FlexGroup volume.
## Quota report APIs
The following APIs can be used to retrieve quota reports associated with a volume in ONTAP.

* GET       /api/storage/quota/reports
* GET       /api/storage/quota/reports/{volume_uuid}/{index}
## Examples
### Retrieving all the quota report records
This API is used to retrieve all the quota report records. <br/>
The following example shows how to retrieve quota report records for all FlexVol volumes and FlexGroup volumes.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QuotaReport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(QuotaReport.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    QuotaReport(
        {
            "volume": {
                "name": "fg",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/314a328f-502d-11e9-8771-005056a7f717"
                    }
                },
                "uuid": "314a328f-502d-11e9-8771-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/314a328f-502d-11e9-8771-005056a7f717/0"
                }
            },
            "index": 0,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "fg",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/314a328f-502d-11e9-8771-005056a7f717"
                    }
                },
                "uuid": "314a328f-502d-11e9-8771-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/314a328f-502d-11e9-8771-005056a7f717/1152921504606846976"
                }
            },
            "index": 1152921504606846976,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "fg",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/314a328f-502d-11e9-8771-005056a7f717"
                    }
                },
                "uuid": "314a328f-502d-11e9-8771-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/314a328f-502d-11e9-8771-005056a7f717/3458764513820540928"
                }
            },
            "index": 3458764513820540928,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "fg",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/314a328f-502d-11e9-8771-005056a7f717"
                    }
                },
                "uuid": "314a328f-502d-11e9-8771-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/314a328f-502d-11e9-8771-005056a7f717/4611686018427387904"
                }
            },
            "index": 4611686018427387904,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "fg",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/314a328f-502d-11e9-8771-005056a7f717"
                    }
                },
                "uuid": "314a328f-502d-11e9-8771-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/314a328f-502d-11e9-8771-005056a7f717/5764607523034234880"
                }
            },
            "index": 5764607523034234880,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
                    }
                },
                "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cb20da45-4f6b-11e9-9a71-005056a7f717/0"
                }
            },
            "index": 0,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
                    }
                },
                "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cb20da45-4f6b-11e9-9a71-005056a7f717/281474976710656"
                }
            },
            "index": 281474976710656,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
                    }
                },
                "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cb20da45-4f6b-11e9-9a71-005056a7f717/1152921504606846976"
                }
            },
            "index": 1152921504606846976,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
                    }
                },
                "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cb20da45-4f6b-11e9-9a71-005056a7f717/1153202979583557632"
                }
            },
            "index": 1153202979583557632,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
                    }
                },
                "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cb20da45-4f6b-11e9-9a71-005056a7f717/2305843013508661248"
                }
            },
            "index": 2305843013508661248,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
                    }
                },
                "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cb20da45-4f6b-11e9-9a71-005056a7f717/3458764513820540928"
                }
            },
            "index": 3458764513820540928,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
                    }
                },
                "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cb20da45-4f6b-11e9-9a71-005056a7f717/3459045988797251584"
                }
            },
            "index": 3459045988797251584,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
                    }
                },
                "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cb20da45-4f6b-11e9-9a71-005056a7f717/4611686018427387904"
                }
            },
            "index": 4611686018427387904,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
                    }
                },
                "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cb20da45-4f6b-11e9-9a71-005056a7f717/4611967493404098560"
                }
            },
            "index": 4611967493404098560,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
                    }
                },
                "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cb20da45-4f6b-11e9-9a71-005056a7f717/5764607523034234880"
                }
            },
            "index": 5764607523034234880,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific quota report record
This API is used to retrieve a specific quota report record. <br/>
The following example shows how to retrieve a single quota report user record.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QuotaReport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = QuotaReport(
        index=281474976710656, **{"volume.uuid": "cf480c37-2a6b-11e9-8513-005056a7657c"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
QuotaReport(
    {
        "users": [{"name": "fred", "id": "300008"}],
        "files": {
            "hard_limit": 40,
            "soft_limit": 30,
            "used": {"hard_limit_percent": 28, "soft_limit_percent": 37, "total": 11},
        },
        "volume": {
            "name": "fv",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/cf480c37-2a6b-11e9-8513-005056a7657c"
                }
            },
            "uuid": "cf480c37-2a6b-11e9-8513-005056a7657c",
        },
        "space": {
            "hard_limit": 41943040,
            "soft_limit": 31457280,
            "used": {
                "hard_limit_percent": 25,
                "soft_limit_percent": 34,
                "total": 10567680,
            },
        },
        "qtree": {
            "name": "qt1",
            "_links": {
                "self": {
                    "href": "/api/storage/qtrees/cf480c37-2a6b-11e9-8513-005056a7657c/1"
                }
            },
            "id": 1,
        },
        "_links": {
            "self": {
                "href": "/api/storage/quota/reports/cf480c37-2a6b-11e9-8513-005056a7657c/281474976710656"
            }
        },
        "index": 281474976710656,
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/5093e722-248e-11e9-96ee-005056a7657c"}
            },
            "uuid": "5093e722-248e-11e9-96ee-005056a7657c",
        },
        "type": "user",
    }
)

```
</div>
</div>

---
### Retrieving a single quota report multi-user record
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QuotaReport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = QuotaReport(
        index=281474976710656, **{"volume.uuid": "cf480c37-2a6b-11e9-8513-005056a7657c"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
QuotaReport(
    {
        "users": [
            {"name": "fred", "id": "300008"},
            {"name": "john", "id": "300009"},
            {"name": "smith", "id": "300010"},
        ],
        "files": {
            "hard_limit": 40,
            "soft_limit": 30,
            "used": {"hard_limit_percent": 28, "soft_limit_percent": 37, "total": 11},
        },
        "volume": {
            "name": "fv",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/cf480c37-2a6b-11e9-8513-005056a7657c"
                }
            },
            "uuid": "cf480c37-2a6b-11e9-8513-005056a7657c",
        },
        "space": {
            "hard_limit": 41943040,
            "soft_limit": 31457280,
            "used": {
                "hard_limit_percent": 25,
                "soft_limit_percent": 34,
                "total": 10567680,
            },
        },
        "qtree": {
            "name": "qt1",
            "_links": {
                "self": {
                    "href": "/api/storage/qtrees/cf480c37-2a6b-11e9-8513-005056a7657c/1"
                }
            },
            "id": 1,
        },
        "_links": {
            "self": {
                "href": "/api/storage/quota/reports/cf480c37-2a6b-11e9-8513-005056a7657c/1153484454560268288"
            }
        },
        "index": 1153484454560268288,
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/5093e722-248e-11e9-96ee-005056a7657c"}
            },
            "uuid": "5093e722-248e-11e9-96ee-005056a7657c",
        },
        "type": "user",
    }
)

```
</div>
</div>

---
### Retrieving a single quota report group record
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QuotaReport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = QuotaReport(
        index=3459045988797251584,
        **{"volume.uuid": "cf480c37-2a6b-11e9-8513-005056a7657c"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
QuotaReport(
    {
        "group": {"name": "test_group", "id": "500009"},
        "files": {
            "hard_limit": 40,
            "soft_limit": 30,
            "used": {"hard_limit_percent": 28, "soft_limit_percent": 37, "total": 11},
        },
        "volume": {
            "name": "fv",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/cf480c37-2a6b-11e9-8513-005056a7657c"
                }
            },
            "uuid": "cf480c37-2a6b-11e9-8513-005056a7657c",
        },
        "space": {
            "hard_limit": 41943040,
            "soft_limit": 31457280,
            "used": {
                "hard_limit_percent": 25,
                "soft_limit_percent": 34,
                "total": 10567680,
            },
        },
        "qtree": {
            "name": "qt1",
            "_links": {
                "self": {
                    "href": "/api/storage/qtrees/cf480c37-2a6b-11e9-8513-005056a7657c/1"
                }
            },
            "id": 1,
        },
        "_links": {
            "self": {
                "href": "/api/storage/quota/reports/cf480c37-2a6b-11e9-8513-005056a7657c/3459045988797251584"
            }
        },
        "index": 3459045988797251584,
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/5093e722-248e-11e9-96ee-005056a7657c"}
            },
            "uuid": "5093e722-248e-11e9-96ee-005056a7657c",
        },
        "type": "group",
    }
)

```
</div>
</div>

---
### Retrieving a single quota report tree record
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QuotaReport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = QuotaReport(
        index=4612248968380809216,
        **{"volume.uuid": "cf480c37-2a6b-11e9-8513-005056a7657c"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
QuotaReport(
    {
        "files": {
            "hard_limit": 40,
            "soft_limit": 30,
            "used": {"hard_limit_percent": 28, "soft_limit_percent": 37, "total": 11},
        },
        "volume": {
            "name": "fv",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/cf480c37-2a6b-11e9-8513-005056a7657c"
                }
            },
            "uuid": "cf480c37-2a6b-11e9-8513-005056a7657c",
        },
        "space": {
            "hard_limit": 41943040,
            "soft_limit": 31457280,
            "used": {
                "hard_limit_percent": 25,
                "soft_limit_percent": 34,
                "total": 10567680,
            },
        },
        "qtree": {
            "name": "qt1",
            "_links": {
                "self": {
                    "href": "/api/storage/qtrees/cf480c37-2a6b-11e9-8513-005056a7657c/1"
                }
            },
            "id": 1,
        },
        "_links": {
            "self": {
                "href": "/api/storage/quota/reports/cf480c37-2a6b-11e9-8513-005056a7657c/4612248968380809216"
            }
        },
        "index": 4612248968380809216,
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/5093e722-248e-11e9-96ee-005056a7657c"}
            },
            "uuid": "5093e722-248e-11e9-96ee-005056a7657c",
        },
        "type": "tree",
    }
)

```
</div>
</div>

---
### Retrieving only records enforced by non-default rules
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QuotaReport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(QuotaReport.get_collection(show_default_records=False)))

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
[
    QuotaReport(
        {
            "files": {
                "hard_limit": 40,
                "soft_limit": 30,
                "used": {
                    "hard_limit_percent": 28,
                    "soft_limit_percent": 37,
                    "total": 11,
                },
            },
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cf480c37-2a6b-11e9-8513-005056a7657c"
                    }
                },
                "uuid": "cf480c37-2a6b-11e9-8513-005056a7657c",
            },
            "space": {
                "hard_limit": 41943040,
                "soft_limit": 31457280,
                "used": {
                    "hard_limit_percent": 25,
                    "soft_limit_percent": 34,
                    "total": 10567680,
                },
            },
            "qtree": {
                "name": "qt1",
                "_links": {
                    "self": {
                        "href": "/api/storage/qtrees/cf480c37-2a6b-11e9-8513-005056a7657c/1"
                    }
                },
                "id": 1,
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cf480c37-2a6b-11e9-8513-005056a7657c/4612248968380809216"
                }
            },
            "index": 4612248968380809216,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/5093e722-248e-11e9-96ee-005056a7657c"
                    }
                },
                "uuid": "5093e722-248e-11e9-96ee-005056a7657c",
            },
            "type": "tree",
        }
    ),
    QuotaReport(
        {
            "users": [
                {"name": "fred", "id": "300008"},
                {"name": "john", "id": "300009"},
                {"name": "smith", "id": "300010"},
            ],
            "files": {
                "hard_limit": 40,
                "soft_limit": 30,
                "used": {
                    "hard_limit_percent": 28,
                    "soft_limit_percent": 37,
                    "total": 11,
                },
            },
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cf480c37-2a6b-11e9-8513-005056a7657c"
                    }
                },
                "uuid": "cf480c37-2a6b-11e9-8513-005056a7657c",
            },
            "space": {
                "hard_limit": 41943040,
                "soft_limit": 31457280,
                "used": {
                    "hard_limit_percent": 25,
                    "soft_limit_percent": 34,
                    "total": 10567680,
                },
            },
            "qtree": {
                "name": "qt1",
                "_links": {
                    "self": {
                        "href": "/api/storage/qtrees/cf480c37-2a6b-11e9-8513-005056a7657c/1"
                    }
                },
                "id": 1,
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cf480c37-2a6b-11e9-8513-005056a7657c/1153484454560268288"
                }
            },
            "index": 1153484454560268288,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/5093e722-248e-11e9-96ee-005056a7657c"
                    }
                },
                "uuid": "5093e722-248e-11e9-96ee-005056a7657c",
            },
            "type": "user",
        }
    ),
]

```
</div>
</div>

---
### Retrieving quota report records with query parameters
The following example shows how to retrieve tree type quota report records.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QuotaReport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(QuotaReport.get_collection(type="tree")))

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
[
    QuotaReport(
        {
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/8812b000-6e1e-11ea-9bad-00505682cd5c"
                    }
                },
                "uuid": "8812b000-6e1e-11ea-9bad-00505682cd5c",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/8812b000-6e1e-11ea-9bad-00505682cd5c/2305843013508661248"
                }
            },
            "index": 2305843013508661248,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/903e54ee-6ccf-11ea-bc35-005056823577"
                    }
                },
                "uuid": "903e54ee-6ccf-11ea-bc35-005056823577",
            },
            "type": "tree",
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "fg",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/a5ceebd2-6ccf-11ea-bc35-005056823577"
                    }
                },
                "uuid": "a5ceebd2-6ccf-11ea-bc35-005056823577",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/a5ceebd2-6ccf-11ea-bc35-005056823577/2305843013508661248"
                }
            },
            "index": 2305843013508661248,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/903e54ee-6ccf-11ea-bc35-005056823577"
                    }
                },
                "uuid": "903e54ee-6ccf-11ea-bc35-005056823577",
            },
            "type": "tree",
        }
    ),
]

```
</div>
</div>

---
### Retrieving all the quota reports of a specific volume and the files fields
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QuotaReport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(QuotaReport.get_collection(fields="files", **{"volume.name": "fv"})))

```
<div class="try_it_out">
<input id="example7_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example7_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example7_result" class="try_it_out_content">
```
[
    QuotaReport(
        {
            "files": {
                "hard_limit": 30,
                "soft_limit": 20,
                "used": {"hard_limit_percent": 0, "soft_limit_percent": 0, "total": 0},
            },
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/8812b000-6e1e-11ea-9bad-00505682cd5c"
                    }
                },
                "uuid": "8812b000-6e1e-11ea-9bad-00505682cd5c",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/8812b000-6e1e-11ea-9bad-00505682cd5c/410328290557952"
                }
            },
            "index": 410328290557952,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/903e54ee-6ccf-11ea-bc35-005056823577"
                    }
                },
                "uuid": "903e54ee-6ccf-11ea-bc35-005056823577",
            },
        }
    ),
    QuotaReport(
        {
            "files": {
                "hard_limit": 400,
                "soft_limit": 200,
                "used": {"hard_limit_percent": 1, "soft_limit_percent": 2, "total": 4},
            },
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/8812b000-6e1e-11ea-9bad-00505682cd5c"
                    }
                },
                "uuid": "8812b000-6e1e-11ea-9bad-00505682cd5c",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/8812b000-6e1e-11ea-9bad-00505682cd5c/2305843013508661248"
                }
            },
            "index": 2305843013508661248,
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/903e54ee-6ccf-11ea-bc35-005056823577"
                    }
                },
                "uuid": "903e54ee-6ccf-11ea-bc35-005056823577",
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving quota reports for all volumes with the property files.hard_limit greater than 5 or null (unlimited) for qtree qt1
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QuotaReport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            QuotaReport.get_collection(
                **{"qtree.name": "qt1", "files.hard_limit": ">5|null"}
            )
        )
    )

```
<div class="try_it_out">
<input id="example8_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example8_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example8_result" class="try_it_out_content">
```
[
    QuotaReport(
        {
            "volume": {
                "name": "srcVolume",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/0c9cff59-da3c-11ed-930f-005056ac3135"
                    }
                },
                "uuid": "0c9cff59-da3c-11ed-930f-005056ac3135",
            },
            "qtree": {"name": "qt1"},
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/0c9cff59-da3c-11ed-930f-005056ac3135/281474976710656"
                }
            },
            "index": 281474976710656,
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/842981cb-c985-11ed-a399-005056ac442b"
                    }
                },
                "uuid": "842981cb-c985-11ed-a399-005056ac442b",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "srcVolume",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/0c9cff59-da3c-11ed-930f-005056ac3135"
                    }
                },
                "uuid": "0c9cff59-da3c-11ed-930f-005056ac3135",
            },
            "qtree": {"name": "qt1"},
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/0c9cff59-da3c-11ed-930f-005056ac3135/1153202979583557632"
                }
            },
            "index": 1153202979583557632,
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/842981cb-c985-11ed-a399-005056ac442b"
                    }
                },
                "uuid": "842981cb-c985-11ed-a399-005056ac442b",
            },
        }
    ),
    QuotaReport(
        {
            "files": {"hard_limit": 15},
            "volume": {
                "name": "srcVolume",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/0c9cff59-da3c-11ed-930f-005056ac3135"
                    }
                },
                "uuid": "0c9cff59-da3c-11ed-930f-005056ac3135",
            },
            "qtree": {"name": "qt1"},
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/0c9cff59-da3c-11ed-930f-005056ac3135/2305843013508661248"
                }
            },
            "index": 2305843013508661248,
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/842981cb-c985-11ed-a399-005056ac442b"
                    }
                },
                "uuid": "842981cb-c985-11ed-a399-005056ac442b",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "srcVolume",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/0c9cff59-da3c-11ed-930f-005056ac3135"
                    }
                },
                "uuid": "0c9cff59-da3c-11ed-930f-005056ac3135",
            },
            "qtree": {"name": "qt1"},
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/0c9cff59-da3c-11ed-930f-005056ac3135/3459045988797251584"
                }
            },
            "index": 3459045988797251584,
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/842981cb-c985-11ed-a399-005056ac442b"
                    }
                },
                "uuid": "842981cb-c985-11ed-a399-005056ac442b",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "srcVolume",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/0c9cff59-da3c-11ed-930f-005056ac3135"
                    }
                },
                "uuid": "0c9cff59-da3c-11ed-930f-005056ac3135",
            },
            "qtree": {"name": "qt1"},
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/0c9cff59-da3c-11ed-930f-005056ac3135/4611967493404098560"
                }
            },
            "index": 4611967493404098560,
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/842981cb-c985-11ed-a399-005056ac442b"
                    }
                },
                "uuid": "842981cb-c985-11ed-a399-005056ac442b",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "srcVolume2",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/3a2a8d78-ded3-11ed-9806-005056ac3135"
                    }
                },
                "uuid": "3a2a8d78-ded3-11ed-9806-005056ac3135",
            },
            "qtree": {"name": "qt1"},
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/3a2a8d78-ded3-11ed-9806-005056ac3135/281474976710656"
                }
            },
            "index": 281474976710656,
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/842981cb-c985-11ed-a399-005056ac442b"
                    }
                },
                "uuid": "842981cb-c985-11ed-a399-005056ac442b",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "srcVolume2",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/3a2a8d78-ded3-11ed-9806-005056ac3135"
                    }
                },
                "uuid": "3a2a8d78-ded3-11ed-9806-005056ac3135",
            },
            "qtree": {"name": "qt1"},
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/3a2a8d78-ded3-11ed-9806-005056ac3135/1153202979583557632"
                }
            },
            "index": 1153202979583557632,
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/842981cb-c985-11ed-a399-005056ac442b"
                    }
                },
                "uuid": "842981cb-c985-11ed-a399-005056ac442b",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "srcVolume2",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/3a2a8d78-ded3-11ed-9806-005056ac3135"
                    }
                },
                "uuid": "3a2a8d78-ded3-11ed-9806-005056ac3135",
            },
            "qtree": {"name": "qt1"},
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/3a2a8d78-ded3-11ed-9806-005056ac3135/3459045988797251584"
                }
            },
            "index": 3459045988797251584,
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/842981cb-c985-11ed-a399-005056ac442b"
                    }
                },
                "uuid": "842981cb-c985-11ed-a399-005056ac442b",
            },
        }
    ),
    QuotaReport(
        {
            "volume": {
                "name": "srcVolume2",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/3a2a8d78-ded3-11ed-9806-005056ac3135"
                    }
                },
                "uuid": "3a2a8d78-ded3-11ed-9806-005056ac3135",
            },
            "qtree": {"name": "qt1"},
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/3a2a8d78-ded3-11ed-9806-005056ac3135/4611967493404098560"
                }
            },
            "index": 4611967493404098560,
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/842981cb-c985-11ed-a399-005056ac442b"
                    }
                },
                "uuid": "842981cb-c985-11ed-a399-005056ac442b",
            },
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


__all__ = ["QuotaReport", "QuotaReportSchema"]
__pdoc__ = {
    "QuotaReportSchema.resource": False,
    "QuotaReportSchema.opts": False,
}


class QuotaReportSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the QuotaReport object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the quota_report."""

    files = marshmallow_fields.Nested("netapp_ontap.models.quota_report_files.QuotaReportFilesSchema", data_key="files", unknown=EXCLUDE, allow_none=True)
    r""" The files field of the quota_report."""

    group = marshmallow_fields.Nested("netapp_ontap.models.quota_report_group.QuotaReportGroupSchema", data_key="group", unknown=EXCLUDE, allow_none=True)
    r""" This parameter specifies the target group associated with the given quota report record. This parameter is available for group quota records and is not available for user or tree quota records. The target group is identified by a UNIX group name and UNIX group identifier."""

    index = Size(
        data_key="index",
        allow_none=True,
    )
    r""" Index that identifies a unique quota record. Valid in URL."""

    qtree = marshmallow_fields.Nested("netapp_ontap.models.quota_report_qtree.QuotaReportQtreeSchema", data_key="qtree", unknown=EXCLUDE, allow_none=True)
    r""" The qtree field of the quota_report."""

    space = marshmallow_fields.Nested("netapp_ontap.models.quota_report_space.QuotaReportSpaceSchema", data_key="space", unknown=EXCLUDE, allow_none=True)
    r""" The space field of the quota_report."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the quota_report."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['tree', 'user', 'group']),
        allow_none=True,
    )
    r""" Quota type associated with the quota record.

Valid choices:

* tree
* user
* group"""

    users = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.quota_report_users.QuotaReportUsersSchema", unknown=EXCLUDE, allow_none=True), data_key="users", allow_none=True)
    r""" This parameter specifies the target user or users associated with the given quota report record. This parameter is available for user quota records and is not available for group or tree quota records. The target user or users are identified by a user name and user identifier. The user name can be a UNIX user name or a Windows user name, and the identifier can be a UNIX user identifier or a Windows security identifier."""

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE, allow_none=True)
    r""" The volume field of the quota_report."""

    @property
    def resource(self):
        return QuotaReport

    gettable_fields = [
        "links",
        "files",
        "group",
        "index",
        "qtree.links",
        "qtree.id",
        "qtree.name",
        "space",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "type",
        "users",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """links,files,group,index,qtree.links,qtree.id,qtree.name,space,svm.links,svm.name,svm.uuid,type,users,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "files",
        "group",
        "space",
        "svm.name",
        "svm.uuid",
        "users",
        "volume.name",
        "volume.uuid",
    ]
    """files,group,space,svm.name,svm.uuid,users,volume.name,volume.uuid,"""

    postable_fields = [
        "files",
        "group",
        "space",
        "svm.name",
        "svm.uuid",
        "users",
        "volume.name",
        "volume.uuid",
    ]
    """files,group,space,svm.name,svm.uuid,users,volume.name,volume.uuid,"""

class QuotaReport(Resource):
    """Allows interaction with QuotaReport objects on the host"""

    _schema = QuotaReportSchema
    _path = "/api/storage/quota/reports"
    _keys = ["volume.uuid", "index"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the quota report records for all FlexVol volumes and FlexGroup volumes.
### Related ONTAP commands
* `quota report`

### Learn more
* [`DOC /storage/quota/reports`](#docs-storage-storage_quota_reports)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all QuotaReport resources that match the provided query"""
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
        """Returns a list of RawResources that represent QuotaReport resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the quota report records for all FlexVol volumes and FlexGroup volumes.
### Related ONTAP commands
* `quota report`

### Learn more
* [`DOC /storage/quota/reports`](#docs-storage-storage_quota_reports)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific quota report record.
### Related ONTAP commands
* `quota report`

### Learn more
* [`DOC /storage/quota/reports`](#docs-storage-storage_quota_reports)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





