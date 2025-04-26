r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["EmsUiMessage", "EmsUiMessageSchema"]
__pdoc__ = {
    "EmsUiMessageSchema.resource": False,
    "EmsUiMessageSchema.opts": False,
    "EmsUiMessage": False,
}


class EmsUiMessageSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsUiMessage object"""

    arguments = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.ems_event_action_title_arguments.EmsEventActionTitleArgumentsSchema", unknown=EXCLUDE, allow_none=True), data_key="arguments", allow_none=True)
    r""" Message arguments """

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Unique message code.

Example: 4 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" User message.

Example: entry doesn't exist """

    @property
    def resource(self):
        return EmsUiMessage

    gettable_fields = [
        "arguments",
        "code",
        "message",
    ]
    """arguments,code,message,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class EmsUiMessage(Resource):

    _schema = EmsUiMessageSchema
