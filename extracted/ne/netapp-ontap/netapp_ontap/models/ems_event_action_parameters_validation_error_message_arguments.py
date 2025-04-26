r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["EmsEventActionParametersValidationErrorMessageArguments", "EmsEventActionParametersValidationErrorMessageArgumentsSchema"]
__pdoc__ = {
    "EmsEventActionParametersValidationErrorMessageArgumentsSchema.resource": False,
    "EmsEventActionParametersValidationErrorMessageArgumentsSchema.opts": False,
    "EmsEventActionParametersValidationErrorMessageArguments": False,
}


class EmsEventActionParametersValidationErrorMessageArgumentsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsEventActionParametersValidationErrorMessageArguments object"""

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Argument code """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Message argument """

    @property
    def resource(self):
        return EmsEventActionParametersValidationErrorMessageArguments

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


class EmsEventActionParametersValidationErrorMessageArguments(Resource):

    _schema = EmsEventActionParametersValidationErrorMessageArgumentsSchema
