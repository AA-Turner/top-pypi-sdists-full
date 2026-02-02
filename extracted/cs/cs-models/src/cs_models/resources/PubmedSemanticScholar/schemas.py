from marshmallow import (
    Schema,
    fields,
    validate,
)


class PubmedSemanticScholarResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    pubmed_id = fields.Integer(required=True)
    paper_id = fields.String(required=True)
    reference_count = fields.String(allow_none=True)
    citation_count = fields.String(allow_none=True)
    influential_citation_count = fields.String(allow_none=True)
    updated_at = fields.DateTime()
