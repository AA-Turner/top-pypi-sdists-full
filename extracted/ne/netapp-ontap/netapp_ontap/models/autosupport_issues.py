r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AutosupportIssues", "AutosupportIssuesSchema"]
__pdoc__ = {
    "AutosupportIssuesSchema.resource": False,
    "AutosupportIssuesSchema.opts": False,
    "AutosupportIssues": False,
}


class AutosupportIssuesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AutosupportIssues object"""

    component = marshmallow_fields.Str(data_key="component", allow_none=True)
    r""" The name of the component where the issue occurred.


Valid choices:

* https_put_destination
* https_post_destination
* mail_server
* ondemand_server """

    corrective_action = marshmallow_fields.Nested("netapp_ontap.models.autosupport_connectivity_corrective_action.AutosupportConnectivityCorrectiveActionSchema", unknown=EXCLUDE, data_key="corrective_action", allow_none=True)
    r""" The corrective_action field of the autosupport_issues. """

    destination = marshmallow_fields.Str(data_key="destination", allow_none=True)
    r""" The HTTPS/SMTP/AOD AutoSupport Destination.

Example: mailhost1.example.com """

    issue = marshmallow_fields.Nested("netapp_ontap.models.autosupport_connectivity_issue.AutosupportConnectivityIssueSchema", unknown=EXCLUDE, data_key="issue", allow_none=True)
    r""" The issue field of the autosupport_issues. """

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the autosupport_issues. """

    @property
    def resource(self):
        return AutosupportIssues

    gettable_fields = [
        "component",
        "corrective_action",
        "destination",
        "issue",
        "node.links",
        "node.name",
        "node.uuid",
    ]
    """component,corrective_action,destination,issue,node.links,node.name,node.uuid,"""

    patchable_fields = [
        "component",
        "corrective_action",
        "issue",
    ]
    """component,corrective_action,issue,"""

    postable_fields = [
        "component",
        "corrective_action",
        "issue",
    ]
    """component,corrective_action,issue,"""


class AutosupportIssues(Resource):

    _schema = AutosupportIssuesSchema
