from marshmallow import (
    Schema,
    fields,
)


class UserVAAlertResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True)
    va_parameter_id = fields.Integer(required=True)
    threshold_percent = fields.Float(required=True)
    is_active = fields.Boolean(allow_none=True)
    is_deleted = fields.Boolean(allow_none=True)
    last_checked_at = fields.DateTime(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
