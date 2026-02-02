from marshmallow import (
    Schema,
    fields,
    validate,
)


class DigestResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    saved_search_id = fields.Integer(required=True)
    user_id = fields.String(allow_none=True)
    type = fields.String(required=True)
    description = fields.String(required=True)
    created_at = fields.DateTime()
    sent_at = fields.DateTime()
    updated_at = fields.DateTime()
