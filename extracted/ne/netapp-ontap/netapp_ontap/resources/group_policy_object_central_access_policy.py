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


__all__ = ["GroupPolicyObjectCentralAccessPolicy", "GroupPolicyObjectCentralAccessPolicySchema"]
__pdoc__ = {
    "GroupPolicyObjectCentralAccessPolicySchema.resource": False,
    "GroupPolicyObjectCentralAccessPolicySchema.opts": False,
}


class GroupPolicyObjectCentralAccessPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the GroupPolicyObjectCentralAccessPolicy object"""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" Policy creation timestamp.

Example: 2018-01-01T16:00:00.000+0000"""

    description = marshmallow_fields.Str(
        data_key="description",
        allow_none=True,
    )
    r""" Description about the policy.

Example: policy #1"""

    member_rules = marshmallow_fields.List(marshmallow_fields.Str, data_key="member_rules", allow_none=True)
    r""" Names of all central access rules applied to members.

Example: ["r1","r2"]"""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1),
        allow_none=True,
    )
    r""" The name field of the group_policy_object_central_access_policy.

Example: p1"""

    sid = marshmallow_fields.Str(
        data_key="sid",
        allow_none=True,
    )
    r""" Security ID, unique identifier of the central policy.

Example: S-1-5-21-256008430-3394229847-3930036330-1001"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the group_policy_object_central_access_policy."""

    update_time = ImpreciseDateTime(
        data_key="update_time",
        allow_none=True,
    )
    r""" Last policy modification timestamp.

Example: 2018-01-01T16:00:00.000+0000"""

    @property
    def resource(self):
        return GroupPolicyObjectCentralAccessPolicy

    gettable_fields = [
        "create_time",
        "description",
        "member_rules",
        "name",
        "sid",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "update_time",
    ]
    """create_time,description,member_rules,name,sid,svm.links,svm.name,svm.uuid,update_time,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class GroupPolicyObjectCentralAccessPolicy(Resource):
    """Allows interaction with GroupPolicyObjectCentralAccessPolicy objects on the host"""

    _schema = GroupPolicyObjectCentralAccessPolicySchema
    _path = "/api/protocols/cifs/group-policies/{svm[uuid]}/central-access-policies"
    _keys = ["svm.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves applied central access policies for specified SVM.
### Related ONTAP commands
* `vserver cifs group-policy central-access-policy show-applied`
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
        """Returns a count of all GroupPolicyObjectCentralAccessPolicy resources that match the provided query"""
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
        """Returns a list of RawResources that represent GroupPolicyObjectCentralAccessPolicy resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves applied central access policies for specified SVM.
### Related ONTAP commands
* `vserver cifs group-policy central-access-policy show-applied`
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves applied central access policy for specified SVM.
### Related ONTAP commands
* `vserver cifs group-policy central-access-policy show-applied`
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





