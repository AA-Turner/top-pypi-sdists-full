from marshmallow import (
    Schema,
    fields,
    validate,
)


class MergerAmountResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    merger_id = fields.Integer(required=True)
    deal_value = fields.Decimal(required=True)
    currency = fields.String(required=True)
    type = fields.String(required=True)
    updated_at = fields.DateTime()