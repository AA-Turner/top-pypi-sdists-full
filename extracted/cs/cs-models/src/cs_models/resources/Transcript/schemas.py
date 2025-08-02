from marshmallow import (
    Schema,
    fields,
    validate,
)


class TranscriptResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    event_id = fields.Integer(required=True)
    date = fields.DateTime(required=True)
    title = fields.String(required=True)
    event_type = fields.String(allow_none=True)
    event_tags = fields.String(allow_none=True)
    human_verified = fields.Boolean(allow_none=True)
    audio_url = fields.String(allow_none=True)
    transcription_status = fields.String(allow_none=True)
    updated_at = fields.DateTime()
