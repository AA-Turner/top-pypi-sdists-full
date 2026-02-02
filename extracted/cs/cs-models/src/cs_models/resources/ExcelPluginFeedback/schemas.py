"""Marshmallow schemas for ExcelPluginFeedback."""
import json
from marshmallow import Schema, fields, validate


class JsonTextField(fields.Field):
    """Field that serializes/deserializes JSON stored as text."""

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return None
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        if isinstance(value, str):
            return value
        return json.dumps(value)


class ExcelPluginFeedbackResourceSchema(Schema):
    """Schema for ExcelPluginFeedback create/read operations."""

    id = fields.Integer(dump_only=True)
    query_id = fields.Integer(required=True)
    user_id = fields.String(required=True, validate=validate.Length(min=1, max=128))
    operation_results = JsonTextField(required=True)
    operations_succeeded = fields.Integer(allow_none=True)
    operations_total = fields.Integer(allow_none=True)
    user_rating = fields.Integer(allow_none=True, validate=validate.Range(min=1, max=5))
    user_comment = fields.String(allow_none=True)
    created_at = fields.DateTime(dump_only=True)


class ExcelPluginFeedbackQueryParamsSchema(Schema):
    """Schema for querying ExcelPluginFeedback."""

    id = fields.Integer()
    query_id = fields.Integer()
    user_id = fields.String()
    user_rating = fields.Integer()


class ExcelPluginFeedbackPatchSchema(Schema):
    """Schema for partial updates to ExcelPluginFeedback."""

    user_rating = fields.Integer(allow_none=True, validate=validate.Range(min=1, max=5))
    user_comment = fields.String(allow_none=True)
