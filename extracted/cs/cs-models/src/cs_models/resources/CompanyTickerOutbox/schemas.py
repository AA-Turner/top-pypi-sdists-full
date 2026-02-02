from marshmallow import (
    Schema,
    fields,
    validate,
)


class CompanyTickerOutboxResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    type = fields.String(required=True)
    cik_str = fields.String(required=True, validate=not_blank)
    ticker = fields.String(allow_none=True)
    name = fields.String(required=True)
    exchange = fields.String(allow_none=True)
    news_id = fields.Integer(allow_none=True)
    historical = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
