r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataSourcesAggregationsInner", "DataSourcesAggregationsInnerSchema"]
__pdoc__ = {
    "DataSourcesAggregationsInnerSchema.resource": False,
    "DataSourcesAggregationsInnerSchema.opts": False,
    "DataSourcesAggregationsInner": False,
}

class DataSourcesAggregationsInnerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataSourcesAggregationsInner object"""

    entity_count = Size(data_key="entity_count", allow_none=True)
    r""" Number of entities in the data_source.

Example: 20 """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the data_source.

Example: data_source_1 """

    sensitive_entity_count = Size(data_key="sensitive_entity_count", allow_none=True)
    r""" Number of sensitive entities in the data_source.

Example: 100 """

    sensitive_entity_percent = Size(data_key="sensitive_entity_percent", allow_none=True)
    r""" Percentage of sensitive entities in the data_source.

Example: 23 """

    space_used = Size(data_key="space_used", allow_none=True)
    r""" Total utilized size of the data_source.

Example: 2066541 """

    top_document_categories = marshmallow_fields.Str(data_key="top_document_categories", allow_none=True)
    r""" Top document categories of the data_source.

Example: General Privacy, Financial Documents """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" UUID of the data_source.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return DataSourcesAggregationsInner

    gettable_fields = [
        "entity_count",
        "name",
        "sensitive_entity_count",
        "sensitive_entity_percent",
        "space_used",
        "top_document_categories",
        "uuid",
    ]
    """entity_count,name,sensitive_entity_count,sensitive_entity_percent,space_used,top_document_categories,uuid,"""

    patchable_fields = [
        "entity_count",
        "name",
        "sensitive_entity_count",
        "sensitive_entity_percent",
        "space_used",
        "top_document_categories",
        "uuid",
    ]
    """entity_count,name,sensitive_entity_count,sensitive_entity_percent,space_used,top_document_categories,uuid,"""

    postable_fields = [
        "entity_count",
        "name",
        "sensitive_entity_count",
        "sensitive_entity_percent",
        "space_used",
        "top_document_categories",
        "uuid",
    ]
    """entity_count,name,sensitive_entity_count,sensitive_entity_percent,space_used,top_document_categories,uuid,"""


class DataSourcesAggregationsInner(Resource):

    _schema = DataSourcesAggregationsInnerSchema
