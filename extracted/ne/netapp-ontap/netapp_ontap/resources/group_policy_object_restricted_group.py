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


__all__ = ["GroupPolicyObjectRestrictedGroup", "GroupPolicyObjectRestrictedGroupSchema"]
__pdoc__ = {
    "GroupPolicyObjectRestrictedGroupSchema.resource": False,
    "GroupPolicyObjectRestrictedGroupSchema.opts": False,
}


class GroupPolicyObjectRestrictedGroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the GroupPolicyObjectRestrictedGroup object"""

    group_name = marshmallow_fields.Str(
        data_key="group_name",
        validate=len_validation(minimum=1),
        allow_none=True,
    )
    r""" The group_name field of the group_policy_object_restricted_group.

Example: test_group"""

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

    members = marshmallow_fields.List(marshmallow_fields.Str, data_key="members", allow_none=True)
    r""" Members of the group.

Example: ["DOMAIN/test_user","DOMAIN/user2"]"""

    memberships = marshmallow_fields.List(marshmallow_fields.Str, data_key="memberships", allow_none=True)
    r""" Group is member of Group/OU.

Example: ["DOMAIN/AdministratorGrp","DOMAIN/deptMark"]"""

    policy_name = marshmallow_fields.Str(
        data_key="policy_name",
        validate=len_validation(minimum=1),
        allow_none=True,
    )
    r""" The policy_name field of the group_policy_object_restricted_group.

Example: test_policy"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the group_policy_object_restricted_group."""

    version = Size(
        data_key="version",
        allow_none=True,
    )
    r""" Group policy object version.

Example: 7"""

    @property
    def resource(self):
        return GroupPolicyObjectRestrictedGroup

    gettable_fields = [
        "group_name",
        "link",
        "members",
        "memberships",
        "policy_name",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "version",
    ]
    """group_name,link,members,memberships,policy_name,svm.links,svm.name,svm.uuid,version,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class GroupPolicyObjectRestrictedGroup(Resource):
    """Allows interaction with GroupPolicyObjectRestrictedGroup objects on the host"""

    _schema = GroupPolicyObjectRestrictedGroupSchema
    _path = "/api/protocols/cifs/group-policies/{svm[uuid]}/restricted-groups"
    _keys = ["svm.uuid", "policy_index", "group_name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves applied policies of restricted groups for specified SVM.
### Related ONTAP commands
* `vserver cifs group-policy restricted-group show-applied`
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
        """Returns a count of all GroupPolicyObjectRestrictedGroup resources that match the provided query"""
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
        """Returns a list of RawResources that represent GroupPolicyObjectRestrictedGroup resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves applied policies of restricted groups for specified SVM.
### Related ONTAP commands
* `vserver cifs group-policy restricted-group show-applied`
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves applied policy of restricted group for specified SVM.
### Related ONTAP commands
* `vserver cifs group-policy restricted-group show-applied`
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





