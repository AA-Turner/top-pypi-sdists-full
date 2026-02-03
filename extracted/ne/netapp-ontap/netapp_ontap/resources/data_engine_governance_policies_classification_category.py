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


__all__ = ["DataEngineGovernancePoliciesClassificationCategory", "DataEngineGovernancePoliciesClassificationCategorySchema"]
__pdoc__ = {
    "DataEngineGovernancePoliciesClassificationCategorySchema.resource": False,
    "DataEngineGovernancePoliciesClassificationCategorySchema.opts": False,
}

class DataEngineGovernancePoliciesClassificationCategorySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineGovernancePoliciesClassificationCategory object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the data_engine_governance_policies_classification_category."""

    classifiers = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_engine_governance_policies_classifier", "DataEngineGovernancePoliciesClassifierSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="classifiers",
                allow_none=True
            )
    r""" Defines the structure of a classifier."""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" The timestamp indicating when the category was created.

Example: 2018-06-04T19:00:00.000+0000"""

    custom = marshmallow_fields.Boolean(
        data_key="custom",
        allow_none=True,
    )
    r""" Indicates if the classification category is custom or predefined.

Example: false"""

    description = marshmallow_fields.Str(
        data_key="description",
        allow_none=True,
    )
    r""" Description of the classification category.

Example: General privacy classification category"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the classification category.

Example: General privacy"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['enabled', 'disabled', 'simulate']),
        allow_none=True,
    )
    r""" State of the classification category. Possible values are:

* <i>enabled</i>: Classification category is enabled.
* <i>disabled</i>: Classification category is disabled.
* <i>simulate</i>: Classification category is in simulation mode.


Valid choices:

* enabled
* disabled
* simulate"""

    tag = marshmallow_fields.Str(
        data_key="tag",
        allow_none=True,
    )
    r""" Tag associated with the classification category.

Example: CAT_GP00000"""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['data', 'document']),
        allow_none=True,
    )
    r""" Specifies the type of classification category. Possible values are:

* <i>data</i>: Classification category for data entities.
* <i>document</i>: Classification category for document entities.


Valid choices:

* data
* document"""

    update_time = ImpreciseDateTime(
        data_key="update_time",
        allow_none=True,
    )
    r""" The timestamp indicating when the category was last updated.

Example: 2018-06-04T19:00:00.000+0000"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier of the classification category.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return DataEngineGovernancePoliciesClassificationCategory

    gettable_fields = [
        "links",
        "classifiers",
        "create_time",
        "custom",
        "description",
        "name",
        "state",
        "tag",
        "type",
        "update_time",
        "uuid",
    ]
    """links,classifiers,create_time,custom,description,name,state,tag,type,update_time,uuid,"""

    patchable_fields = [
        "classifiers",
        "custom",
        "description",
        "name",
        "state",
        "tag",
        "type",
    ]
    """classifiers,custom,description,name,state,tag,type,"""

    postable_fields = [
        "classifiers",
        "custom",
        "description",
        "name",
        "state",
        "tag",
        "type",
    ]
    """classifiers,custom,description,name,state,tag,type,"""

class DataEngineGovernancePoliciesClassificationCategory(Resource):
    r""" Defines the structure of a classification category. """

    _schema = DataEngineGovernancePoliciesClassificationCategorySchema
    _path = "/api/data-engine/governance/policies/classification/categories"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of categories.
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
        """Returns a count of all DataEngineGovernancePoliciesClassificationCategory resources that match the provided query"""
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
        """Returns a list of RawResources that represent DataEngineGovernancePoliciesClassificationCategory resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["DataEngineGovernancePoliciesClassificationCategory"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the specified category.
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["DataEngineGovernancePoliciesClassificationCategory"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["DataEngineGovernancePoliciesClassificationCategory"], NetAppResponse]:
        r"""Creates a new category.
### Required properties
* `name`: Name of the category.
* `description`: Description of the category.
* `tag`: Tag associated with the category.
* `classifiers`: List of classifiers associated with the category.
* `status`: Status of the category.
* `custom`: Specifies if the category is user-defined.
* `type`: Type of the category.
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
        records: Iterable["DataEngineGovernancePoliciesClassificationCategory"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a category.
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of categories.
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the details of the specified category.
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
        r"""Creates a new category.
### Required properties
* `name`: Name of the category.
* `description`: Description of the category.
* `tag`: Tag associated with the category.
* `classifiers`: List of classifiers associated with the category.
* `status`: Status of the category.
* `custom`: Specifies if the category is user-defined.
* `type`: Type of the category.
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
        r"""Updates the specified category.
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
        r"""Deletes a category.
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


