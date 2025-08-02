from marshmallow import (
    Schema,
    fields,
    validate,
)


class JournalScoreResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    issn = fields.String(required=True)
    sjr_score = fields.Float(allow_none=True)
    best_quartile = fields.Integer(allow_none=True)
    h_index = fields.Float(allow_none=True)
    updated_at = fields.DateTime()
