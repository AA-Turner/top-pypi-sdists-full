r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DcnCommonError", "DcnCommonErrorSchema"]
__pdoc__ = {
    "DcnCommonErrorSchema.resource": False,
    "DcnCommonErrorSchema.opts": False,
    "DcnCommonError": False,
}

class DcnCommonErrorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnCommonError object"""

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Error code. """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Error message. """

    target = marshmallow_fields.Str(data_key="target", allow_none=True)
    r""" The target parameter that caused the error.

Example: workspace """

    @property
    def resource(self):
        return DcnCommonError

    gettable_fields = [
        "code",
        "message",
        "target",
    ]
    """code,message,target,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DcnCommonError(Resource):

    _schema = DcnCommonErrorSchema
