r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["EmsEventActionParametersHelpArguments", "EmsEventActionParametersHelpArgumentsSchema"]
__pdoc__ = {
    "EmsEventActionParametersHelpArgumentsSchema.resource": False,
    "EmsEventActionParametersHelpArgumentsSchema.opts": False,
    "EmsEventActionParametersHelpArguments": False,
}


class EmsEventActionParametersHelpArgumentsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsEventActionParametersHelpArguments object"""

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Argument code """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Message argument """

    @property
    def resource(self):
        return EmsEventActionParametersHelpArguments

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


class EmsEventActionParametersHelpArguments(Resource):

    _schema = EmsEventActionParametersHelpArgumentsSchema
