r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["EmsActionParameterValidationErrorMessageArguments", "EmsActionParameterValidationErrorMessageArgumentsSchema"]
__pdoc__ = {
    "EmsActionParameterValidationErrorMessageArgumentsSchema.resource": False,
    "EmsActionParameterValidationErrorMessageArgumentsSchema.opts": False,
    "EmsActionParameterValidationErrorMessageArguments": False,
}


class EmsActionParameterValidationErrorMessageArgumentsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsActionParameterValidationErrorMessageArguments object"""

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Argument code """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Message argument """

    @property
    def resource(self):
        return EmsActionParameterValidationErrorMessageArguments

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


class EmsActionParameterValidationErrorMessageArguments(Resource):

    _schema = EmsActionParameterValidationErrorMessageArgumentsSchema
