r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Non-Volatile Memory Express (NVMe) subsystem controllers represent dynamic connections between hosts and a storage solution.<br/>
The NVMe subsystem controllers REST API provides information about connected hosts.
## Examples
### Retrieving the NVMe subsystem controllers for the entire system
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeSubsystemController

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(NvmeSubsystemController.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    NvmeSubsystemController(
        {
            "subsystem": {
                "name": "symmcon_symmcon_fcnvme_vserver_0_subsystem_0",
                "uuid": "14875240-2594-11e9-abde-00a098984313",
                "_links": {
                    "self": {
                        "href": "/api/protocols/nvme/subsystems/14875240-2594-11e9-abde-00a098984313"
                    }
                },
            },
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/subsystem-controllers/14875240-2594-11e9-abde-00a098984313/0040h"
                }
            },
            "id": "0040h",
            "svm": {
                "name": "symmcon_fcnvme_vserver_0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/f0f5b928-2593-11e9-94c4-00a0989a1c8e"
                    }
                },
                "uuid": "f0f5b928-2593-11e9-94c4-00a0989a1c8e",
            },
        }
    ),
    NvmeSubsystemController(
        {
            "subsystem": {
                "name": "symmcon_symmcon_fcnvme_vserver_0_subsystem_0",
                "uuid": "14875240-2594-11e9-abde-00a098984313",
                "_links": {
                    "self": {
                        "href": "/api/protocols/nvme/subsystems/14875240-2594-11e9-abde-00a098984313"
                    }
                },
            },
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/subsystem-controllers/14875240-2594-11e9-abde-00a098984313/0041h"
                }
            },
            "id": "0041h",
            "svm": {
                "name": "symmcon_fcnvme_vserver_0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/f0f5b928-2593-11e9-94c4-00a0989a1c8e"
                    }
                },
                "uuid": "f0f5b928-2593-11e9-94c4-00a0989a1c8e",
            },
        }
    ),
    NvmeSubsystemController(
        {
            "subsystem": {
                "name": "symmcon_symmcon_fcnvme_vserver_0_subsystem_1",
                "uuid": "1489d0d5-2594-11e9-94c4-00a0989a1c8e",
                "_links": {
                    "self": {
                        "href": "/api/protocols/nvme/subsystems/1489d0d5-2594-11e9-94c4-00a0989a1c8e"
                    }
                },
            },
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/subsystem-controllers/1489d0d5-2594-11e9-94c4-00a0989a1c8e/0040h"
                }
            },
            "id": "0040h",
            "svm": {
                "name": "symmcon_fcnvme_vserver_0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/f0f5b928-2593-11e9-94c4-00a0989a1c8e"
                    }
                },
                "uuid": "f0f5b928-2593-11e9-94c4-00a0989a1c8e",
            },
        }
    ),
    NvmeSubsystemController(
        {
            "subsystem": {
                "name": "symmcon_symmcon_fcnvme_vserver_0_subsystem_1",
                "uuid": "1489d0d5-2594-11e9-94c4-00a0989a1c8e",
                "_links": {
                    "self": {
                        "href": "/api/protocols/nvme/subsystems/1489d0d5-2594-11e9-94c4-00a0989a1c8e"
                    }
                },
            },
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/subsystem-controllers/1489d0d5-2594-11e9-94c4-00a0989a1c8e/0041h"
                }
            },
            "id": "0041h",
            "svm": {
                "name": "symmcon_fcnvme_vserver_0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/f0f5b928-2593-11e9-94c4-00a0989a1c8e"
                    }
                },
                "uuid": "f0f5b928-2593-11e9-94c4-00a0989a1c8e",
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving the NVMe subsystem controllers for a specific subsystem
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeSubsystemController

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            NvmeSubsystemController.get_collection(
                **{"subsystem.uuid": "14875240-2594-11e9-abde-00a098984313"}
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
    NvmeSubsystemController(
        {
            "subsystem": {
                "name": "symmcon_symmcon_fcnvme_vserver_0_subsystem_0",
                "uuid": "14875240-2594-11e9-abde-00a098984313",
                "_links": {
                    "self": {
                        "href": "/api/protocols/nvme/subsystems/14875240-2594-11e9-abde-00a098984313"
                    }
                },
            },
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/subsystem-controllers/14875240-2594-11e9-abde-00a098984313/0040h"
                }
            },
            "id": "0040h",
            "svm": {
                "name": "symmcon_fcnvme_vserver_0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/f0f5b928-2593-11e9-94c4-00a0989a1c8e"
                    }
                },
                "uuid": "f0f5b928-2593-11e9-94c4-00a0989a1c8e",
            },
        }
    ),
    NvmeSubsystemController(
        {
            "subsystem": {
                "name": "symmcon_symmcon_fcnvme_vserver_0_subsystem_0",
                "uuid": "14875240-2594-11e9-abde-00a098984313",
                "_links": {
                    "self": {
                        "href": "/api/protocols/nvme/subsystems/14875240-2594-11e9-abde-00a098984313"
                    }
                },
            },
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/subsystem-controllers/14875240-2594-11e9-abde-00a098984313/0041h"
                }
            },
            "id": "0041h",
            "svm": {
                "name": "symmcon_fcnvme_vserver_0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/f0f5b928-2593-11e9-94c4-00a0989a1c8e"
                    }
                },
                "uuid": "f0f5b928-2593-11e9-94c4-00a0989a1c8e",
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific NVMe subsystem controller
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeSubsystemController

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NvmeSubsystemController(
        id="0040h", **{"subsystem.uuid": "14875240-2594-11e9-abde-00a098984313"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
NvmeSubsystemController(
    {
        "subsystem": {
            "name": "symmcon_symmcon_fcnvme_vserver_0_subsystem_0",
            "uuid": "14875240-2594-11e9-abde-00a098984313",
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/subsystems/14875240-2594-11e9-abde-00a098984313"
                }
            },
        },
        "interface": {
            "name": "symmcon_lif_fcnvme_symmcon_fcnvme_vserver_0_3a_0",
            "transport_address": "nn-0x200400a0989a1c8d:pn-0x200500a0989a1c8d",
            "uuid": "fa1c5941-2593-11e9-94c4-00a0989a1c8e",
        },
        "keep_alive_timeout": 4000,
        "host": {
            "nqn": "nqn.2014-08.org.nvmexpress:uuid:c2846cb1-89d2-4020-a3b0-71ce907b4eef",
            "id": "b8546ca6097349e5b1558dc154fc073b",
            "transport_address": "nn-0x20000090fae00806:pn-0x10000090fae00806",
        },
        "tls": {
            "cipher": "tls_aes_128_gcm_sha256",
            "psk_identity": "NVMe1R01 nqn.2014-08.org.nvmexpress:uuid:c2846cb1-89d2-4020-a3b0-71ce907b4eef nqn.1992-08.com.netapp:sn.ca3cae02070811ef9a53005056bb9001:subsystem.ss1 c9X3RurQxGiGa76Tpk2tirifrUhHmVp035MOrtHXnAU=",
            "key_type": "configured",
        },
        "node": {
            "name": "ssan-8040-94a",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/ebf66f05-2590-11e9-abde-00a098984313"
                }
            },
            "uuid": "ebf66f05-2590-11e9-abde-00a098984313",
        },
        "digest": {"data": False, "header": True},
        "_links": {
            "self": {
                "href": "/api/protocols/nvme/subsystem-controllers/14875240-2594-11e9-abde-00a098984313/0040h"
            }
        },
        "id": "0040h",
        "svm": {
            "name": "symmcon_fcnvme_vserver_0",
            "_links": {
                "self": {"href": "/api/svm/svms/f0f5b928-2593-11e9-94c4-00a0989a1c8e"}
            },
            "uuid": "f0f5b928-2593-11e9-94c4-00a0989a1c8e",
        },
        "admin_queue": {"depth": 32},
        "io_queue": {"depth": [32, 32, 32, 32], "count": 4},
        "dh_hmac_chap": {"mode": "none"},
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


__all__ = ["NvmeSubsystemController", "NvmeSubsystemControllerSchema"]
__pdoc__ = {
    "NvmeSubsystemControllerSchema.resource": False,
    "NvmeSubsystemControllerSchema.opts": False,
}


class NvmeSubsystemControllerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeSubsystemController object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the nvme_subsystem_controller."""

    admin_queue = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_controller_admin_queue.NvmeSubsystemControllerAdminQueueSchema", data_key="admin_queue", unknown=EXCLUDE, allow_none=True)
    r""" The admin_queue field of the nvme_subsystem_controller."""

    dh_hmac_chap = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_controller_dh_hmac_chap.NvmeSubsystemControllerDhHmacChapSchema", data_key="dh_hmac_chap", unknown=EXCLUDE, allow_none=True)
    r""" A container for properties of the NVMe in-band authentication DH-HMAC-CHAP protocol used by the the host connection to the controller."""

    digest = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_controller_digest.NvmeSubsystemControllerDigestSchema", data_key="digest", unknown=EXCLUDE, allow_none=True)
    r""" Digests are properties of NVMe controllers created over the NVMe/TCP transport protocol. The usage of digests is negotiated between the host and the controller during connection setup. ONTAP enables digests only if the host requests them. The header digest is the crc32 checksum of the header portion of the NVMe/TCP PDU. The data digest is the crc32 checksum of the data portion of the NVMe/TCP PDU.<br/>
If a digest is enabled, upon receiving an NVMe/TCP PDU, ONTAP calculates the crc32 checksum of the associated portion of the PDU and compares it with the digest value present in the transmitted PDU. If there is a mismatch, ONTAP returns an error and destroys the controller."""

    host = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_controller_host.NvmeSubsystemControllerHostSchema", data_key="host", unknown=EXCLUDE, allow_none=True)
    r""" Properties of the connected host."""

    id = marshmallow_fields.Str(
        data_key="id",
        allow_none=True,
    )
    r""" The identifier of the subsystem controller. This field consists of 4 zero-filled hexadecimal digits followed by an 'h'.


Example: 0040h"""

    interface = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_controller_interface.NvmeSubsystemControllerInterfaceSchema", data_key="interface", unknown=EXCLUDE, allow_none=True)
    r""" The logical interface through which the host is connected."""

    io_queue = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_controller_io_queue.NvmeSubsystemControllerIoQueueSchema", data_key="io_queue", unknown=EXCLUDE, allow_none=True)
    r""" Properties of the I/O queues available to the controller."""

    keep_alive_timeout = Size(
        data_key="keep_alive_timeout",
        allow_none=True,
    )
    r""" The keep-alive timeout value for the controller and all of its host connections, in milliseconds. <br/>
If the NVMe controller does not receive a keep-alive request or an I/O request within the timeout window, the NVMe controller terminates its admin queue and I/O queue connections leading to NVMe controller teardown. If the NVMe host does not receive a response to a keep-alive request or an I/O request within the timeout window, the NVMe host initiates a connection disconnect.


Example: 1500"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the nvme_subsystem_controller."""

    subsystem = marshmallow_fields.Nested("netapp_ontap.resources.nvme_subsystem.NvmeSubsystemSchema", data_key="subsystem", unknown=EXCLUDE, allow_none=True)
    r""" The subsystem field of the nvme_subsystem_controller."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the nvme_subsystem_controller."""

    tls = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_controller_tls.NvmeSubsystemControllerTlsSchema", data_key="tls", unknown=EXCLUDE, allow_none=True)
    r""" A container for properties that describe the encrypted NVMe/TCP transport connection between the host and the NVMe subsystem."""

    transport_protocol = marshmallow_fields.Str(
        data_key="transport_protocol",
        validate=enum_validation(['fc_nvme', 'nvme_tcp']),
        allow_none=True,
    )
    r""" Transport Protocol

Valid choices:

* fc_nvme
* nvme_tcp"""

    @property
    def resource(self):
        return NvmeSubsystemController

    gettable_fields = [
        "links",
        "admin_queue",
        "dh_hmac_chap",
        "digest",
        "host",
        "id",
        "interface",
        "io_queue",
        "keep_alive_timeout",
        "node.links",
        "node.name",
        "node.uuid",
        "subsystem.links",
        "subsystem.name",
        "subsystem.uuid",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "tls",
        "transport_protocol",
    ]
    """links,admin_queue,dh_hmac_chap,digest,host,id,interface,io_queue,keep_alive_timeout,node.links,node.name,node.uuid,subsystem.links,subsystem.name,subsystem.uuid,svm.links,svm.name,svm.uuid,tls,transport_protocol,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class NvmeSubsystemController(Resource):
    r""" A Non-Volatile Memory Express (NVMe) subsystem controller represents a connection between a host and a storage solution.<br/>
An NVMe subsystem controller is identified by the NVMe subsystem UUID and the controller ID. """

    _schema = NvmeSubsystemControllerSchema
    _path = "/api/protocols/nvme/subsystem-controllers"
    _keys = ["subsystem.uuid", "id"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves NVMe subsystem controllers.
### Related ONTAP commands
* `vserver nvme subsystem controller show`
### Learn more
* [`DOC /protocols/nvme/subsystem-controllers`](#docs-NVMe-protocols_nvme_subsystem-controllers)
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
        """Returns a count of all NvmeSubsystemController resources that match the provided query"""
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
        """Returns a list of RawResources that represent NvmeSubsystemController resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves NVMe subsystem controllers.
### Related ONTAP commands
* `vserver nvme subsystem controller show`
### Learn more
* [`DOC /protocols/nvme/subsystem-controllers`](#docs-NVMe-protocols_nvme_subsystem-controllers)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an NVMe subsystem controller.
### Related ONTAP commands
* `vserver nvme subsystem controller show`
### Learn more
* [`DOC /protocols/nvme/subsystem-controllers`](#docs-NVMe-protocols_nvme_subsystem-controllers)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





