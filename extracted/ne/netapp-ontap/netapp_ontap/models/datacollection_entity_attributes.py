r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DatacollectionEntityAttributes", "DatacollectionEntityAttributesSchema"]
__pdoc__ = {
    "DatacollectionEntityAttributesSchema.resource": False,
    "DatacollectionEntityAttributesSchema.opts": False,
    "DatacollectionEntityAttributes": False,
}

class DatacollectionEntityAttributesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DatacollectionEntityAttributes object"""

    content = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_engine_entity_attributes_extended", "DataEngineEntityAttributesExtendedSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="content",
                allow_none=True
                )
    r""" The content field of the datacollection_entity_attributes. """

    custom = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_engine_entity_attributes_extended", "DataEngineEntityAttributesExtendedSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="custom",
                allow_none=True
                )
    r""" The custom field of the datacollection_entity_attributes. """

    extended = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_engine_entity_attributes_extended", "DataEngineEntityAttributesExtendedSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="extended",
                allow_none=True
                )
    r""" The extended field of the datacollection_entity_attributes. """

    system = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_engine_entity_attributes_extended", "DataEngineEntityAttributesExtendedSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="system",
                allow_none=True
                )
    r""" The system field of the datacollection_entity_attributes. """

    @property
    def resource(self):
        return DatacollectionEntityAttributes

    gettable_fields = [
        "content",
        "custom",
        "extended",
        "system",
    ]
    """content,custom,extended,system,"""

    patchable_fields = [
        "content",
        "custom",
        "extended",
        "system",
    ]
    """content,custom,extended,system,"""

    postable_fields = [
        "content",
        "custom",
        "extended",
        "system",
    ]
    """content,custom,extended,system,"""


class DatacollectionEntityAttributes(Resource):

    _schema = DatacollectionEntityAttributesSchema
