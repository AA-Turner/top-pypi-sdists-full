from marshmallow import (
    Schema,
    fields,
    validate,
)


class MeetingOutboxResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    meeting_name = fields.String(required=True)
    start_date = fields.DateTime(allow_none=True)
    end_date = fields.DateTime(allow_none=True)
    meeting_id = fields.Integer(allow_none=True)
    news_id = fields.Integer(required=True)
    reviewed = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()
