from marshmallow import (
    Schema,
    fields,
    validate,
)


class NCTRefResourceSchema(Schema):
    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.Integer(dump_only=True)
    nct_study_id = fields.Integer(required=True)
    pmid = fields.Integer()
    pubmed_id = fields.Integer(allow_none=True)
    reference_type = fields.String(allow_none=True)
    citation = fields.String()
    updated_at = fields.DateTime(dump_only=True)
