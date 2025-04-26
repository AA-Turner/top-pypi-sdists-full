r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Fibre Channel (FC) logins represent connections formed by FC initiators that have successfully logged in to ONTAP. This represents the FC login on which higher-level protocols such as Fibre Channel Protocol and NVMe over FC (NVMe/FC) rely.<br/>
The Fibre Channel logins REST API provides information about active FC logins.
## Examples
### Retrieving all FC logins
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FcLogin

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(FcLogin.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    FcLogin(
        {
            "interface": {
                "name": "lif1",
                "uuid": "01056403-1383-bc4b-786a-93e8ea35969d",
                "_links": {
                    "self": {
                        "href": "/api/network/fc/interfaces/01056403-1383-bc4b-786a-93e8ea35969d"
                    }
                },
            },
            "initiator": {"wwpn": "8b:21:2f:07:00:00:00:00"},
            "_links": {
                "self": {
                    "href": "/api/network/fc/logins/01056403-1383-bc4b-786a-93e8ea35969d/8b%3A21%3A2f%3A07%3A00%3A00%3A00%3A00"
                }
            },
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/056403da-83a7-4b13-bc78-6a93e8ea3596"
                    }
                },
                "uuid": "056403da-83a7-4b13-bc78-6a93e8ea3596",
            },
        }
    ),
    FcLogin(
        {
            "interface": {
                "name": "lif2",
                "uuid": "02056403-1383-bc4b-786a-93e8ea35969d",
                "_links": {
                    "self": {
                        "href": "/api/network/fc/interfaces/02056403-1383-bc4b-786a-93e8ea35969d"
                    }
                },
            },
            "initiator": {"wwpn": "8c:21:2f:07:00:00:00:00"},
            "_links": {
                "self": {
                    "href": "/api/network/fc/logins/02056403-1383-bc4b-786a-93e8ea35969d/8c%3A21%3A2f%3A07%3A00%3A00%3A00%3A00"
                }
            },
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/056403da-83a7-4b13-bc78-6a93e8ea3596"
                    }
                },
                "uuid": "056403da-83a7-4b13-bc78-6a93e8ea3596",
            },
        }
    ),
    FcLogin(
        {
            "interface": {
                "name": "lif3",
                "uuid": "03056403-1383-bc4b-786a-93e8ea35969d",
                "_links": {
                    "self": {
                        "href": "/api/network/fc/interfaces/00056403-1383-bc4b-786a-93e8ea35969d"
                    }
                },
            },
            "initiator": {"wwpn": "8a:21:2f:07:00:00:00:00"},
            "_links": {
                "self": {
                    "href": "/api/network/fc/logins/00056403-1383-bc4b-786a-93e8ea35969d/8a%3A21%3A2f%3A07%3A00%3A00%3A00%3A00"
                }
            },
            "svm": {
                "name": "svm2",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/156403da-83a7-4b13-bc78-6a93e8ea3596"
                    }
                },
                "uuid": "156403da-83a7-4b13-bc78-6a93e8ea3596",
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving all FC logins with data protocol _fcp_ in SVM _svm1_
The `svm.name` and `protocol` query parameters are used to perform the query.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FcLogin

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(FcLogin.get_collection(protocol="fcp", **{"svm.name": "svm1"})))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    FcLogin(
        {
            "interface": {
                "name": "lif2",
                "uuid": "01056403-1383-bc4b-786a-93e8ea35969d",
                "_links": {
                    "self": {
                        "href": "/api/network/fc/interfaces/01056403-1383-bc4b-786a-93e8ea35969d"
                    }
                },
            },
            "protocol": "fcp",
            "initiator": {"wwpn": "8b:21:2f:07:00:00:00:00"},
            "_links": {
                "self": {
                    "href": "/api/network/fc/logins/01056403-1383-bc4b-786a-93e8ea35969d/8b%3A21%3A2f%3A07%3A00%3A00%3A00%3A00"
                }
            },
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/056403da-83a7-4b13-bc78-6a93e8ea3596"
                    }
                },
                "uuid": "056403da-83a7-4b13-bc78-6a93e8ea3596",
            },
        }
    ),
    FcLogin(
        {
            "interface": {
                "name": "lif3",
                "uuid": "02056403-1383-bc4b-786a-93e8ea35969d",
                "_links": {
                    "self": {
                        "href": "/api/network/fc/interfaces/02056403-1383-bc4b-786a-93e8ea35969d"
                    }
                },
            },
            "protocol": "fcp",
            "initiator": {"wwpn": "8c:21:2f:07:00:00:00:00"},
            "_links": {
                "self": {
                    "href": "/api/network/fc/logins/02056403-1383-bc4b-786a-93e8ea35969d/8c%3A21%3A2f%3A07%3A00%3A00%3A00%3A00"
                }
            },
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/056403da-83a7-4b13-bc78-6a93e8ea3596"
                    }
                },
                "uuid": "056403da-83a7-4b13-bc78-6a93e8ea3596",
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving all FC logins for initiators belonging to _igroup1_ and returning all of their properties
The `igroups.name` query parameter is used to perform the query. The `fields` query parameter is used to return all of the properties.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FcLogin

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(FcLogin.get_collection(fields="*", **{"igroups.name": "igroup1"})))

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    FcLogin(
        {
            "interface": {
                "name": "lif2",
                "uuid": "01056403-1383-bc4b-786a-93e8ea35969d",
                "_links": {
                    "self": {
                        "href": "/api/network/fc/interfaces/01056403-1383-bc4b-786a-93e8ea35969d"
                    }
                },
                "wwpn": "8b:21:2f:07:00:00:00:00",
            },
            "protocol": "fcp",
            "initiator": {
                "comment": "Example information about this initiator",
                "wwpn": "8b:21:2f:07:00:00:00:00",
                "wwnn": "95:21:2f:07:00:00:00:00",
            },
            "igroups": [
                {
                    "name": "igroup1",
                    "uuid": "243bbb8a-46e9-4b2d-a508-a62dc93df9d1",
                    "_links": {
                        "self": {
                            "href": "/api/protocols/san/igroups/243bbb8a-46e9-4b2d-a508-a62dc93df9d1"
                        }
                    },
                }
            ],
            "_links": {
                "self": {
                    "href": "/api/network/fc/logins/01056403-1383-bc4b-786a-93e8ea35969d/8b%3A21%3A2f%3A07%3A00%3A00%3A00%3A00"
                }
            },
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/056403da-83a7-4b13-bc78-6a93e8ea3596"
                    }
                },
                "uuid": "056403da-83a7-4b13-bc78-6a93e8ea3596",
            },
        }
    )
]

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


__all__ = ["FcLogin", "FcLoginSchema"]
__pdoc__ = {
    "FcLoginSchema.resource": False,
    "FcLoginSchema.opts": False,
}


class FcLoginSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FcLogin object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.collection_links.CollectionLinksSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the fc_login."""

    igroups = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.igroup.IgroupSchema", unknown=EXCLUDE, allow_none=True), data_key="igroups", allow_none=True)
    r""" The initiator groups in which the initiator is a member."""

    initiator = marshmallow_fields.Nested("netapp_ontap.models.fc_login_initiator.FcLoginInitiatorSchema", data_key="initiator", unknown=EXCLUDE, allow_none=True)
    r""" Information about the logged in FC initiator."""

    interface = marshmallow_fields.Nested("netapp_ontap.resources.fc_interface.FcInterfaceSchema", data_key="interface", unknown=EXCLUDE, allow_none=True)
    r""" The interface field of the fc_login."""

    protocol = marshmallow_fields.Str(
        data_key="protocol",
        validate=enum_validation(['fc_nvme', 'fcp']),
        allow_none=True,
    )
    r""" The data protocol used to perform the login.


Valid choices:

* fc_nvme
* fcp"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the fc_login."""

    @property
    def resource(self):
        return FcLogin

    gettable_fields = [
        "links",
        "igroups.links",
        "igroups.name",
        "igroups.uuid",
        "initiator",
        "interface.links",
        "interface.name",
        "interface.uuid",
        "interface.wwpn",
        "protocol",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,igroups.links,igroups.name,igroups.uuid,initiator,interface.links,interface.name,interface.uuid,interface.wwpn,protocol,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class FcLogin(Resource):
    r""" A Fibre Channel (FC) login represents a connection formed by an FC initiator that has successfully logged in to ONTAP. This represents the FC login on which higher-level protocols such as Fibre Channel Protocol and NVMe over Fibre Channel (NVMe/FC) rely. """

    _schema = FcLoginSchema
    _path = "/api/network/fc/logins"
    _keys = ["interface.uuid", "initiator.wwpn"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves FC logins.
### Related ONTAP commands
* `vserver fcp initiator show`
### Learn more
* SAN: [`DOC /network/fc/logins`](#docs-SAN-network_fc_logins)
* NVMe: [`DOC /network/fc/logins`](#docs-NVMe-network_fc_logins)
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
        """Returns a count of all FcLogin resources that match the provided query"""
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
        """Returns a list of RawResources that represent FcLogin resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves FC logins.
### Related ONTAP commands
* `vserver fcp initiator show`
### Learn more
* SAN: [`DOC /network/fc/logins`](#docs-SAN-network_fc_logins)
* NVMe: [`DOC /network/fc/logins`](#docs-NVMe-network_fc_logins)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an FC login.
### Related ONTAP commands
* `vserver fcp initiator show`
### Learn more
* SAN: [`DOC /network/fc/logins`](#docs-SAN-network_fc_logins)
* NVMe: [`DOC /network/fc/logins`](#docs-NVMe-network_fc_logins)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





