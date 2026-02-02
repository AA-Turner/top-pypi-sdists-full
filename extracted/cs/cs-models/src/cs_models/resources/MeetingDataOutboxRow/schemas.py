from marshmallow import (
    Schema,
    fields,
    validate,
)


class MeetingDataOutboxRowResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    meeting_data_outbox_id = fields.Integer(required=True)
    row = fields.String(allow_none=True)
    updated_at = fields.DateTime()
