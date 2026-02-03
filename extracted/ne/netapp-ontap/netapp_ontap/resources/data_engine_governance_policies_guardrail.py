r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

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


__all__ = ["DataEngineGovernancePoliciesGuardrail", "DataEngineGovernancePoliciesGuardrailSchema"]
__pdoc__ = {
    "DataEngineGovernancePoliciesGuardrailSchema.resource": False,
    "DataEngineGovernancePoliciesGuardrailSchema.opts": False,
}

class DataEngineGovernancePoliciesGuardrailSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineGovernancePoliciesGuardrail object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the data_engine_governance_policies_guardrail."""

    action_time = ImpreciseDateTime(
        data_key="action_time",
        allow_none=True,
    )
    r""" The timestamp from which actions specified in the `actions` array become effective for this policy.

* Applies to the entire policy, not individual actions.
* Only data collections created after this time will be affected by the policy's actions.
* If the `actions` array is updated and `action_time` is specified, it will be updated accordingly.
* For some actions (such as <i>exclude</i>), providing an `action_time` is required; for others (such as <i>anonymize</i>), it is currently optional.
* Setting `action_time` to a future date is allowed.
* There is no lag between updating the actions and their effectiveness as determined by this timestamp.
* Does not change when only other properties (such as `state`) are updated.


Example: 2018-06-04T19:00:00.000+0000"""

    actions = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_engine_governance_policies_guardrail_actions", "DataEngineGovernancePoliciesGuardrailActionsSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="actions",
                allow_none=True
            )
    r""" List of actions associated with the guardrail."""

    conditions = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_engine_governance_policies_guardrail_conditions", "DataEngineGovernancePoliciesGuardrailConditionsSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="conditions",
                allow_none=True
            )
    r""" List of conditions associated with the guardrail."""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" The timestamp indicating when the guardrail was created.

Example: 2018-06-04T19:00:00.000+0000"""

    description = marshmallow_fields.Str(
        data_key="description",
        allow_none=True,
    )
    r""" Description of the guardrail.

Example: exclude credit card number from data"""

    has_issue = marshmallow_fields.Boolean(
        data_key="has_issue",
        allow_none=True,
    )
    r""" Indicates if the guardrail has any issues.

Example: false"""

    impacted_files_count = Size(
        data_key="impacted_files_count",
        allow_none=True,
    )
    r""" The number of files impacted by the guardrail.

Example: 100"""

    issue_tags = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_engine_governance_policies_guardrail_issue_tags", "DataEngineGovernancePoliciesGuardrailIssueTagsSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="issue_tags",
                allow_none=True
            )
    r""" List of classifier or category tags which has issues."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the guardrail.

Example: exclude credit card number"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['enabled', 'disabled', 'simulate']),
        allow_none=True,
    )
    r""" State of the guardrail. Possible values are:

* <i>enabled</i>: Guardrail is enabled.
* <i>disabled</i>: Guardrail is disabled.
* <i>simulate</i>: Guardrail is in simulation mode.


Valid choices:

* enabled
* disabled
* simulate"""

    update_time = ImpreciseDateTime(
        data_key="update_time",
        allow_none=True,
    )
    r""" The timestamp indicating when the guardrail was last updated.

Example: 2018-06-04T19:00:00.000+0000"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" UUID of the guardrail.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412"""

    workspaces = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_engine_governance_policies_guardrail_workspaces", "DataEngineGovernancePoliciesGuardrailWorkspacesSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="workspaces",
                allow_none=True
            )
    r""" List of workspaces associated with the guardrail."""

    @property
    def resource(self):
        return DataEngineGovernancePoliciesGuardrail

    gettable_fields = [
        "links",
        "action_time",
        "actions",
        "conditions",
        "create_time",
        "description",
        "has_issue",
        "impacted_files_count",
        "issue_tags",
        "name",
        "state",
        "update_time",
        "uuid",
        "workspaces",
    ]
    """links,action_time,actions,conditions,create_time,description,has_issue,impacted_files_count,issue_tags,name,state,update_time,uuid,workspaces,"""

    patchable_fields = [
        "action_time",
        "actions",
        "conditions",
        "description",
        "issue_tags",
        "name",
        "state",
        "workspaces",
    ]
    """action_time,actions,conditions,description,issue_tags,name,state,workspaces,"""

    postable_fields = [
        "action_time",
        "actions",
        "conditions",
        "description",
        "issue_tags",
        "name",
        "state",
        "workspaces",
    ]
    """action_time,actions,conditions,description,issue_tags,name,state,workspaces,"""

class DataEngineGovernancePoliciesGuardrail(Resource):
    r""" Defines the structure of a guardrail. """

    _schema = DataEngineGovernancePoliciesGuardrailSchema
    _path = "/api/data-engine/governance/policies/guardrails"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of guardrails.
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
        """Returns a count of all DataEngineGovernancePoliciesGuardrail resources that match the provided query"""
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
        """Returns a list of RawResources that represent DataEngineGovernancePoliciesGuardrail resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["DataEngineGovernancePoliciesGuardrail"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the specified guardrail.
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["DataEngineGovernancePoliciesGuardrail"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["DataEngineGovernancePoliciesGuardrail"], NetAppResponse]:
        r"""Creates a new guardrail.
### Required properties
* `name`: Name of the guardrail.
* `description`: Description of the guardrail.
* `condition`: Condition under which the guardrail is applied.
* `action`: Action to be performed by the guardrail.
* `status`: Status of the guardrail.
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
        records: Iterable["DataEngineGovernancePoliciesGuardrail"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a guardrail.
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of guardrails.
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the details of the specified guardrail.
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
        r"""Creates a new guardrail.
### Required properties
* `name`: Name of the guardrail.
* `description`: Description of the guardrail.
* `condition`: Condition under which the guardrail is applied.
* `action`: Action to be performed by the guardrail.
* `status`: Status of the guardrail.
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
        r"""Updates the specified guardrail.
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
        r"""Deletes a guardrail.
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


