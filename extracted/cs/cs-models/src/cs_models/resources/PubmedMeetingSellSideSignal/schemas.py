from marshmallow import Schema, fields, validate


class PubmedMeetingSellSideSignalResourceSchema(Schema):
    id = fields.Integer(dump_only=True)

    pubmed_id = fields.Integer(required=True)
    meeting_id = fields.Integer(required=True)
    sell_side_source_id = fields.Integer(required=True)

    doc_count = fields.Integer(required=True)
    mention_count = fields.Integer(required=True)

    avg_sentiment = fields.Float(allow_none=True)
    max_sentiment = fields.Float(allow_none=True)

    first_mention_at = fields.DateTime(allow_none=True)
    last_mention_at = fields.DateTime(allow_none=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
