from marshmallow import Schema, fields


class SellSideAbstractMentionResourceSchema(Schema):
    id = fields.Integer(dump_only=True)

    # which PDF / note
    user_document_id = fields.Integer(required=True)
    # which conference
    meeting_id = fields.Integer(required=True)

    page_number = fields.Integer(allow_none=True)
    char_start = fields.Integer(allow_none=True)
    char_end = fields.Integer(allow_none=True)

    title = fields.String(allow_none=True)
    url = fields.String(allow_none=True)
    abstract_number = fields.String(allow_none=True)
    abstract_search_query = fields.String(allow_none=True)
    context = fields.String(allow_none=True)
    sentiment = fields.String(allow_none=True)

    llm_confidence = fields.Float(allow_none=True)

    raw_json = fields.String(allow_none=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
