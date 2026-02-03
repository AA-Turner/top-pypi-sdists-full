r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DatacollectionRag", "DatacollectionRagSchema"]
__pdoc__ = {
    "DatacollectionRagSchema.resource": False,
    "DatacollectionRagSchema.opts": False,
    "DatacollectionRag": False,
}

class DatacollectionRagSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DatacollectionRag object"""

    url = marshmallow_fields.Str(data_key="url", allow_none=True)
    r""" The URL for the Retrieval-Augmented Generation (RAG) endpoint.

Example: https://1.2.3.4/api/data-engine/workspaces/02c9e252-41be-11e9-81d5-00a0986138f7/data-collections/123e4567-e89b-12d3-a456-426614174000/search """

    @property
    def resource(self):
        return DatacollectionRag

    gettable_fields = [
        "url",
    ]
    """url,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DatacollectionRag(Resource):

    _schema = DatacollectionRagSchema
