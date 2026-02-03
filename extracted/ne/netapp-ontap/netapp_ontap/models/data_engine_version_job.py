r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineVersionJob", "DataEngineVersionJobSchema"]
__pdoc__ = {
    "DataEngineVersionJobSchema.resource": False,
    "DataEngineVersionJobSchema.opts": False,
    "DataEngineVersionJob": False,
}

class DataEngineVersionJobSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineVersionJob object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                unknown=EXCLUDE,
                data_key="_links",
                allow_none=True
            )
    r""" The links field of the data_engine_version_job. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state of the data engine job:

* <i>queued</i> - The job is queued for execution.
* <i>running</i> - The job is currently in execution.
* <i>success</i> - The job has been completed successfully.
* <i>failure</i> - The job has failed.


Valid choices:

* queued
* running
* success
* failure """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the job.

Example: 123e4567-e89b-12d3-a456-426614174000 """

    @property
    def resource(self):
        return DataEngineVersionJob

    gettable_fields = [
        "links",
        "state",
        "uuid",
    ]
    """links,state,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DataEngineVersionJob(Resource):

    _schema = DataEngineVersionJobSchema
