r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineGovernanceFilePreviewFileContent", "DataEngineGovernanceFilePreviewFileContentSchema"]
__pdoc__ = {
    "DataEngineGovernanceFilePreviewFileContentSchema.resource": False,
    "DataEngineGovernanceFilePreviewFileContentSchema.opts": False,
    "DataEngineGovernanceFilePreviewFileContent": False,
}

class DataEngineGovernanceFilePreviewFileContentSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineGovernanceFilePreviewFileContent object"""

    data = marshmallow_fields.Str(data_key="data", allow_none=True)
    r""" Base64 encoded anonymized byte/octet stream from the first five pages.

Example: encoded response """

    @property
    def resource(self):
        return DataEngineGovernanceFilePreviewFileContent

    gettable_fields = [
        "data",
    ]
    """data,"""

    patchable_fields = [
        "data",
    ]
    """data,"""

    postable_fields = [
        "data",
    ]
    """data,"""


class DataEngineGovernanceFilePreviewFileContent(Resource):

    _schema = DataEngineGovernanceFilePreviewFileContentSchema
