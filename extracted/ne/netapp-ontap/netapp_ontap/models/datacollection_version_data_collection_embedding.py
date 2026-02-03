r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DatacollectionVersionDataCollectionEmbedding", "DatacollectionVersionDataCollectionEmbeddingSchema"]
__pdoc__ = {
    "DatacollectionVersionDataCollectionEmbeddingSchema.resource": False,
    "DatacollectionVersionDataCollectionEmbeddingSchema.opts": False,
    "DatacollectionVersionDataCollectionEmbedding": False,
}

class DatacollectionVersionDataCollectionEmbeddingSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DatacollectionVersionDataCollectionEmbedding object"""

    chunk_size = Size(data_key="chunk_size", allow_none=True)
    r""" The chunk size value in the range (3..1536)

Example: 1536 """

    chunk_type = marshmallow_fields.Str(data_key="chunk_type", allow_none=True)
    r""" The type of chunking.

Valid choices:

* sentence
* paragraph
* full_file
* semantic
* recursive
* fixed_size """

    dimension = Size(data_key="dimension", allow_none=True)
    r""" The dimension of vectorization.

Example: 1024 """

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Indicates whether vectorization is enabled.

Example: true """

    quantization = marshmallow_fields.Str(data_key="quantization", allow_none=True)
    r""" The vector quantization value.

Valid choices:

* fp32
* fp16
* fp8
* uint8 """

    re_rank = marshmallow_fields.Boolean(data_key="re_rank", allow_none=True)
    r""" Indicates whether re_rank is enabled

Example: true """

    @property
    def resource(self):
        return DatacollectionVersionDataCollectionEmbedding

    gettable_fields = [
        "chunk_size",
        "chunk_type",
        "dimension",
        "enabled",
        "quantization",
        "re_rank",
    ]
    """chunk_size,chunk_type,dimension,enabled,quantization,re_rank,"""

    patchable_fields = [
        "chunk_size",
        "chunk_type",
        "dimension",
        "enabled",
        "quantization",
        "re_rank",
    ]
    """chunk_size,chunk_type,dimension,enabled,quantization,re_rank,"""

    postable_fields = [
        "chunk_size",
        "chunk_type",
        "dimension",
        "enabled",
        "quantization",
        "re_rank",
    ]
    """chunk_size,chunk_type,dimension,enabled,quantization,re_rank,"""


class DatacollectionVersionDataCollectionEmbedding(Resource):

    _schema = DatacollectionVersionDataCollectionEmbeddingSchema
