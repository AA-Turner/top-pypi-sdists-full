r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AggregateWarning", "AggregateWarningSchema"]
__pdoc__ = {
    "AggregateWarningSchema.resource": False,
    "AggregateWarningSchema.opts": False,
    "AggregateWarning": False,
}


class AggregateWarningSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AggregateWarning object"""

    action = marshmallow_fields.Nested("netapp_ontap.models.aggregate_warning_action.AggregateWarningActionSchema", unknown=EXCLUDE, data_key="action", allow_none=True)
    r""" The action field of the aggregate_warning. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the entity that returns the warning. """

    warning = marshmallow_fields.Nested("netapp_ontap.models.aggregate_warning_warning.AggregateWarningWarningSchema", unknown=EXCLUDE, data_key="warning", allow_none=True)
    r""" The warning field of the aggregate_warning. """

    @property
    def resource(self):
        return AggregateWarning

    gettable_fields = [
        "action",
        "name",
        "warning",
    ]
    """action,name,warning,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class AggregateWarning(Resource):

    _schema = AggregateWarningSchema
