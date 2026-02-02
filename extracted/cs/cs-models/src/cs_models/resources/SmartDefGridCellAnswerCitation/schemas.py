from marshmallow import Schema, fields, validate


class SmartDefGridCellAnswerCitationResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    answer_id = fields.Integer(required=True)

    source_type = fields.String(allow_none=True)
    source_id = fields.String(allow_none=True)
    url = fields.String(allow_none=True)
    title = fields.String(allow_none=True)
    snippet = fields.String(allow_none=True)
    published_at = fields.DateTime(allow_none=True)
    extra = fields.Raw(allow_none=True)                  # any additional normalized payload
