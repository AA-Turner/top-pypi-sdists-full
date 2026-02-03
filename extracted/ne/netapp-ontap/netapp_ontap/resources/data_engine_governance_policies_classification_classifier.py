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


__all__ = ["DataEngineGovernancePoliciesClassificationClassifier", "DataEngineGovernancePoliciesClassificationClassifierSchema"]
__pdoc__ = {
    "DataEngineGovernancePoliciesClassificationClassifierSchema.resource": False,
    "DataEngineGovernancePoliciesClassificationClassifierSchema.opts": False,
}

class DataEngineGovernancePoliciesClassificationClassifierSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineGovernancePoliciesClassificationClassifier object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the data_engine_governance_policies_classification_classifier."""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" The timestamp indicating when the classifier was created.

Example: 2018-06-04T19:00:00.000+0000"""

    custom = marshmallow_fields.Boolean(
        data_key="custom",
        allow_none=True,
    )
    r""" Indicates if the classifier is custom or predefined.

Example: false"""

    description = marshmallow_fields.Str(
        data_key="description",
        allow_none=True,
    )
    r""" Description of the classifier.

Example: classifier for data subjects(i.e., person names)"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the classifier.

Example: data subjects classifier"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['enabled', 'disabled', 'simulate']),
        allow_none=True,
    )
    r""" State of the classifier. Possible values are:

* <i>enabled</i>: Classifier is enabled.
* <i>disabled</i>: Classifier is disabled.
* <i>simulate</i>: Classifier is in simulation mode.


Valid choices:

* enabled
* disabled
* simulate"""

    tag = marshmallow_fields.Str(
        data_key="tag",
        allow_none=True,
    )
    r""" Tag associated with the classifier.

Example: CLS_ENTD00000"""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['data', 'document']),
        allow_none=True,
    )
    r""" Specifies the type of classifier. Possible values are:

* <i>data</i>: Classifier for data entities.
* <i>document</i>: Classifier for document entities.


Valid choices:

* data
* document"""

    update_time = ImpreciseDateTime(
        data_key="update_time",
        allow_none=True,
    )
    r""" The timestamp indicating when the classifier was last updated.

Example: 2018-06-04T19:00:00.000+0000"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier of the classifier.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return DataEngineGovernancePoliciesClassificationClassifier

    gettable_fields = [
        "links",
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
    """links,create_time,custom,description,name,state,tag,type,update_time,uuid,"""

    patchable_fields = [
        "custom",
        "description",
        "name",
        "state",
        "tag",
        "type",
    ]
    """custom,description,name,state,tag,type,"""

    postable_fields = [
        "custom",
        "description",
        "name",
        "state",
        "tag",
        "type",
    ]
    """custom,description,name,state,tag,type,"""

class DataEngineGovernancePoliciesClassificationClassifier(Resource):
    r""" Defines the structure of a classifier. """

    _schema = DataEngineGovernancePoliciesClassificationClassifierSchema
    _path = "/api/data-engine/governance/policies/classification/classifiers"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of classifiers.
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
        """Returns a count of all DataEngineGovernancePoliciesClassificationClassifier resources that match the provided query"""
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
        """Returns a list of RawResources that represent DataEngineGovernancePoliciesClassificationClassifier resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["DataEngineGovernancePoliciesClassificationClassifier"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the specified classifier.
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of classifiers.
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the details of the specified classifier.
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
        r"""Updates the specified classifier.
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



