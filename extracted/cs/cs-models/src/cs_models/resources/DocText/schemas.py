from marshmallow import (
    Schema,
    fields,
    validate,
)


class DocTextResourceSchema(Schema):
    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.Integer(dump_only=True)
    news_id = fields.Integer(allow_none=True)
    sec_filing_id = fields.Integer(allow_none=True)
    company_filing_id = fields.Integer(allow_none=True)
    fda_meeting_filing_id = fields.Integer(allow_none=True)
    pubmed_id = fields.Integer(allow_none=True)
    text_type = fields.String(allow_none=True)
    text = fields.String(required=True)
    preferred = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
