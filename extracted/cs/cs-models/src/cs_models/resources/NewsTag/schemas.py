from marshmallow import (
    Schema,
    fields,
    validate,
)


class NewsTagResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    news_id = fields.Integer(required=True)
    tag = fields.String(required=True, validate=not_blank)
    score = fields.Float(allow_none=True)
    updated_at = fields.DateTime()
