r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineGovernanceFilePreviewFileContentRequestFile", "DataEngineGovernanceFilePreviewFileContentRequestFileSchema"]
__pdoc__ = {
    "DataEngineGovernanceFilePreviewFileContentRequestFileSchema.resource": False,
    "DataEngineGovernanceFilePreviewFileContentRequestFileSchema.opts": False,
    "DataEngineGovernanceFilePreviewFileContentRequestFile": False,
}

class DataEngineGovernanceFilePreviewFileContentRequestFileSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineGovernanceFilePreviewFileContentRequestFile object"""

    format = marshmallow_fields.Str(data_key="format", allow_none=True)
    r""" Format of the file.

Valid choices:

* pdf
* docx
* txt
* csv
* json
* map
* js
* doc
* xlsx
* css
* xls """

    path = marshmallow_fields.Str(data_key="path", allow_none=True)
    r""" Path to the downloaded file. This is present when the job is completed.

Example: /downloaded_folder/file1.pdf """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" UUID of the entity.

Example: 12c9e267-23be-22e9-81d5-00xx986138f7 """

    @property
    def resource(self):
        return DataEngineGovernanceFilePreviewFileContentRequestFile

    gettable_fields = [
        "format",
        "path",
        "uuid",
    ]
    """format,path,uuid,"""

    patchable_fields = [
        "format",
        "path",
        "uuid",
    ]
    """format,path,uuid,"""

    postable_fields = [
        "format",
        "path",
        "uuid",
    ]
    """format,path,uuid,"""


class DataEngineGovernanceFilePreviewFileContentRequestFile(Resource):

    _schema = DataEngineGovernanceFilePreviewFileContentRequestFileSchema
