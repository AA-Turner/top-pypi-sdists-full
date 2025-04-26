r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
When group policy objects (GPO) are enabled on your SMB server, ONTAP sends LDAP queries to the Active Directory server requesting GPO information.
If there are GPO definitions that are applicable to your SMB server, the Active Directory server returns the following GPO information:
• GPO name
• Current GPO version
• Location of the GPO definition
• Lists of UUIDs (universally unique identifiers) for GPO policy sets"""

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


__all__ = ["GroupPolicyObject", "GroupPolicyObjectSchema"]
__pdoc__ = {
    "GroupPolicyObjectSchema.resource": False,
    "GroupPolicyObjectSchema.opts": False,
}


class GroupPolicyObjectSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the GroupPolicyObject object"""

    central_access_policy_settings = marshmallow_fields.List(marshmallow_fields.Str, data_key="central_access_policy_settings", allow_none=True)
    r""" Will not be populated for objects that are yet to be applied."""

    central_access_policy_staging_audit_type = marshmallow_fields.Str(
        data_key="central_access_policy_staging_audit_type",
        validate=enum_validation(['none', 'success', 'failure', 'both']),
        allow_none=True,
    )
    r""" Types of events to be audited.

Valid choices:

* none
* success
* failure
* both"""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Specifies whether group policies are enabled for the SVM."""

    extensions = marshmallow_fields.List(marshmallow_fields.Str, data_key="extensions", allow_none=True)
    r""" List of extensions."""

    file_system_path = marshmallow_fields.Str(
        data_key="file_system_path",
        allow_none=True,
    )
    r""" File system path.

Example: \test.com\SysVol\test.com\policies\{42474212-3f9d-4489-ae01-6fcf4f805d4c}"""

    index = Size(
        data_key="index",
        allow_none=True,
    )
    r""" Group policy object index.

Example: 1"""

    ldap_path = marshmallow_fields.Str(
        data_key="ldap_path",
        allow_none=True,
    )
    r""" LDAP path to the GPO.

Example: cn={42474212-3f9d-4489-ae01-6fcf4f805d4c},cn=policies,cn=system,DC=TEST,DC=COM"""

    link = marshmallow_fields.Str(
        data_key="link",
        validate=enum_validation(['local', 'site', 'domain', 'organizational_unit', 'rsop']),
        allow_none=True,
    )
    r""" Link info.

Valid choices:

* local
* site
* domain
* organizational_unit
* rsop"""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1),
        allow_none=True,
    )
    r""" The name field of the group_policy_object.

Example: test_policy"""

    registry_settings = marshmallow_fields.Nested("netapp_ontap.models.group_policy_object_registry_setting.GroupPolicyObjectRegistrySettingSchema", data_key="registry_settings", unknown=EXCLUDE, allow_none=True)
    r""" The registry_settings field of the group_policy_object."""

    security_settings = marshmallow_fields.Nested("netapp_ontap.models.group_policy_object_security_setting.GroupPolicyObjectSecuritySettingSchema", data_key="security_settings", unknown=EXCLUDE, allow_none=True)
    r""" The security_settings field of the group_policy_object."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the group_policy_object."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Policy UUID.

Example: 42474212-3f9d-4489-ae01-6fcf4f805d4c"""

    version = Size(
        data_key="version",
        allow_none=True,
    )
    r""" Group policy object version.

Example: 7"""

    @property
    def resource(self):
        return GroupPolicyObject

    gettable_fields = [
        "central_access_policy_settings",
        "central_access_policy_staging_audit_type",
        "enabled",
        "extensions",
        "file_system_path",
        "index",
        "ldap_path",
        "link",
        "name",
        "registry_settings",
        "security_settings",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
        "version",
    ]
    """central_access_policy_settings,central_access_policy_staging_audit_type,enabled,extensions,file_system_path,index,ldap_path,link,name,registry_settings,security_settings,svm.links,svm.name,svm.uuid,uuid,version,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class GroupPolicyObject(Resource):
    """Allows interaction with GroupPolicyObject objects on the host"""

    _schema = GroupPolicyObjectSchema
    _path = "/api/protocols/cifs/group-policies/{svm[uuid]}/objects"
    _keys = ["svm.uuid", "index"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves applied group policy objects for specified SVM.
### Related ONTAP commands
* `vserver cifs group-policy show-applied`

### Learn more
* [`DOC /protocols/cifs/group-policies/{svm.uuid}/objects`](#docs-NAS-protocols_cifs_group-policies_{svm.uuid}_objects)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all GroupPolicyObject resources that match the provided query"""
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
        """Returns a list of RawResources that represent GroupPolicyObject resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves applied group policy objects for specified SVM.
### Related ONTAP commands
* `vserver cifs group-policy show-applied`

### Learn more
* [`DOC /protocols/cifs/group-policies/{svm.uuid}/objects`](#docs-NAS-protocols_cifs_group-policies_{svm.uuid}_objects)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves applied group policy object for specified SVM.
### Related ONTAP commands
* `vserver cifs group-policy show-applied`

### Learn more
* [`DOC /protocols/cifs/group-policies/{svm.uuid}/objects`](#docs-NAS-protocols_cifs_group-policies_{svm.uuid}_objects)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





