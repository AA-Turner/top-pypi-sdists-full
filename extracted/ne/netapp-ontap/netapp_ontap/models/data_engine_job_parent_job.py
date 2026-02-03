r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineJobParentJob", "DataEngineJobParentJobSchema"]
__pdoc__ = {
    "DataEngineJobParentJobSchema.resource": False,
    "DataEngineJobParentJobSchema.opts": False,
    "DataEngineJobParentJob": False,
}

class DataEngineJobParentJobSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineJobParentJob object"""

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the parent job.

Example: 123e4567-e89b-12d3-a456-426614173000 """

    @property
    def resource(self):
        return DataEngineJobParentJob

    gettable_fields = [
        "uuid",
    ]
    """uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DataEngineJobParentJob(Resource):

    _schema = DataEngineJobParentJobSchema
