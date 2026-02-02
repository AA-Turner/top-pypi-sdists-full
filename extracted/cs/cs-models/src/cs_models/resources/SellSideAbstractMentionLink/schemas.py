from marshmallow import Schema, fields, validate


class SellSideAbstractMentionLinkResourceSchema(Schema):
    id = fields.Integer(dump_only=True)

    mention_id = fields.Integer(required=True)
    pubmed_id = fields.Integer(required=True)

    # e.g. "grid_cited", "abstract_number", "url", "title_fuzzy", "context_llm"
    match_source = fields.String(required=True, validate=validate.Length(min=1))

    match_score = fields.Float(required=True)

    number_score = fields.Float(allow_none=True)
    url_score = fields.Float(allow_none=True)
    title_score = fields.Float(allow_none=True)
    context_score = fields.Float(allow_none=True)
    llm_score = fields.Float(allow_none=True)

    is_primary = fields.Boolean(required=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
