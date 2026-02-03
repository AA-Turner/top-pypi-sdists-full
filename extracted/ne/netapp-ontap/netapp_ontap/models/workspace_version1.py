r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["WorkspaceVersion1", "WorkspaceVersion1Schema"]
__pdoc__ = {
    "WorkspaceVersion1Schema.resource": False,
    "WorkspaceVersion1Schema.opts": False,
    "WorkspaceVersion1": False,
}

class WorkspaceVersion1Schema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WorkspaceVersion1 object"""

    current = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.datacollection_version1_current", "DatacollectionVersion1CurrentSchema"),
                unknown=EXCLUDE,
                data_key="current",
                allow_none=True
            )
    r""" The current field of the workspace_version1. """

    job = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_version_job", "DataEngineVersionJobSchema"),
                unknown=EXCLUDE,
                data_key="job",
                allow_none=True
            )
    r""" The version job details. """

    next = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.datacollection_version1_next", "DatacollectionVersion1NextSchema"),
                unknown=EXCLUDE,
                data_key="next",
                allow_none=True
            )
    r""" The next field of the workspace_version1. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the version.

Example: 123e4567-e89b-12d3-a456-426614174000 """

    @property
    def resource(self):
        return WorkspaceVersion1

    gettable_fields = [
        "current",
        "job",
        "next",
        "uuid",
    ]
    """current,job,next,uuid,"""

    patchable_fields = [
        "current",
        "next",
        "uuid",
    ]
    """current,next,uuid,"""

    postable_fields = [
        "current",
        "next",
        "uuid",
    ]
    """current,next,uuid,"""


class WorkspaceVersion1(Resource):

    _schema = WorkspaceVersion1Schema
