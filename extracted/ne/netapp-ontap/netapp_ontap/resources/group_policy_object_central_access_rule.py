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


__all__ = ["GroupPolicyObjectCentralAccessRule", "GroupPolicyObjectCentralAccessRuleSchema"]
__pdoc__ = {
    "GroupPolicyObjectCentralAccessRuleSchema.resource": False,
    "GroupPolicyObjectCentralAccessRuleSchema.opts": False,
}


class GroupPolicyObjectCentralAccessRuleSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the GroupPolicyObjectCentralAccessRule object"""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" Policy creation timestamp.

Example: 2018-01-01T16:00:00.000+0000"""

    current_permission = marshmallow_fields.Str(
        data_key="current_permission",
        allow_none=True,
    )
    r""" Effective security policy in security descriptor definition language format.

Example: O:SYG:SYD:AR(A;;FA;;;WD)"""

    description = marshmallow_fields.Str(
        data_key="description",
        allow_none=True,
    )
    r""" Description about the policy.

Example: rule #1"""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1),
        allow_none=True,
    )
    r""" The name field of the group_policy_object_central_access_rule.

Example: p1"""

    proposed_permission = marshmallow_fields.Str(
        data_key="proposed_permission",
        allow_none=True,
    )
    r""" Proposed security policy in security descriptor definition language format.

Example: O:SYG:SYD:(A;;FA;;;OW)(A;;FA;;;BA)(A;;FA;;;SY)"""

    resource_criteria = marshmallow_fields.Str(
        data_key="resource_criteria",
        allow_none=True,
    )
    r""" Criteria to scope resources for which access rules apply.

Example: department"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the group_policy_object_central_access_rule."""

    update_time = ImpreciseDateTime(
        data_key="update_time",
        allow_none=True,
    )
    r""" Last policy modification timestamp.

Example: 2018-01-01T16:00:00.000+0000"""

    @property
    def resource(self):
        return GroupPolicyObjectCentralAccessRule

    gettable_fields = [
        "create_time",
        "current_permission",
        "description",
        "name",
        "proposed_permission",
        "resource_criteria",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "update_time",
    ]
    """create_time,current_permission,description,name,proposed_permission,resource_criteria,svm.links,svm.name,svm.uuid,update_time,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class GroupPolicyObjectCentralAccessRule(Resource):
    """Allows interaction with GroupPolicyObjectCentralAccessRule objects on the host"""

    _schema = GroupPolicyObjectCentralAccessRuleSchema
    _path = "/api/protocols/cifs/group-policies/{svm[uuid]}/central-access-rules"
    _keys = ["svm.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves applied central access rules for specified SVM.
### Related ONTAP commands
* `vserver cifs group-policy central-access-rule show-applied`
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
        """Returns a count of all GroupPolicyObjectCentralAccessRule resources that match the provided query"""
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
        """Returns a list of RawResources that represent GroupPolicyObjectCentralAccessRule resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves applied central access rules for specified SVM.
### Related ONTAP commands
* `vserver cifs group-policy central-access-rule show-applied`
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves applied central access rule for specified SVM.
### Related ONTAP commands
* `vserver cifs group-policy central-access-rule show-applied`
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





