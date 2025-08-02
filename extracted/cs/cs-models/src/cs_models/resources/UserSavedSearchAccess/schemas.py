from marshmallow import (
    Schema,
    fields,
    validate,
)


class UserSavedSearchAccessResourceSchema(Schema):
    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True, validate=not_blank)
    saved_search_id = fields.Integer(required=True)
    is_deleted = fields.Boolean(allow_none=True)
    instant_notification = fields.Boolean(allow_none=True)
    daily_digest = fields.Boolean(allow_none=True)
    weekly_digest = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
