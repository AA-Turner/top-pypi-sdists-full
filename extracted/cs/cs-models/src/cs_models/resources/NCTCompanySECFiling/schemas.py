from marshmallow import (
    Schema,
    fields,
    validate,
)


class NCTCompanySECFilingResourceSchema(Schema):
    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.Integer(dump_only=True)
    nct_study_id = fields.Integer(required=True)
    sec_filing_id = fields.Integer(required=True)
    is_deleted = fields.Boolean(allow_none=True)
    sec_filing_date = fields.DateTime(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
