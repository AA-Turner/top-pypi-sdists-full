r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DatacollectionSearch", "DatacollectionSearchSchema"]
__pdoc__ = {
    "DatacollectionSearchSchema.resource": False,
    "DatacollectionSearchSchema.opts": False,
    "DatacollectionSearch": False,
}

class DatacollectionSearchSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DatacollectionSearch object"""

    chunk = marshmallow_fields.Str(data_key="chunk", allow_none=True)
    r""" The content of the chunk. """

    entity = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.datacollection_entity", "DatacollectionEntitySchema"),
                unknown=EXCLUDE,
                data_key="entity",
                allow_none=True
            )
    r""" The entity field of the datacollection_search. """

    index = Size(data_key="index", allow_none=True)
    r""" The index of the chunk in the result.

Example: 1 """

    score = marshmallow_fields.Dict(data_key="score", allow_none=True)
    r""" Similarity score of the chunk with the prompt that was searched for.

Example: 0.9 """

    @property
    def resource(self):
        return DatacollectionSearch

    gettable_fields = [
        "chunk",
        "entity.links",
        "entity.uuid",
        "index",
        "score",
    ]
    """chunk,entity.links,entity.uuid,index,score,"""

    patchable_fields = [
        "entity.links",
    ]
    """entity.links,"""

    postable_fields = [
        "entity.links",
    ]
    """entity.links,"""


class DatacollectionSearch(Resource):

    _schema = DatacollectionSearchSchema
