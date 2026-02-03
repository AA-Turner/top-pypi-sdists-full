r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineEntityErrors", "DataEngineEntityErrorsSchema"]
__pdoc__ = {
    "DataEngineEntityErrorsSchema.resource": False,
    "DataEngineEntityErrorsSchema.opts": False,
    "DataEngineEntityErrors": False,
}

class DataEngineEntityErrorsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineEntityErrors object"""

    error = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_common_error", "DcnCommonErrorSchema"),
                unknown=EXCLUDE,
                data_key="error",
                allow_none=True
            )
    r""" DCN ONTAP related error information. """

    @property
    def resource(self):
        return DataEngineEntityErrors

    gettable_fields = [
        "error",
    ]
    """error,"""

    patchable_fields = [
        "error",
    ]
    """error,"""

    postable_fields = [
        "error",
    ]
    """error,"""


class DataEngineEntityErrors(Resource):

    _schema = DataEngineEntityErrorsSchema
