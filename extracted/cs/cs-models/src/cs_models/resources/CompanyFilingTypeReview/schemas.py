from marshmallow import (
    Schema,
    fields,
    validate,
)


class CompanyFilingTypeReviewResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    company_file_id = fields.Integer(required=True)
    filing_type = fields.String(allow_none=True)
    filing_type_score = fields.Float(allow_none=True)
    reviewed = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
