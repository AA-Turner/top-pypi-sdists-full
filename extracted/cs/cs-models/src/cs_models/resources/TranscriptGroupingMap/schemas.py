from marshmallow import (
    Schema,
    fields,
    validate,
)


class TranscriptGroupingMapResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    transcript_id = fields.Integer(required=True)
    grouping_id = fields.Integer(required=True)
    updated_at = fields.DateTime()
