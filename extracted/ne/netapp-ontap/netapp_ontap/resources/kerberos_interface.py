r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

##  Examples
### Retrieving the Kerberos interface configuration details
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KerberosInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(KerberosInterface.get_collection()))

```

### Updating the Kerberos interface configuration
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KerberosInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = KerberosInterface(
        **{"interface.uuid": "e62936de-7342-11e8-9eb4-0050568be2b7"}
    )
    resource.enabled = True
    resource.spn = "nfs/datalif1-vsim3-d1.sim.netapp.com@NFS-NSR-W01.RTP.NETAPP.COM"
    resource.user = "administrator"
    resource.password = "Hello123!"
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


__all__ = ["KerberosInterface", "KerberosInterfaceSchema"]
__pdoc__ = {
    "KerberosInterfaceSchema.resource": False,
    "KerberosInterfaceSchema.opts": False,
}


class KerberosInterfaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the KerberosInterface object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the kerberos_interface."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Specifies if Kerberos is enabled."""

    encryption_types = marshmallow_fields.List(marshmallow_fields.Str, data_key="encryption_types", allow_none=True)
    r""" The encryption_types field of the kerberos_interface."""

    force = marshmallow_fields.Boolean(
        data_key="force",
        allow_none=True,
    )
    r""" Specifies whether the server should ignore any error encountered while deleting the corresponding machine account on the KDC and also disables Kerberos on the LIF."""

    interface = marshmallow_fields.Nested("netapp_ontap.resources.ip_interface.IpInterfaceSchema", data_key="interface", unknown=EXCLUDE, allow_none=True)
    r""" The interface field of the kerberos_interface."""

    keytab_uri = marshmallow_fields.Str(
        data_key="keytab_uri",
        allow_none=True,
    )
    r""" Load keytab from URI"""

    machine_account = marshmallow_fields.Str(
        data_key="machine_account",
        allow_none=True,
    )
    r""" Specifies the machine account to create in Active Directory."""

    organizational_unit = marshmallow_fields.Str(
        data_key="organizational_unit",
        allow_none=True,
    )
    r""" Organizational unit"""

    password = marshmallow_fields.Str(
        data_key="password",
        allow_none=True,
    )
    r""" Account creation password"""

    spn = marshmallow_fields.Str(
        data_key="spn",
        allow_none=True,
    )
    r""" Service principal name. Valid in PATCH."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the kerberos_interface."""

    user = marshmallow_fields.Str(
        data_key="user",
        allow_none=True,
    )
    r""" Account creation user name"""

    @property
    def resource(self):
        return KerberosInterface

    gettable_fields = [
        "links",
        "enabled",
        "encryption_types",
        "interface.links",
        "interface.ip",
        "interface.name",
        "interface.uuid",
        "machine_account",
        "spn",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,enabled,encryption_types,interface.links,interface.ip,interface.name,interface.uuid,machine_account,spn,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "enabled",
        "force",
        "keytab_uri",
        "machine_account",
        "organizational_unit",
        "password",
        "spn",
        "user",
    ]
    """enabled,force,keytab_uri,machine_account,organizational_unit,password,spn,user,"""

    postable_fields = [
        "enabled",
        "force",
        "keytab_uri",
        "machine_account",
        "organizational_unit",
        "password",
        "spn",
        "user",
    ]
    """enabled,force,keytab_uri,machine_account,organizational_unit,password,spn,user,"""

class KerberosInterface(Resource):
    """Allows interaction with KerberosInterface objects on the host"""

    _schema = KerberosInterfaceSchema
    _path = "/api/protocols/nfs/kerberos/interfaces"
    _keys = ["interface.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves Kerberos interfaces.
### Related ONTAP commands
* `vserver nfs kerberos interface show`
### Learn more
* [`DOC /protocols/nfs/kerberos/interfaces`](#docs-NAS-protocols_nfs_kerberos_interfaces)
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
        """Returns a count of all KerberosInterface resources that match the provided query"""
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
        """Returns a list of RawResources that represent KerberosInterface resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["KerberosInterface"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the properties of a Kerberos interface.
### Optional property
* `force` - Specifies whether the server should ignore any error encountered while deleting the corresponding machine account on the KDC and also disables Kerberos on the LIF. This is applicable only when disabling Kerberos.
### Related ONTAP commands
* `vserver nfs kerberos interface modify`
* `vserver nfs kerberos interface enable`
* `vserver nfs kerberos interface disable`
### Learn more
* [`DOC /protocols/nfs/kerberos/interfaces`](#docs-NAS-protocols_nfs_kerberos_interfaces)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves Kerberos interfaces.
### Related ONTAP commands
* `vserver nfs kerberos interface show`
### Learn more
* [`DOC /protocols/nfs/kerberos/interfaces`](#docs-NAS-protocols_nfs_kerberos_interfaces)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a Kerberos interface.
### Related ONTAP commands
* `vserver nfs kerberos interface show`
### Learn more
* [`DOC /protocols/nfs/kerberos/interfaces`](#docs-NAS-protocols_nfs_kerberos_interfaces)
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
        r"""Updates the properties of a Kerberos interface.
### Optional property
* `force` - Specifies whether the server should ignore any error encountered while deleting the corresponding machine account on the KDC and also disables Kerberos on the LIF. This is applicable only when disabling Kerberos.
### Related ONTAP commands
* `vserver nfs kerberos interface modify`
* `vserver nfs kerberos interface enable`
* `vserver nfs kerberos interface disable`
### Learn more
* [`DOC /protocols/nfs/kerberos/interfaces`](#docs-NAS-protocols_nfs_kerberos_interfaces)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



