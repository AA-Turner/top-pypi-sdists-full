"""Marshmallow Schema for AssistantCommand."""
import json

from marshmallow import Schema, fields

from ..AssistantCommand.models import (
    AssistantCommandModel,
    AssistantCommandStatusEnum,
    AssistantCommandTypeEnum,
)


class AssistantCommandResultField(fields.Field):
    """Field that stores result for the Assistant command."""

    def _serialize(self, value, attr, obj, **kwargs):
        """
        In the DB, the `result` field is a text field. We persist
        data by performing the following:

        AssistantCommandModel(
            ...
            result=json.dumps({...}),
        )

        So here we need to perform the inverse operation (i.e `json.loads(..)`)
        """
        if value is None:
            return None
        return json.loads(value)

    def _deserialize(self, value, attr, data, **kwargs):
        """
        In the DB, the `result` field is a text field. We persist
        data by performing the following:



        AssistantCommandModel(
            ***AssistantCommandResourceSchema().load({
                ...
                "result": [{"some_key": 1}, {"some_key": 2}],
            }),
        )
        """
        if value is None:
            return None
        return json.dumps(value)


class AssistantCommandLLMResultField(fields.Field):
    """Field that stores result for the Assistant command."""

    def _serialize(self, value, attr, obj, **kwargs):
        """
        In the DB, the `result` field is a text field. We persist
        data by performing the following:

        AssistantCommandModel(
            ...
            result=json.dumps({...}),
        )

        So here we need to perform the inverse operation (i.e `json.loads(..)`)
        """
        if value is None:
            return None
        return json.loads(value)

    def _deserialize(self, value, attr, data, **kwargs):
        """
        In the DB, the `result` field is a text field. We persist
        data by performing the following:



        AssistantCommandModel(
            ***AssistantCommandResourceSchema().load({
                ...
                "result": [{"some_key": 1}, {"some_key": 2}],
            }),
        )
        """
        if value is None:
            return None
        return json.dumps(value)


class AssistantCommandResourceSchema(Schema):
    """Class for AssistantCommandResource schema"""

    id = fields.Integer(dump_only=True)
    user_query_id = fields.Integer(required=True)
    step_number = fields.Integer(required=True)
    type = fields.Enum(AssistantCommandTypeEnum, required=True, by_value=True)
    label = fields.String(required=True)
    status = fields.Enum(
        AssistantCommandStatusEnum, required=True, by_value=True
    )
    higher_neighbour_ids = fields.Method(
        serialize="serialize_higher_neighbours"
    )
    lower_neighbour_ids = fields.Method(serialize="serialize_lower_neighbours")
    result = AssistantCommandResultField(required=True, allow_none=True)
    llm_result = AssistantCommandLLMResultField(allow_none=True)
    error = fields.String(allow_none=True)
    internal_doc = fields.Boolean(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    def serialize_higher_neighbours(self, obj: AssistantCommandModel):
        """
        https://marshmallow.readthedocs.io/en/stable/custom_fields.html#adding-context-to-method-and-function-fields
        """
        return [x.higher_id for x in obj.lower_edges]

    def serialize_lower_neighbours(self, obj: AssistantCommandModel):
        """
        https://marshmallow.readthedocs.io/en/stable/custom_fields.html#adding-context-to-method-and-function-fields
        """
        return [x.lower_id for x in obj.higher_edges]
