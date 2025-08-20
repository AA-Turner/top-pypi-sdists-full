"""Marshmallow Schema for AssistantCommand."""
import json
from marshmallow import Schema, fields
from ..WorkbookBlockComment.schemas import (
    WorkbookBlockCommentResourceSchema,
)


class WorkbookBlockDataField(fields.Field):
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


class WorkbookBlockResourceSchema(Schema):
    """Class for AssistantCommandResource schema"""

    id = fields.Integer(dump_only=True)
    workbook_id = fields.Integer(required=True)
    block_uid = fields.String(required=True)
    sequence_number = fields.Integer(required=True)
    type = fields.String(required=True)
    data = WorkbookBlockDataField(required=True, allow_none=True)
    comments = fields.Nested(
        WorkbookBlockCommentResourceSchema(exclude=("block_id",)),
        many=True,
        dump_only=True,
    )
    is_deleted = fields.Boolean(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
