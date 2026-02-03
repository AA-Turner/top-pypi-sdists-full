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


__all__ = ["DataEnginePolicy", "DataEnginePolicySchema"]
__pdoc__ = {
    "DataEnginePolicySchema.resource": False,
    "DataEnginePolicySchema.opts": False,
}

class DataEnginePolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEnginePolicy object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the data_engine_policy."""

    actions = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_engine_policy_actions", "DataEnginePolicyActionsSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="actions",
                allow_none=True
            )
    r""" A list of actions to be performed by the data engine policy."""

    attributes = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_engine_event_attributes", "DataEngineEventAttributesSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="attributes",
                allow_none=True
            )
    r""" The list of attributes associated with the data engine policy."""

    conditions = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_engine_policy_conditions", "DataEnginePolicyConditionsSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="conditions",
                allow_none=True
            )
    r""" A list of conditions that define how the data engine policy should be applied."""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" The timestamp indicating when the data engine policy was created. This field is auto-generated.

Example: 2018-06-04T19:00:00.000+0000"""

    delete_time = ImpreciseDateTime(
        data_key="delete_time",
        allow_none=True,
    )
    r""" The timestamp indicating when the data engine policy was deleted. This field is auto-generated.

Example: 2018-06-04T19:00:00.000+0000"""

    description = marshmallow_fields.Str(
        data_key="description",
        allow_none=True,
    )
    r""" A detailed description of the data engine policy.

Example: Exclude email addresses from the files."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Indicates whether the data engine policy is enabled.


Example: true"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the data engine policy. This field is required for POST requests.

Example: Exclude email addresses."""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['global', 'workspace', 'data_source', 'data_collection']),
        allow_none=True,
    )
    r""" Specifies the scope of the data engine policy. Possible values are:

* <i>global</i> - Applies globally.
* <i>workspace</i> - Applies to workspaces.
* <i>data_source</i> - Applies to data sources.
* <i>data_collection</i> - Applies to data collections.


Valid choices:

* global
* workspace
* data_source
* data_collection"""

    target = marshmallow_fields.Str(
        data_key="target",
        validate=enum_validation(['workspace', 'data_source', 'data_collection']),
        allow_none=True,
    )
    r""" Target resources for the data engine policy.

* <i>workspace</i> - Targets workspaces.
* <i>data_source</i> - Targets data sources.
* <i>data_collection</i> - Targets data collections.


Valid choices:

* workspace
* data_source
* data_collection"""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['data_source_exclusion', 'classifier', 'classification_guardrail']),
        allow_none=True,
    )
    r""" Specifies the type of the data engine policy. Possible values are:

* <i>data_source_exclusion</i> - A global data source exclusion policy.
* <i>classifier</i> - A global classifier enablement policy.
* <i>classification_guardrail</i> - A classification guardrail policy.


Valid choices:

* data_source_exclusion
* classifier
* classification_guardrail"""

    update_time = ImpreciseDateTime(
        data_key="update_time",
        allow_none=True,
    )
    r""" The timestamp indicating when the data engine policy was last updated. This field is auto-generated.

Example: 2018-06-04T19:00:00.000+0000"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier of the data engine policy.

Example: 02c9e252-41be-11e9-81d5-00a0986138f7"""

    version = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_policy_version1", "DataEnginePolicyVersion1Schema"),
                data_key="version",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The version field of the data_engine_policy."""

    @property
    def resource(self):
        return DataEnginePolicy

    gettable_fields = [
        "links",
        "actions",
        "attributes",
        "conditions",
        "create_time",
        "delete_time",
        "description",
        "enabled",
        "name",
        "scope",
        "target",
        "type",
        "update_time",
        "uuid",
        "version",
    ]
    """links,actions,attributes,conditions,create_time,delete_time,description,enabled,name,scope,target,type,update_time,uuid,version,"""

    patchable_fields = [
        "actions",
        "attributes",
        "conditions",
        "description",
        "enabled",
        "name",
        "scope",
        "target",
        "type",
    ]
    """actions,attributes,conditions,description,enabled,name,scope,target,type,"""

    postable_fields = [
        "actions",
        "attributes",
        "conditions",
        "description",
        "enabled",
        "name",
        "scope",
        "target",
        "type",
    ]
    """actions,attributes,conditions,description,enabled,name,scope,target,type,"""

class DataEnginePolicy(Resource):
    r""" Data engine policy. """

    _schema = DataEnginePolicySchema
    _path = "/api/data-engine/policies"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of policies.
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
        """Returns a count of all DataEnginePolicy resources that match the provided query"""
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
        """Returns a list of RawResources that represent DataEnginePolicy resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["DataEnginePolicy"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a data engine policy. Every update to the data engine policy creates a new version of the policy.
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of policies.
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the details of the specified data engine policy.
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
        r"""Updates a data engine policy. Every update to the data engine policy creates a new version of the policy.
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



