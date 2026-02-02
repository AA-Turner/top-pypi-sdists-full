"""Marshmallow Schema for AssistantCommand."""
import json
from marshmallow import Schema, fields
from ..WorkbookBlockComment.schemas import (
    WorkbookBlockCommentResourceSchema,
)


class WorkbookWorkflowBlockDataField(fields.Field):
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


class WorkbookWorkflowBlockResourceSchema(Schema):
    """Class for AssistantCommandResource schema"""

    id = fields.Integer(dump_only=True)
    workflow_id = fields.Integer(required=True)
    sequence_number = fields.Integer(required=True)
    block_type = fields.String(required=True)
    data = WorkbookWorkflowBlockDataField(required=True, allow_none=True)
    status = fields.String(required=True)
    rendered = fields.Boolean(allow_none=True)
    is_completed = fields.Boolean(allow_none=True)
    is_deleted = fields.Boolean(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
