"""Marshmallow schemas for ExcelPluginQuery."""
import json
from marshmallow import Schema, fields, validate

from .models import ExcelPluginQueryStatus


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


class ExcelPluginQueryResourceSchema(Schema):
    """Schema for ExcelPluginQuery create/read operations."""

    id = fields.Integer(dump_only=True)
    session_id = fields.Integer(allow_none=True)
    user_id = fields.String(required=True, validate=validate.Length(min=1, max=128))
    query_text = fields.String(required=True, validate=validate.Length(min=1))
    workbook_context = JsonTextField(allow_none=True)
    response = JsonTextField(allow_none=True)
    operations_count = fields.Integer(allow_none=True)
    processing_time_ms = fields.Integer(allow_none=True)
    status = fields.Enum(ExcelPluginQueryStatus, by_value=True, load_default=ExcelPluginQueryStatus.pending)
    error_message = fields.String(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ExcelPluginQueryQueryParamsSchema(Schema):
    """Schema for querying ExcelPluginQueries."""

    id = fields.Integer()
    session_id = fields.Integer()
    user_id = fields.String()
    status = fields.Enum(ExcelPluginQueryStatus, by_value=True)


class ExcelPluginQueryPatchSchema(Schema):
    """Schema for partial updates to ExcelPluginQuery."""

    response = JsonTextField(allow_none=True)
    operations_count = fields.Integer(allow_none=True)
    processing_time_ms = fields.Integer(allow_none=True)
    status = fields.Enum(ExcelPluginQueryStatus, by_value=True)
    error_message = fields.String(allow_none=True)
