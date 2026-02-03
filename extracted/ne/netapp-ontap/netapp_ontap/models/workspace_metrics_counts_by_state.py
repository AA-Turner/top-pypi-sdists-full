r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["WorkspaceMetricsCountsByState", "WorkspaceMetricsCountsByStateSchema"]
__pdoc__ = {
    "WorkspaceMetricsCountsByStateSchema.resource": False,
    "WorkspaceMetricsCountsByStateSchema.opts": False,
    "WorkspaceMetricsCountsByState": False,
}

class WorkspaceMetricsCountsByStateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WorkspaceMetricsCountsByState object"""

    count = Size(data_key="count", allow_none=True)
    r""" The number of workspaces in this state.

Example: 50 """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" State of the workspace:

* <i>processing</i> - The workspace is being processed after creation.
* <i>ready</i> - The workspace is ready for use.
* <i>failed</i> - The workspace has a failure.
* <i>outdated</i> - The workspace is outdated.
* <i>deleted</i> - The workspace has been marked for deletion.


Valid choices:

* processing
* ready
* failed
* outdated
* deleted """

    @property
    def resource(self):
        return WorkspaceMetricsCountsByState

    gettable_fields = [
        "count",
        "state",
    ]
    """count,state,"""

    patchable_fields = [
        "count",
        "state",
    ]
    """count,state,"""

    postable_fields = [
        "count",
        "state",
    ]
    """count,state,"""


class WorkspaceMetricsCountsByState(Resource):

    _schema = WorkspaceMetricsCountsByStateSchema
