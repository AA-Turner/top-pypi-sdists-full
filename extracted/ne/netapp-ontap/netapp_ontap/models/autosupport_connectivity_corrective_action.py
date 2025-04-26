r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AutosupportConnectivityCorrectiveAction", "AutosupportConnectivityCorrectiveActionSchema"]
__pdoc__ = {
    "AutosupportConnectivityCorrectiveActionSchema.resource": False,
    "AutosupportConnectivityCorrectiveActionSchema.opts": False,
    "AutosupportConnectivityCorrectiveAction": False,
}


class AutosupportConnectivityCorrectiveActionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AutosupportConnectivityCorrectiveAction object"""

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Corrective action code

Example: 53149746 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Corrective action message. The corrective action might contain commands which needs to be executed on the ONTAP CLI.

Example: Check the hostname of the SMTP server """

    @property
    def resource(self):
        return AutosupportConnectivityCorrectiveAction

    gettable_fields = [
        "code",
        "message",
    ]
    """code,message,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class AutosupportConnectivityCorrectiveAction(Resource):

    _schema = AutosupportConnectivityCorrectiveActionSchema
