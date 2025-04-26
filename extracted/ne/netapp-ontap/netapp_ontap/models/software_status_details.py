r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SoftwareStatusDetails", "SoftwareStatusDetailsSchema"]
__pdoc__ = {
    "SoftwareStatusDetailsSchema.resource": False,
    "SoftwareStatusDetailsSchema.opts": False,
    "SoftwareStatusDetails": False,
}


class SoftwareStatusDetailsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SoftwareStatusDetails object"""

    action = marshmallow_fields.Nested("netapp_ontap.models.software_status_details_reference_action.SoftwareStatusDetailsReferenceActionSchema", unknown=EXCLUDE, data_key="action", allow_none=True)
    r""" The action field of the software_status_details. """

    end_time = ImpreciseDateTime(data_key="end_time", allow_none=True)
    r""" End time for each status phase.

Example: 2019-02-02T19:00:00.000+0000 """

    issue = marshmallow_fields.Nested("netapp_ontap.models.software_status_details_reference_issue.SoftwareStatusDetailsReferenceIssueSchema", unknown=EXCLUDE, data_key="issue", allow_none=True)
    r""" The issue field of the software_status_details. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the phase to be retrieved for status details.

Example: initialize """

    node = marshmallow_fields.Nested("netapp_ontap.models.software_status_details_reference_node.SoftwareStatusDetailsReferenceNodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the software_status_details. """

    start_time = ImpreciseDateTime(data_key="start_time", allow_none=True)
    r""" Start time for each status phase.

Example: 2019-02-02T19:00:00.000+0000 """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Status of the phase

Valid choices:

* in_progress
* waiting
* paused_by_user
* paused_on_error
* completed
* canceled
* failed
* pause_pending
* cancel_pending """

    @property
    def resource(self):
        return SoftwareStatusDetails

    gettable_fields = [
        "action",
        "end_time",
        "issue",
        "name",
        "node",
        "start_time",
        "state",
    ]
    """action,end_time,issue,name,node,start_time,state,"""

    patchable_fields = [
        "node",
    ]
    """node,"""

    postable_fields = [
        "node",
    ]
    """node,"""


class SoftwareStatusDetails(Resource):

    _schema = SoftwareStatusDetailsSchema
