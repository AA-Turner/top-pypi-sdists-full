from marshmallow import (
    Schema,
    fields,
    validate,
)


class CompanyOutboxResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    cik_str = fields.String(allow_none=True)
    ticker = fields.String(allow_none=True)
    name = fields.String(required=True)
    cleaned_name = fields.String(allow_none=True)
    exchange = fields.String(allow_none=True)
    company_sec_id = fields.Integer(allow_none=True)
    company_ous_id = fields.Integer(allow_none=True)
    source = fields.String(required=True)
    news_id = fields.Integer(allow_none=True)
    reviewed = fields.Boolean(allow_none=True)
    historical = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
