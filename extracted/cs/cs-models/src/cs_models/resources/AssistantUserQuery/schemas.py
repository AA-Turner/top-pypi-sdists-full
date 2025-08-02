import json
from marshmallow import Schema, fields
from .models import AssistantUserQueryStatusEnum
from ..AssistantCommand.schemas import (
    AssistantCommandResourceSchema,
)


class AssistantUserQueryFilterField(fields.Field):
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


class AssistantUserQueryResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    session_id = fields.Integer(required=True)
    value = fields.String(required=True)
    filter = AssistantUserQueryFilterField(allow_none=True)
    type = fields.String(required=True)
    status = fields.Enum(AssistantUserQueryStatusEnum, required=True, by_value=True)
    commands = fields.Nested(
        AssistantCommandResourceSchema(exclude=("user_query_id",)),
        many=True,
        dump_only=True,
    )
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
