r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["EmsActionParameterTitleArguments", "EmsActionParameterTitleArgumentsSchema"]
__pdoc__ = {
    "EmsActionParameterTitleArgumentsSchema.resource": False,
    "EmsActionParameterTitleArgumentsSchema.opts": False,
    "EmsActionParameterTitleArguments": False,
}


class EmsActionParameterTitleArgumentsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsActionParameterTitleArguments object"""

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Argument code """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Message argument """

    @property
    def resource(self):
        return EmsActionParameterTitleArguments

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


class EmsActionParameterTitleArguments(Resource):

    _schema = EmsActionParameterTitleArgumentsSchema
