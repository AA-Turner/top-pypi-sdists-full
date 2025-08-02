from marshmallow import (
    Schema,
    fields,
    validate,
)


class UserAutomatedDigestResourceSchema(Schema):
    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True, validate=not_blank)
    type = fields.String(required=True)
    type_id = fields.String(required=True)
    digest_name = fields.String(required=True)
    created_at = fields.DateTime(required=True)
    assistant_user_query_id = fields.Integer(required=True)
    is_deleted = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
