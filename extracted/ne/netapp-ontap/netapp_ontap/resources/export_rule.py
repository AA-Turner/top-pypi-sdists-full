r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

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


__all__ = ["ExportRule", "ExportRuleSchema"]
__pdoc__ = {
    "ExportRuleSchema.resource": False,
    "ExportRuleSchema.opts": False,
}


class ExportRuleSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ExportRule object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the export_rule."""

    allow_device_creation = marshmallow_fields.Boolean(
        data_key="allow_device_creation",
        allow_none=True,
    )
    r""" Specifies whether or not device creation is allowed."""

    allow_suid = marshmallow_fields.Boolean(
        data_key="allow_suid",
        allow_none=True,
    )
    r""" Specifies whether or not SetUID bits in SETATTR Op is to be honored."""

    anonymous_user = marshmallow_fields.Str(
        data_key="anonymous_user",
        allow_none=True,
    )
    r""" User ID To Which Anonymous Users Are Mapped."""

    chown_mode = marshmallow_fields.Str(
        data_key="chown_mode",
        validate=enum_validation(['restricted', 'unrestricted']),
        allow_none=True,
    )
    r""" Specifies who is authorized to change the ownership mode of a file.

Valid choices:

* restricted
* unrestricted"""

    clients = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.export_clients.ExportClientsSchema", unknown=EXCLUDE, allow_none=True), data_key="clients", allow_none=True)
    r""" Array of client matches"""

    index = Size(
        data_key="index",
        allow_none=True,
    )
    r""" Index of the rule within the export policy."""

    ntfs_unix_security = marshmallow_fields.Str(
        data_key="ntfs_unix_security",
        validate=enum_validation(['fail', 'ignore']),
        allow_none=True,
    )
    r""" NTFS export UNIX security options.

Valid choices:

* fail
* ignore"""

    policy = marshmallow_fields.Nested("netapp_ontap.models.export_rule_policy.ExportRulePolicySchema", data_key="policy", unknown=EXCLUDE, allow_none=True)
    r""" The policy field of the export_rule."""

    protocols = marshmallow_fields.List(marshmallow_fields.Str, data_key="protocols", allow_none=True)
    r""" The protocols field of the export_rule."""

    ro_rule = marshmallow_fields.List(marshmallow_fields.Str, data_key="ro_rule", allow_none=True)
    r""" Authentication flavors that the read-only access rule governs"""

    rw_rule = marshmallow_fields.List(marshmallow_fields.Str, data_key="rw_rule", allow_none=True)
    r""" Authentication flavors that the read/write access rule governs"""

    superuser = marshmallow_fields.List(marshmallow_fields.Str, data_key="superuser", allow_none=True)
    r""" Authentication flavors that the superuser security type governs"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the export_rule."""

    @property
    def resource(self):
        return ExportRule

    gettable_fields = [
        "links",
        "allow_device_creation",
        "allow_suid",
        "anonymous_user",
        "chown_mode",
        "clients",
        "index",
        "ntfs_unix_security",
        "policy",
        "protocols",
        "ro_rule",
        "rw_rule",
        "superuser",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,allow_device_creation,allow_suid,anonymous_user,chown_mode,clients,index,ntfs_unix_security,policy,protocols,ro_rule,rw_rule,superuser,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "allow_device_creation",
        "allow_suid",
        "anonymous_user",
        "chown_mode",
        "clients",
        "index",
        "ntfs_unix_security",
        "protocols",
        "ro_rule",
        "rw_rule",
        "superuser",
    ]
    """allow_device_creation,allow_suid,anonymous_user,chown_mode,clients,index,ntfs_unix_security,protocols,ro_rule,rw_rule,superuser,"""

    postable_fields = [
        "allow_device_creation",
        "allow_suid",
        "anonymous_user",
        "chown_mode",
        "clients",
        "index",
        "ntfs_unix_security",
        "policy",
        "protocols",
        "ro_rule",
        "rw_rule",
        "superuser",
    ]
    """allow_device_creation,allow_suid,anonymous_user,chown_mode,clients,index,ntfs_unix_security,policy,protocols,ro_rule,rw_rule,superuser,"""

class ExportRule(Resource):
    """Allows interaction with ExportRule objects on the host"""

    _schema = ExportRuleSchema
    _path = "/api/protocols/nfs/export-policies/{policy[id]}/rules"
    _keys = ["policy.id", "index"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves export policy rules.
### Related ONTAP commands
* `vserver export-policy rule show`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
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
        """Returns a count of all ExportRule resources that match the provided query"""
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
        """Returns a list of RawResources that represent ExportRule resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["ExportRule"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the properties of an export policy rule to change an export policy rule's index or fields.
### Related ONTAP commands
* `vserver export-policy rule modify`
* `vserver export-policy rule setindex`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["ExportRule"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["ExportRule"], NetAppResponse]:
        r"""Creates an export policy rule.
### Required properties
* `policy.id`  - Existing export policy for which to create an export rule.
* `clients.match`  - List of clients (hostnames, ipaddresses, netgroups, domains) to which the export rule applies.
* `ro_rule`  - Used to specify the security type for read-only access to volumes that use the export rule.
* `rw_rule`  - Used to specify the security type for read-write access to volumes that use the export rule.
### Optional property
* `index`    - Used to specify the index number of the export rule that you want to create. If you specify an index number that already matches a rule, the index number of the existing rule is incremented, as are the index numbers of all subsequent rules, either to the end of the list or to an open space in the list. If you do not specify an index number, the new rule is placed at the end of the policy's list.
### Default property values
If not specified in POST, the following default property values are assigned:
* `protocols` - _any_
* `anonymous_user` - _none_
* `superuser` - _any_
* `allow_device_creation` - _true_
* `ntfs_unix_security` - _fail_
* `chown_mode` - _restricted_
* `allow_suid` - _true_
### Related ONTAP commands
* `vserver export-policy rule create`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
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
        records: Iterable["ExportRule"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an export policy rule.
### Related ONTAP commands
* `vserver export-policy rule delete`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves export policy rules.
### Related ONTAP commands
* `vserver export-policy rule show`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an export policy rule
### Related ONTAP commands
* `vserver export-policy rule show`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
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
        r"""Creates an export policy rule.
### Required properties
* `policy.id`  - Existing export policy for which to create an export rule.
* `clients.match`  - List of clients (hostnames, ipaddresses, netgroups, domains) to which the export rule applies.
* `ro_rule`  - Used to specify the security type for read-only access to volumes that use the export rule.
* `rw_rule`  - Used to specify the security type for read-write access to volumes that use the export rule.
### Optional property
* `index`    - Used to specify the index number of the export rule that you want to create. If you specify an index number that already matches a rule, the index number of the existing rule is incremented, as are the index numbers of all subsequent rules, either to the end of the list or to an open space in the list. If you do not specify an index number, the new rule is placed at the end of the policy's list.
### Default property values
If not specified in POST, the following default property values are assigned:
* `protocols` - _any_
* `anonymous_user` - _none_
* `superuser` - _any_
* `allow_device_creation` - _true_
* `ntfs_unix_security` - _fail_
* `chown_mode` - _restricted_
* `allow_suid` - _true_
### Related ONTAP commands
* `vserver export-policy rule create`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
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
        r"""Updates the properties of an export policy rule to change an export policy rule's index or fields.
### Related ONTAP commands
* `vserver export-policy rule modify`
* `vserver export-policy rule setindex`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
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
        r"""Deletes an export policy rule.
### Related ONTAP commands
* `vserver export-policy rule delete`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


