r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["TopEnforcedGuardrailsInner", "TopEnforcedGuardrailsInnerSchema"]
__pdoc__ = {
    "TopEnforcedGuardrailsInnerSchema.resource": False,
    "TopEnforcedGuardrailsInnerSchema.opts": False,
    "TopEnforcedGuardrailsInner": False,
}

class TopEnforcedGuardrailsInnerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TopEnforcedGuardrailsInner object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the guardrail.

Example: Customer Data Protection """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" UUID of the guardrail.

Example: 02c9e252-41be-11e9-81d5-00a0986138f7 """

    @property
    def resource(self):
        return TopEnforcedGuardrailsInner

    gettable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    patchable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class TopEnforcedGuardrailsInner(Resource):

    _schema = TopEnforcedGuardrailsInnerSchema
