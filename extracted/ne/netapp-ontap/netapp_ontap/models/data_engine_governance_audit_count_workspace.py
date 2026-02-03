r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineGovernanceAuditCountWorkspace", "DataEngineGovernanceAuditCountWorkspaceSchema"]
__pdoc__ = {
    "DataEngineGovernanceAuditCountWorkspaceSchema.resource": False,
    "DataEngineGovernanceAuditCountWorkspaceSchema.opts": False,
    "DataEngineGovernanceAuditCountWorkspace": False,
}

class DataEngineGovernanceAuditCountWorkspaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineGovernanceAuditCountWorkspace object"""

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" UUID of the workspace.

Example: 02c9e252-41be-11e9-81d5-00a0986138f7 """

    @property
    def resource(self):
        return DataEngineGovernanceAuditCountWorkspace

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


class DataEngineGovernanceAuditCountWorkspace(Resource):

    _schema = DataEngineGovernanceAuditCountWorkspaceSchema
