from marshmallow import (
    Schema,
    fields,
    validate,
)


class TagTreeResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    tag_id = fields.Integer(required=True)
    label_name = fields.String(required=True, validate=not_blank)
    method = fields.String(required=True)
    score = fields.Float(required=True)
    level = fields.Integer(required=True)
    updated_at = fields.DateTime()
