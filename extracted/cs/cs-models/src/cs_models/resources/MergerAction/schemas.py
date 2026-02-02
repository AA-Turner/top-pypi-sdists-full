from marshmallow import (
    Schema,
    fields,
    validate,
)


class MergerActionResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    acquirer_company = fields.String(required=True, validate=not_blank)
    target_company = fields.String(required=True, validate=not_blank)
    updated_at = fields.DateTime()
