r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

##  Examples
### Retrieving the NFS over TLS interface configuration details
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NfsTlsInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(NfsTlsInterface.get_collection()))

```

### Updating the NFS over TLS interface configuration
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NfsTlsInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NfsTlsInterface(
        **{"interface.uuid": "e62936de-7342-11e8-9eb4-0050568be2b7"}
    )
    resource.enabled = True
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


__all__ = ["NfsTlsInterface", "NfsTlsInterfaceSchema"]
__pdoc__ = {
    "NfsTlsInterfaceSchema.resource": False,
    "NfsTlsInterfaceSchema.opts": False,
}


class NfsTlsInterfaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NfsTlsInterface object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the nfs_tls_interface."""

    certificate = marshmallow_fields.Nested("netapp_ontap.resources.security_certificate.SecurityCertificateSchema", data_key="certificate", unknown=EXCLUDE, allow_none=True)
    r""" The certificate field of the nfs_tls_interface."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Indicates whether NFS over TLS is enabled."""

    interface = marshmallow_fields.Nested("netapp_ontap.resources.ip_interface.IpInterfaceSchema", data_key="interface", unknown=EXCLUDE, allow_none=True)
    r""" The interface field of the nfs_tls_interface."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the nfs_tls_interface."""

    @property
    def resource(self):
        return NfsTlsInterface

    gettable_fields = [
        "links",
        "certificate.links",
        "certificate.name",
        "certificate.uuid",
        "enabled",
        "interface.links",
        "interface.ip",
        "interface.name",
        "interface.uuid",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,certificate.links,certificate.name,certificate.uuid,enabled,interface.links,interface.ip,interface.name,interface.uuid,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "certificate.name",
        "certificate.uuid",
        "enabled",
    ]
    """certificate.name,certificate.uuid,enabled,"""

    postable_fields = [
        "certificate.name",
        "certificate.uuid",
        "enabled",
    ]
    """certificate.name,certificate.uuid,enabled,"""

class NfsTlsInterface(Resource):
    """Allows interaction with NfsTlsInterface objects on the host"""

    _schema = NfsTlsInterfaceSchema
    _path = "/api/protocols/nfs/tls/interfaces"
    _keys = ["interface.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves NFS over TLS interfaces.
### Related ONTAP commands
* `vserver nfs tls interface show`
### Learn more
* [`DOC /protocols/nfs/tls/interfaces`](#docs-NAS-protocols_nfs_tls_interfaces)
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
        """Returns a count of all NfsTlsInterface resources that match the provided query"""
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
        """Returns a list of RawResources that represent NfsTlsInterface resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["NfsTlsInterface"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the properties of an NFS over TLS interface.
### Related ONTAP commands
* `vserver nfs tls interface modify`
* `vserver nfs tls interface enable`
* `vserver nfs tls interface disable`
### Learn more
* [`DOC /protocols/nfs/tls/interfaces`](#docs-NAS-protocols_nfs_tls_interfaces)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves NFS over TLS interfaces.
### Related ONTAP commands
* `vserver nfs tls interface show`
### Learn more
* [`DOC /protocols/nfs/tls/interfaces`](#docs-NAS-protocols_nfs_tls_interfaces)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an NFS over TLS interface.
### Related ONTAP commands
* `vserver nfs tls interface show`
### Learn more
* [`DOC /protocols/nfs/tls/interfaces`](#docs-NAS-protocols_nfs_tls_interfaces)
"""
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
        r"""Updates the properties of an NFS over TLS interface.
### Related ONTAP commands
* `vserver nfs tls interface modify`
* `vserver nfs tls interface enable`
* `vserver nfs tls interface disable`
### Learn more
* [`DOC /protocols/nfs/tls/interfaces`](#docs-NAS-protocols_nfs_tls_interfaces)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



