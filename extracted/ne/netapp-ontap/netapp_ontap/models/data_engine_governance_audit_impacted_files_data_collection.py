r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineGovernanceAuditImpactedFilesDataCollection", "DataEngineGovernanceAuditImpactedFilesDataCollectionSchema"]
__pdoc__ = {
    "DataEngineGovernanceAuditImpactedFilesDataCollectionSchema.resource": False,
    "DataEngineGovernanceAuditImpactedFilesDataCollectionSchema.opts": False,
    "DataEngineGovernanceAuditImpactedFilesDataCollection": False,
}

class DataEngineGovernanceAuditImpactedFilesDataCollectionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineGovernanceAuditImpactedFilesDataCollection object"""

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" UUID of the data collection associated with the file.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return DataEngineGovernanceAuditImpactedFilesDataCollection

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


class DataEngineGovernanceAuditImpactedFilesDataCollection(Resource):

    _schema = DataEngineGovernanceAuditImpactedFilesDataCollectionSchema
