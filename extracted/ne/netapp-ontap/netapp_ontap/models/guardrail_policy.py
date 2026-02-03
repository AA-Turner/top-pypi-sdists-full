r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["GuardrailPolicy", "GuardrailPolicySchema"]
__pdoc__ = {
    "GuardrailPolicySchema.resource": False,
    "GuardrailPolicySchema.opts": False,
    "GuardrailPolicy": False,
}

class GuardrailPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the GuardrailPolicy object"""

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" UUID of the guardrail policy.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return GuardrailPolicy

    gettable_fields = [
        "uuid",
    ]
    """uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class GuardrailPolicy(Resource):

    _schema = GuardrailPolicySchema
