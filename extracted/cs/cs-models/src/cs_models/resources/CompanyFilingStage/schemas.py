from marshmallow import (
    Schema,
    fields,
    validate,
)


class CompanyFilingStageResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    company_filing_id = fields.Integer(required=True)
    stage = fields.Integer(required=True)
    preferred = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()
