r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

##  Examples
### Retrieving the Kerberos realm details
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KerberosRealm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(KerberosRealm.get_collection()))

```

### Creating the Kerberos realm for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KerberosRealm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = KerberosRealm()
    resource.svm.uuid = "05c90dc2-7343-11e8-9eb4-0050568be2b7"
    resource.name = "NFS-NSR-W02.RTP.NETAPP.COM"
    resource.kdc = {"vendor": "microsoft", "ip": "10.225.185.112", "port": 88}
    resource.comment = "realm"
    resource.ad_server = {
        "name": "nfs-nsr-w02.rtp.netapp.com",
        "address": "10.225.185.112",
    }
    resource.post(hydrate=True)
    print(resource)

```

### Updating the Kerberos realm for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KerberosRealm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = KerberosRealm(
        name="NFS-NSR-W02.RTP.NETAPP.COM",
        **{"svm.uuid": "05c90dc2-7343-11e8-9eb4-0050568be2b7"}
    )
    resource.kdc = {"vendor": "Microsoft", "ip": "100.225.185.112", "port": 88}
    resource.comment = "realm modify"
    resource.ad_server = {"name": "nfs.netapp.com", "address": "192.2.18.112"}
    resource.patch()

```

### Deleting the Kerberos realm for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KerberosRealm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = KerberosRealm(
        name="NFS-NSR-W02.RTP.NETAPP.COM",
        **{"svm.uuid": "05c90dc2-7343-11e8-9eb4-0050568be2b7"}
    )
    resource.delete()

```

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


__all__ = ["KerberosRealm", "KerberosRealmSchema"]
__pdoc__ = {
    "KerberosRealmSchema.resource": False,
    "KerberosRealmSchema.opts": False,
}


class KerberosRealmSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the KerberosRealm object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the kerberos_realm."""

    ad_server = marshmallow_fields.Nested("netapp_ontap.models.kerberos_realm_ad_server.KerberosRealmAdServerSchema", data_key="ad_server", unknown=EXCLUDE, allow_none=True)
    r""" The ad_server field of the kerberos_realm."""

    admin_server = marshmallow_fields.Nested("netapp_ontap.models.kerberos_realm_admin_server.KerberosRealmAdminServerSchema", data_key="admin_server", unknown=EXCLUDE, allow_none=True)
    r""" The admin_server field of the kerberos_realm."""

    clock_skew = Size(
        data_key="clock_skew",
        allow_none=True,
    )
    r""" Specifies the allowed time of clock-skew between the server and clients, in minutes."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        allow_none=True,
    )
    r""" Comment"""

    encryption_types = marshmallow_fields.List(marshmallow_fields.Str, data_key="encryption_types", allow_none=True)
    r""" The encryption_types field of the kerberos_realm."""

    kdc = marshmallow_fields.Nested("netapp_ontap.models.kerberos_realm_kdc.KerberosRealmKdcSchema", data_key="kdc", unknown=EXCLUDE, allow_none=True)
    r""" The kdc field of the kerberos_realm."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Kerberos realm"""

    password_server = marshmallow_fields.Nested("netapp_ontap.models.kerberos_realm_password_server.KerberosRealmPasswordServerSchema", data_key="password_server", unknown=EXCLUDE, allow_none=True)
    r""" The password_server field of the kerberos_realm."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the kerberos_realm."""

    @property
    def resource(self):
        return KerberosRealm

    gettable_fields = [
        "links",
        "ad_server",
        "admin_server",
        "clock_skew",
        "comment",
        "encryption_types",
        "kdc",
        "name",
        "password_server",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,ad_server,admin_server,clock_skew,comment,encryption_types,kdc,name,password_server,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "ad_server",
        "admin_server",
        "clock_skew",
        "comment",
        "kdc",
        "name",
        "password_server",
        "svm.name",
        "svm.uuid",
    ]
    """ad_server,admin_server,clock_skew,comment,kdc,name,password_server,svm.name,svm.uuid,"""

    postable_fields = [
        "ad_server",
        "admin_server",
        "clock_skew",
        "comment",
        "kdc",
        "name",
        "password_server",
        "svm.name",
        "svm.uuid",
    ]
    """ad_server,admin_server,clock_skew,comment,kdc,name,password_server,svm.name,svm.uuid,"""

class KerberosRealm(Resource):
    """Allows interaction with KerberosRealm objects on the host"""

    _schema = KerberosRealmSchema
    _path = "/api/protocols/nfs/kerberos/realms"
    _keys = ["svm.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves Kerberos realms.
### Related ONTAP commands
* `vserver nfs kerberos realm show`
### Learn more
* [`DOC /protocols/nfs/kerberos/realms`](#docs-NAS-protocols_nfs_kerberos_realms)
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
        """Returns a count of all KerberosRealm resources that match the provided query"""
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
        """Returns a list of RawResources that represent KerberosRealm resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["KerberosRealm"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the properties of a Kerberos realm.
* `vserver nfs kerberos realm modify`
### Learn more
* [`DOC /protocols/nfs/kerberos/realms`](#docs-NAS-protocols_nfs_kerberos_realms)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["KerberosRealm"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["KerberosRealm"], NetAppResponse]:
        r"""Creates a Kerberos realm.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM on which to create the Kerberos realm.
* `name` - Base name for the Kerberos realm.
* `kdc.vendor` - Vendor of the Key Distribution Center (KDC) server for this Kerberos realm. If the configuration uses a Microsoft Active Directory domain for authentication, this field nust be `microsoft`.
* `kdc.ip` - IP address of the KDC server for this Kerberos realm.
### Recommended optional properties
* `ad_server.name` - Host name of the Active Directory Domain Controller (DC). This is a mandatory parameter if the kdc-vendor is `microsoft`.
* `ad_server.address` - IP address of the Active Directory Domain Controller (DC). This is a mandatory parameter if the kdc-vendor is `microsoft`.
### Default property values
If not specified in POST, the following default property value is assigned:
* `kdc.port` - _88_
* `admin_server.port` - _749_
* `password_server.port` - _464_
* `clock_skew` - _5_
### Related ONTAP commands
* `vserver nfs kerberos realm create`
### Learn more
* [`DOC /protocols/nfs/kerberos/realms`](#docs-NAS-protocols_nfs_kerberos_realms)
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
        records: Iterable["KerberosRealm"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a Kerberos realm.
* `vserver nfs kerberos realm delete`
### Learn more
* [`DOC /protocols/nfs/kerberos/realms`](#docs-NAS-protocols_nfs_kerberos_realms)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves Kerberos realms.
### Related ONTAP commands
* `vserver nfs kerberos realm show`
### Learn more
* [`DOC /protocols/nfs/kerberos/realms`](#docs-NAS-protocols_nfs_kerberos_realms)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a Kerberos realm.
* `vserver nfs kerberos realm show`
### Learn more
* [`DOC /protocols/nfs/kerberos/realms`](#docs-NAS-protocols_nfs_kerberos_realms)
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
        r"""Creates a Kerberos realm.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM on which to create the Kerberos realm.
* `name` - Base name for the Kerberos realm.
* `kdc.vendor` - Vendor of the Key Distribution Center (KDC) server for this Kerberos realm. If the configuration uses a Microsoft Active Directory domain for authentication, this field nust be `microsoft`.
* `kdc.ip` - IP address of the KDC server for this Kerberos realm.
### Recommended optional properties
* `ad_server.name` - Host name of the Active Directory Domain Controller (DC). This is a mandatory parameter if the kdc-vendor is `microsoft`.
* `ad_server.address` - IP address of the Active Directory Domain Controller (DC). This is a mandatory parameter if the kdc-vendor is `microsoft`.
### Default property values
If not specified in POST, the following default property value is assigned:
* `kdc.port` - _88_
* `admin_server.port` - _749_
* `password_server.port` - _464_
* `clock_skew` - _5_
### Related ONTAP commands
* `vserver nfs kerberos realm create`
### Learn more
* [`DOC /protocols/nfs/kerberos/realms`](#docs-NAS-protocols_nfs_kerberos_realms)
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
        r"""Updates the properties of a Kerberos realm.
* `vserver nfs kerberos realm modify`
### Learn more
* [`DOC /protocols/nfs/kerberos/realms`](#docs-NAS-protocols_nfs_kerberos_realms)
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
        r"""Deletes a Kerberos realm.
* `vserver nfs kerberos realm delete`
### Learn more
* [`DOC /protocols/nfs/kerberos/realms`](#docs-NAS-protocols_nfs_kerberos_realms)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


