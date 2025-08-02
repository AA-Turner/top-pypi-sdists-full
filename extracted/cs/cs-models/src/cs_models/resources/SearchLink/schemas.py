from marshmallow import (
    Schema,
    fields,
    validate,
)


class SearchLinkResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True, validate=not_blank)
    type = fields.String(required=True)
    payload = fields.String(required=True)
    is_active = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()
