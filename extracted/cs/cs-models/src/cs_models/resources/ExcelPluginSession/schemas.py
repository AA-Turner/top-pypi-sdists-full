"""Marshmallow schemas for ExcelPluginSession."""
import json
from marshmallow import Schema, fields, validate, post_load, pre_dump

from .models import ExcelPluginSessionStatus


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


class ExcelPluginSessionResourceSchema(Schema):
    """Schema for ExcelPluginSession create/read operations."""

    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True, validate=validate.Length(min=1, max=128))
    org_id = fields.String(allow_none=True, validate=validate.Length(max=128))
    workbook_name = fields.String(allow_none=True, validate=validate.Length(max=500))
    status = fields.Enum(ExcelPluginSessionStatus, by_value=True, load_default=ExcelPluginSessionStatus.active)
    last_context = JsonTextField(allow_none=True)
    session_metadata = JsonTextField(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ExcelPluginSessionQueryParamsSchema(Schema):
    """Schema for querying ExcelPluginSessions."""

    id = fields.Integer()
    user_id = fields.String()
    org_id = fields.String()
    status = fields.Enum(ExcelPluginSessionStatus, by_value=True)


class ExcelPluginSessionPatchSchema(Schema):
    """Schema for partial updates to ExcelPluginSession."""

    workbook_name = fields.String(allow_none=True, validate=validate.Length(max=500))
    status = fields.Enum(ExcelPluginSessionStatus, by_value=True)
    last_context = JsonTextField(allow_none=True)
    session_metadata = JsonTextField(allow_none=True)
