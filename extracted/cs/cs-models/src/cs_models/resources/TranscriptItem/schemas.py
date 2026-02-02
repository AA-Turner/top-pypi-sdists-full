from marshmallow import (
    Schema,
    fields,
    validate,
)


class TranscriptItemResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    transcript_item_id = fields.Integer(required=True)
    transcript_id = fields.Integer(required=True)
    transcript = fields.String(allow_none=True)
    timestamp = fields.DateTime(allow_none=True)
    speaker_id = fields.Integer(allow_none=True)
    speaker_name = fields.String(allow_none=True)
    speaker_title = fields.String(allow_none=True)
    audio_url = fields.String(allow_none=True)
    updated_at = fields.DateTime()
