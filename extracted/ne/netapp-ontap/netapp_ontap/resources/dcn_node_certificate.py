r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API endpoint is designed to manage certificates that are used by DCN nodes. The PATCH method is used to update the certificate of a given DCN node, while the GET method retrieves the certificate of a given DCN node.
<br />
---
## Examples
### Retrieving the certificate that is used by DCN nodes
The following output shows the certificate that is used by DCN nodes.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import DcnNodeCertificate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(DcnNodeCertificate.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    DcnNodeCertificate(
        {
            "dcn-node-name": "node1",
            "_links": {"self": {"href": "/api/dcn/security/node/certificates/node1"}},
        }
    ),
    DcnNodeCertificate(
        {
            "dcn-node-name": "node2",
            "_links": {"self": {"href": "/api/dcn/security/node/certificates/node2"}},
        }
    ),
    DcnNodeCertificate(
        {
            "dcn-node-name": "node3",
            "_links": {"self": {"href": "/api/dcn/security/node/certificates/node3"}},
        }
    ),
]

```
</div>
</div>

---
### Modifies the certificate that is used by DCN nodes
The following output shows how to update the certificate that is used by DCN nodes.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import DcnNodeCertificate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = DcnNodeCertificate(dcn - node - name="<node-name>")
    resource.dcn_cert_name = "dcn-cert1"
    resource.patch()

```
"""

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


__all__ = ["DcnNodeCertificate", "DcnNodeCertificateSchema"]
__pdoc__ = {
    "DcnNodeCertificateSchema.resource": False,
    "DcnNodeCertificateSchema.opts": False,
}

class DcnNodeCertificateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnNodeCertificate object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the dcn_node_certificate."""

    dcn_cert_name = marshmallow_fields.Str(
        data_key="dcn-cert-name",
        allow_none=True,
    )
    r""" Certificate name used by DCN.

Example: dcn-node1-cert"""

    dcn_node_name = marshmallow_fields.Str(
        data_key="dcn-node-name",
        allow_none=True,
    )
    r""" The DCN node name.

Example: dcn-node1"""

    @property
    def resource(self):
        return DcnNodeCertificate

    gettable_fields = [
        "links",
        "dcn_cert_name",
        "dcn_node_name",
    ]
    """links,dcn_cert_name,dcn_node_name,"""

    patchable_fields = [
        "dcn_cert_name",
    ]
    """dcn_cert_name,"""

    postable_fields = [
    ]
    """"""

class DcnNodeCertificate(Resource):
    """Allows interaction with DcnNodeCertificate objects on the host"""

    _schema = DcnNodeCertificateSchema
    _path = "/api/dcn/security/node/certificates"
    _keys = ["dcn-node-name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the certificate that is used by DCN nodes.
### Related ONTAP commands
* `dcn security certificate show`

### Learn more
* [`DOC /dcn/security/node/certificates`](#docs-security-dcn_security_node_certificates)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all DcnNodeCertificate resources that match the provided query"""
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
        """Returns a list of RawResources that represent DcnNodeCertificate resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["DcnNodeCertificate"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the certificate that is used by a specific DCN node.
### Required properties
* `dcn-node-name` - Name of the DCN node.
* `dcn-cert-name` - Certificate name used by the DCN node.
### Related ONTAP commands
* `dcn security certificate modify`

### Learn more
* [`DOC /dcn/security/node/certificates`](#docs-security-dcn_security_node_certificates)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the certificate that is used by DCN nodes.
### Related ONTAP commands
* `dcn security certificate show`

### Learn more
* [`DOC /dcn/security/node/certificates`](#docs-security-dcn_security_node_certificates)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a certificate for a given DCN.
### Related ONTAP commands
* `dcn security certificate show`

### Learn more
* [`DOC /dcn/security/node/certificates`](#docs-security-dcn_security_node_certificates)"""
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
        r"""Updates the certificate that is used by a specific DCN node.
### Required properties
* `dcn-node-name` - Name of the DCN node.
* `dcn-cert-name` - Certificate name used by the DCN node.
### Related ONTAP commands
* `dcn security certificate modify`

### Learn more
* [`DOC /dcn/security/node/certificates`](#docs-security-dcn_security_node_certificates)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



