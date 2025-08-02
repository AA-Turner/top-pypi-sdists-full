from marshmallow import (
    Schema,
    fields,
)


class UserSavedSearchResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True)
    search_name = fields.String(required=True)
    search_query = fields.String(required=True)
    search_type = fields.String(required=True)
    is_deleted = fields.Boolean(allow_none=True)
    created_at = fields.DateTime(required=True)
    last_processed = fields.DateTime(allow_none=True)
    instant_notification = fields.Boolean(allow_none=True)
    daily_digest = fields.Boolean(allow_none=True)
    weekly_digest = fields.Boolean(allow_none=True)
    questions = fields.String(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
