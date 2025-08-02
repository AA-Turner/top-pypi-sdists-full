from marshmallow import (
    Schema,
    fields,
    validate,
)


class SalesEstimateResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    fiscal_year = fields.Integer(allow_none=True)
    request_id = fields.String(allow_none=True)
    metric = fields.String(allow_none=True)
    drug_name = fields.String(required=True)
    company_name = fields.String(allow_none=True)
    currency = fields.String(allow_none=True)
    fiscal_end_date = fields.DateTime(allow_none=True)
    estimate_date = fields.DateTime(allow_none=True)
    estimate_count = fields.Integer(allow_none=True)
    mean = fields.Decimal(allow_none=True)
    median = fields.Decimal(allow_none=True)
    sd = fields.Float(allow_none=True)
    high = fields.Decimal(allow_none=True)
    low = fields.Decimal(allow_none=True)
    updated_at = fields.DateTime()
