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


__all__ = ["PoliciesAndRulesToBeApplied", "PoliciesAndRulesToBeAppliedSchema"]
__pdoc__ = {
    "PoliciesAndRulesToBeAppliedSchema.resource": False,
    "PoliciesAndRulesToBeAppliedSchema.opts": False,
}


class PoliciesAndRulesToBeAppliedSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the PoliciesAndRulesToBeApplied object"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the policies_and_rules_to_be_applied."""

    to_be_applied = marshmallow_fields.Nested("netapp_ontap.models.policies_and_rules_to_be_applied_to_be_applied.PoliciesAndRulesToBeAppliedToBeAppliedSchema", data_key="to_be_applied", unknown=EXCLUDE, allow_none=True)
    r""" The to_be_applied field of the policies_and_rules_to_be_applied."""

    @property
    def resource(self):
        return PoliciesAndRulesToBeApplied

    gettable_fields = [
        "svm.links",
        "svm.name",
        "svm.uuid",
        "to_be_applied",
    ]
    """svm.links,svm.name,svm.uuid,to_be_applied,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class PoliciesAndRulesToBeApplied(Resource):
    """Allows interaction with PoliciesAndRulesToBeApplied objects on the host"""

    _schema = PoliciesAndRulesToBeAppliedSchema
    _path = "/api/protocols/cifs/group-policies"
    _keys = ["svm.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves group policy objects that are yet to be applied for all SVMs.
### Related ONTAP commands
* `vserver cifs group-policy show-defined`
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
        """Returns a count of all PoliciesAndRulesToBeApplied resources that match the provided query"""
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
        """Returns a list of RawResources that represent PoliciesAndRulesToBeApplied resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["PoliciesAndRulesToBeApplied"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Will create a background task to update the GPO settings for specified SVM.
### Related ONTAP commands
* `vserver cifs group-policy update`
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves group policy objects that are yet to be applied for all SVMs.
### Related ONTAP commands
* `vserver cifs group-policy show-defined`
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves group policy objects that are yet to be applied for specified SVM.
### Related ONTAP commands
* `vserver cifs group-policy show-defined`
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
        r"""Will create a background task to update the GPO settings for specified SVM.
### Related ONTAP commands
* `vserver cifs group-policy update`
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



