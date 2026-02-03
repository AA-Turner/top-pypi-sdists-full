r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineGovernanceAuditImpactedFilesFile", "DataEngineGovernanceAuditImpactedFilesFileSchema"]
__pdoc__ = {
    "DataEngineGovernanceAuditImpactedFilesFileSchema.resource": False,
    "DataEngineGovernanceAuditImpactedFilesFileSchema.opts": False,
    "DataEngineGovernanceAuditImpactedFilesFile": False,
}

class DataEngineGovernanceAuditImpactedFilesFileSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineGovernanceAuditImpactedFilesFile object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the file.

Example: example_file.txt """

    size = Size(data_key="size", allow_none=True)
    r""" Size of the file in bytes.

Example: 1024 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" UUID of the file.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return DataEngineGovernanceAuditImpactedFilesFile

    gettable_fields = [
        "name",
        "size",
        "uuid",
    ]
    """name,size,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DataEngineGovernanceAuditImpactedFilesFile(Resource):

    _schema = DataEngineGovernanceAuditImpactedFilesFileSchema
