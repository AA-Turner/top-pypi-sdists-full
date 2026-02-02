from marshmallow import (
    Schema,
    fields,
    validate,
)


class TranscriptEquityCompanyResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    equity_id = fields.Integer(required=True)
    equity_details = fields.String(allow_none=True)
    company_sec_id = fields.Integer(allow_none=True)
    company_ous_id = fields.Integer(allow_none=True)
    updated_at = fields.DateTime()
