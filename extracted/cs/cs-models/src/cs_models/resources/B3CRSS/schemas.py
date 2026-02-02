from marshmallow import (
    Schema,
    fields,
    validate,
)


class B3CRSSResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    article_id = fields.String(required=True)
    article_date = fields.DateTime(required=True)
    updated_at = fields.DateTime()
