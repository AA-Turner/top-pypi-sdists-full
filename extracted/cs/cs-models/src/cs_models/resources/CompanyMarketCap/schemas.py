from marshmallow import (
    Schema,
    fields,
)


class CompanyMarketCapResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    company_id = fields.String(required=True)
    market_cap = fields.Decimal(required=True)
    updated_at = fields.DateTime(dump_only=True)
